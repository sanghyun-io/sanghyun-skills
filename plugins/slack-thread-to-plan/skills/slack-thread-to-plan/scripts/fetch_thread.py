#!/usr/bin/env python3
"""
Slack 스레드 fetcher — permalink URL 하나로 스레드 전체를 읽어 정제된 마크다운으로 출력.

표준 라이브러리만 사용 (urllib). 외부 의존성 없음.

사용:
    python fetch_thread.py <slack_permalink_url>
    python fetch_thread.py <slack_permalink_url> --json              # 가공 전 원시 JSON
    python fetch_thread.py <slack_permalink_url> --download-files    # 첨부 이미지 다운로드
    python fetch_thread.py <slack_permalink_url> --download-files --files-dir <DIR>

옵션:
    --json            가공 전 원시 JSON 출력
    --download-files  스레드의 image/* 첨부를 로컬에 다운로드하고 마크다운에 로컬 경로를 기재
    --files-dir DIR   다운로드 위치 (기본: 현재 작업 디렉토리의 ./slack-files)

환경변수:
    SLACK_USER_TOKEN  (필수)  xoxp-... user token

필요 scope (user token):
    channels:history, groups:history, im:history, mpim:history
    users:read (작성자 id -> 이름 매핑용; 없으면 id 그대로 표시)
    (선택) conversations.info 의 채널명 표시에 channels:read / groups:read

종료 코드:
    0  성공
    2  사용법/인자 오류
    3  토큰 누락
    4  URL 파싱 실패
    5  Slack API 오류 (ok=false 또는 HTTP 오류)
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SLACK_API = "https://slack.com/api"


# ---------------------------------------------------------------------------
# URL 파싱
# ---------------------------------------------------------------------------
def parse_permalink(url):
    """
    Slack permalink 을 (channel_id, ts, thread_ts_or_None) 로 분해.

    지원 포맷:
      https://workspace.slack.com/archives/C0123ABCD/p1700000000123456
      https://workspace.slack.com/archives/C0123ABCD/p1700000000123456?thread_ts=1699999999.000100&cid=C0123ABCD
      https://workspace.slack.com/archives/G0123ABCD/p...   (private channel/group)
      https://workspace.slack.com/archives/D0123ABCD/p...   (DM)

    p-number -> ts 규칙:
      p1700000000123456  ->  1700000000.123456
      (뒤에서 6자리 앞에 소수점 삽입)
    """
    parsed = urllib.parse.urlparse(url)
    # /archives/<channel>/p<digits>
    m = re.search(r"/archives/([A-Z0-9]+)/p(\d+)", parsed.path)
    if not m:
        return None
    channel = m.group(1)
    p_digits = m.group(2)

    # p-number -> ts (뒤 6자리 앞에 소수점)
    if len(p_digits) <= 6:
        return None
    ts = p_digits[:-6] + "." + p_digits[-6:]

    # query 에 thread_ts 가 있으면 그게 스레드 부모. cid 가 있으면 channel 보정.
    qs = urllib.parse.parse_qs(parsed.query)
    thread_ts = qs.get("thread_ts", [None])[0]
    cid = qs.get("cid", [None])[0]
    if cid:
        channel = cid

    return channel, ts, thread_ts


# ---------------------------------------------------------------------------
# Slack API 호출
# ---------------------------------------------------------------------------
def slack_get(method, token, params, retries=3):
    """Slack Web API GET 호출. ok=false 면 SlackError 발생. 429 는 백오프 재시도."""
    url = SLACK_API + "/" + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", "1"))
                time.sleep(wait)
                last_err = "HTTP 429 rate limited"
                continue
            raise SlackError("HTTP %d calling %s: %s" % (e.code, method, e.reason))
        except urllib.error.URLError as e:
            last_err = "network error: %s" % e.reason
            time.sleep(1 + attempt)
            continue

        if not data.get("ok"):
            err = data.get("error", "unknown_error")
            raise SlackError("Slack API '%s' returned ok=false: %s" % (method, err))
        return data
    raise SlackError("'%s' failed after %d attempts: %s" % (method, retries, last_err))


class SlackError(Exception):
    pass


def fetch_replies(channel, ts, token):
    """conversations.replies 로 스레드 전체 메시지를 cursor 페이지네이션 따라 수집."""
    messages = []
    cursor = None
    while True:
        params = {"channel": channel, "ts": ts, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = slack_get("conversations.replies", token, params)
        messages.extend(data.get("messages", []))
        meta = data.get("response_metadata", {})
        cursor = meta.get("next_cursor")
        if not data.get("has_more") or not cursor:
            break
    return messages


def resolve_users(user_ids, token):
    """user id 집합 -> {id: 표시이름}. users:read 없거나 실패하면 id 그대로 fallback."""
    names = {}
    for uid in user_ids:
        if not uid:
            continue
        try:
            data = slack_get("users.info", token, {"user": uid})
            prof = data.get("user", {})
            display = (
                prof.get("profile", {}).get("display_name")
                or prof.get("profile", {}).get("real_name")
                or prof.get("real_name")
                or prof.get("name")
                or uid
            )
            names[uid] = display
        except SlackError:
            names[uid] = uid
    return names


def channel_name(channel, token):
    """채널명 조회. 권한 없거나 DM 이면 id 그대로."""
    try:
        data = slack_get("conversations.info", token, {"channel": channel})
        ch = data.get("channel", {})
        if ch.get("is_im"):
            return "(DM)"
        return "#" + ch.get("name", channel)
    except SlackError:
        return channel


# ---------------------------------------------------------------------------
# 첨부 파일 다운로드
# ---------------------------------------------------------------------------
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPG_SIG = b"\xff\xd8\xff"
GIF_SIG = b"GIF8"


def _safe_name(file_id, name):
    """파일명 정제. id 를 prefix 로 붙여 충돌 방지. 경로 분리자/제어문자 제거."""
    base = name or "file"
    base = re.sub(r"[^\w.\-]", "_", base)
    return "%s_%s" % (file_id, base)


def download_files(messages, token, files_dir):
    """
    스레드 메시지의 image/* 첨부를 files_dir 에 다운로드.

    {file_id: local_path} 매핑을 반환. 다운로드 실패/비이미지는 매핑에서 제외.
    Slack url_private 는 Authorization: Bearer 헤더가 있어야 받아진다.
    토큰 없이 받으면 HTML 로그인 페이지가 오므로, 받은 바이트의 시그니처를 검증한다.
    """
    if not os.path.isdir(files_dir):
        os.makedirs(files_dir, exist_ok=True)

    saved = {}
    for msg in messages:
        for f in msg.get("files", []):
            mimetype = f.get("mimetype", "")
            if not mimetype.startswith("image/"):
                continue
            url = f.get("url_private_download") or f.get("url_private")
            if not url:
                continue
            file_id = f.get("id", "F")
            dest = os.path.join(files_dir, _safe_name(file_id, f.get("name", "image")))
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                sys.stderr.write("WARN: 첨부 다운로드 실패 (%s): %s\n" % (file_id, e))
                continue
            # 시그니처 검증 — HTML/에러페이지면 스킵
            if not (data.startswith(PNG_SIG) or data.startswith(JPG_SIG) or data.startswith(GIF_SIG)):
                sys.stderr.write(
                    "WARN: %s 응답이 이미지가 아님 (토큰/권한 문제 가능). 저장 안 함.\n" % file_id
                )
                continue
            with open(dest, "wb") as fp:
                fp.write(data)
            saved[file_id] = dest
    return saved


# ---------------------------------------------------------------------------
# 텍스트 정제
# ---------------------------------------------------------------------------
def clean_text(text, user_names):
    """Slack mrkdwn -> 읽기 쉬운 텍스트. <@U..> 멘션을 이름으로 치환."""
    if not text:
        return ""

    # 사용자 멘션 <@U123> 또는 <@U123|name>
    def repl_user(m):
        uid = m.group(1)
        return "@" + user_names.get(uid, uid)

    text = re.sub(r"<@([A-Z0-9]+)(?:\|[^>]*)?>", repl_user, text)

    # 채널 멘션 <#C123|general> -> #general
    text = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", lambda m: "#" + m.group(1), text)
    text = re.sub(r"<#([A-Z0-9]+)>", lambda m: "#" + m.group(1), text)

    # 링크 <https://url|label> -> label (url)  /  <https://url> -> url
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", lambda m: "%s (%s)" % (m.group(2), m.group(1)), text)
    text = re.sub(r"<(https?://[^>]+)>", lambda m: m.group(1), text)

    # 특수 멘션 <!here> <!channel> <!subteam^..|@team>
    text = re.sub(r"<!subteam\^[A-Z0-9]+\|?([^>]*)>", lambda m: m.group(1) or "@team", text)
    text = re.sub(r"<!([a-zA-Z]+)(?:\|[^>]*)?>", lambda m: "@" + m.group(1), text)

    # HTML 엔티티 디코드
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return text


def fmt_ts(ts):
    """ts (epoch.micro 문자열) -> 사람이 읽는 시각."""
    try:
        sec = float(ts)
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(sec))
    except (ValueError, TypeError):
        return ts


def build_markdown(channel, channel_disp, messages, user_names, saved_files=None):
    """메시지 리스트 -> 정제 마크다운. saved_files: {file_id: local_path} (다운로드 시)."""
    saved_files = saved_files or {}
    lines = []
    lines.append("# Slack 스레드")
    lines.append("")
    lines.append("- 채널: %s (`%s`)" % (channel_disp, channel))
    lines.append("- 메시지 수: %d" % len(messages))
    if messages:
        lines.append("- 기간: %s ~ %s" % (fmt_ts(messages[0].get("ts", "")), fmt_ts(messages[-1].get("ts", ""))))
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, msg in enumerate(messages):
        uid = msg.get("user") or msg.get("bot_id") or "unknown"
        name = user_names.get(uid, uid)
        when = fmt_ts(msg.get("ts", ""))
        role = "부모 메시지" if i == 0 else "댓글 %d" % i
        lines.append("## [%s] %s — %s" % (role, name, when))
        lines.append("")
        body = clean_text(msg.get("text", ""), user_names)
        lines.append(body if body.strip() else "_(텍스트 없음 — 첨부/리액션만 존재 가능)_")

        # 첨부 파일
        files = msg.get("files", [])
        if files:
            lines.append("")
            lines.append("**첨부:**")
            for f in files:
                fname = f.get("name", "file")
                ftype = f.get("filetype", "")
                local = saved_files.get(f.get("id"))
                if local:
                    lines.append("- %s (%s) — 로컬: `%s`" % (fname, ftype, local))
                else:
                    lines.append("- %s (%s)" % (fname, ftype))

        # 리액션
        reactions = msg.get("reactions", [])
        if reactions:
            rx = ", ".join(":%s: x%d" % (r.get("name", "?"), r.get("count", 0)) for r in reactions)
            lines.append("")
            lines.append("**리액션:** " + rx)

        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv):
    # 인자 파싱: positional(URL) + boolean flag(--json/--download-files) + value flag(--files-dir DIR)
    positional = []
    flags = set()
    files_dir = os.path.join(os.getcwd(), "slack-files")
    rest = argv[1:]
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok == "--files-dir":
            if i + 1 >= len(rest):
                sys.stderr.write("ERROR: --files-dir 뒤에 경로가 필요합니다.\n")
                return 2
            files_dir = rest[i + 1]
            i += 2
            continue
        if tok.startswith("--"):
            flags.add(tok)
            i += 1
            continue
        positional.append(tok)
        i += 1

    if len(positional) != 1:
        sys.stderr.write(
            "usage: fetch_thread.py <slack_permalink_url> [--json] "
            "[--download-files [--files-dir DIR]]\n"
        )
        return 2

    url = positional[0]
    token = os.environ.get("SLACK_USER_TOKEN")
    if not token:
        sys.stderr.write("ERROR: SLACK_USER_TOKEN 환경변수가 설정되지 않았습니다.\n")
        return 3

    parsed = parse_permalink(url)
    if not parsed:
        sys.stderr.write(
            "ERROR: Slack permalink 파싱 실패: %s\n"
            "  기대 포맷: https://<workspace>.slack.com/archives/<CHANNEL>/p<digits>\n" % url
        )
        return 4

    channel, ts, thread_ts = parsed
    # thread_ts 가 있으면 그 부모를 기준으로 (URL 이 댓글 permalink 인 경우)
    fetch_ts = thread_ts if thread_ts else ts

    try:
        messages = fetch_replies(channel, fetch_ts, token)
        if not messages:
            sys.stderr.write("WARN: 메시지가 비어 있습니다. ts/channel 확인 필요.\n")
        user_ids = set(m.get("user") for m in messages if m.get("user"))
        user_names = resolve_users(user_ids, token)
        channel_disp = channel_name(channel, token)
    except SlackError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        # 흔한 원인 힌트
        msg = str(e)
        if "not_in_channel" in msg or "channel_not_found" in msg:
            sys.stderr.write("  힌트: 토큰 소유 계정이 해당 채널의 멤버인지 확인하세요.\n")
        elif "missing_scope" in msg:
            sys.stderr.write("  힌트: 토큰에 *:history / users:read scope 가 필요합니다.\n")
        elif "invalid_auth" in msg or "token_revoked" in msg:
            sys.stderr.write("  힌트: SLACK_USER_TOKEN 이 만료/폐기되었을 수 있습니다.\n")
        return 5

    saved_files = {}
    if "--download-files" in flags:
        saved_files = download_files(messages, token, files_dir)
        sys.stderr.write("INFO: 이미지 첨부 %d개 다운로드 -> %s\n" % (len(saved_files), files_dir))

    if "--json" in flags:
        out = {
            "channel": channel,
            "channel_name": channel_disp,
            "ts": fetch_ts,
            "user_names": user_names,
            "saved_files": saved_files,
            "messages": messages,
        }
        sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(build_markdown(channel, channel_disp, messages, user_names, saved_files))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
