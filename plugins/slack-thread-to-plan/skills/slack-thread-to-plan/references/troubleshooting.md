# 트러블슈팅

실패하면 멈추고 사용자에게 보고한다. 추측으로 다음 시도를 이어가지 않는다.

## 종료 코드별

- **2 인자 오류** — URL 을 따옴표로 감쌌는지 (`&` 포함 query 가 셸에서 잘림). `--files-dir` 뒤 경로 누락도 2.
- **3 토큰 미설정** — 토큰은 `~/.bashrc` 에 export 되어 있어 PowerShell 세션에서 안 보일 수 있다. 사용자 확인 후에만 일회성 주입: `$env:SLACK_USER_TOKEN = "<token>"; python ...`. 토큰 값은 출력·echo 금지.
- **4 URL 파싱 실패** — 채널 링크/단축 URL 이 아니라 메시지 permalink("링크 복사")여야 한다.
- **5 Slack API 오류** — stderr 의 `error`:
  - `not_in_channel` / `channel_not_found` → 토큰 계정이 채널 멤버 아님. 참여 후 재시도
  - `missing_scope` → 토큰 재발급 필요 (아래 scope)
  - `invalid_auth` / `token_revoked` → 새 토큰 발급 후 환경변수 갱신
  - `thread_not_found` → ts 가 부모가 아님. `?thread_ts=` 유무 확인
  - `ratelimited` → 자동 재시도. 지속되면 잠시 후

## scope

- `channels:history` / `groups:history` / `im:history` / `mpim:history` — 각각 public / private / DM / 그룹 DM. 없으면 fetch 실패(코드 5).
- `users:read`, `channels:read`/`groups:read` — 없어도 이름 대신 ID 로 동작.

## 코드 0 인데 메시지 0개

스레드가 비었거나 권한 경계. private 채널에 public scope 만 있으면 ok=true + 빈 배열일 수 있다 → scope 재확인.

## 한글 깨짐

`PYTHONIOENCODING=utf-8` 를 붙였는데도 파이프 경유로 깨지면, 출력을 현재 프로젝트 `tmp-debug/` 로 리다이렉트(`> tmp-debug\slack-thread.md`)한 뒤 Read 로 읽는다.
