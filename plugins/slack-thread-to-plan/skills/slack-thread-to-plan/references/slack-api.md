# Slack API 참조 (`scripts/fetch_thread.py`)

## permalink 파싱

```
https://<workspace>.slack.com/archives/<CHANNEL>/p<DIGITS>[?thread_ts=<TS>&cid=<CHANNEL>]
```

- `<CHANNEL>`: `C..` public / `G..` private / `D..` DM. `?cid=` 가 있으면 그 값 우선.
- `p<DIGITS>` → ts: 뒤 6자리 앞에 소수점 (`p1700000000123456` → `1700000000.123456`).
- `?thread_ts=` (댓글 permalink) 가 있으면 그 부모 ts 기준으로 스레드 전체를 가져온다.

## 사용 API (Bearer `SLACK_USER_TOKEN`)

- `conversations.replies` (`channel`, `ts`=부모, cursor 페이지네이션) — `*:history` scope. messages[0] 이 부모, 나머지 시간순 댓글.
- `users.info` — `users:read`. 이름 우선순위 `profile.display_name` → `profile.real_name` → `real_name` → `name`. 실패 시 user ID 로 fallback (흐름 유지).
- `conversations.info` — 채널명 표시용(`channels:read`/`groups:read`). DM 은 `(DM)`, 권한 없으면 ID.
- `ratelimited` 는 스크립트가 백오프 재시도.

## 텍스트 정제 (clean_text)

`<@U..>` → `@이름`, `<#C..|name>` → `#name`, `<url|label>` → `label (url)`, `<!here>`/`<!channel>` → `@here`/`@channel`, `<!subteam^S..|@team>` → `@team`, HTML entity 복원.

## 종료 코드

0 성공 / 2 인자 오류 / 3 `SLACK_USER_TOKEN` 미설정 / 4 URL 파싱 실패 / 5 Slack API 오류. 대응은 [troubleshooting.md](troubleshooting.md).
