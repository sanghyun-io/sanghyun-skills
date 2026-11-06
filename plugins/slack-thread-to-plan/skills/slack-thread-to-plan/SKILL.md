---
name: slack-thread-to-plan
description: |
  Slack 스레드 permalink URL 을 받아 conversations.replies API 로 스레드 전체(부모+모든 댓글)를 읽어오고,
  요구사항을 분석한 뒤 현재 프로젝트에 어떻게 적용할지 작업 계획을 plan-structure 포맷의 Plan 파일로 저장한다.
  Use when the user mentions 슬랙 스레드, 슬랙 대화, Slack 스레드, Slack thread, 슬랙 요구사항, 스레드 분석,
  슬랙 링크를 공유하면서 "이거 분석해줘 / 요구사항 정리해줘 / 작업 계획 세워줘" 라고 요청할 때,
  or shares a slack.com/archives/... permalink and asks to analyze it, extract requirements, or build a work plan.
  Do NOT trigger for general Slack API questions with no thread URL and no intent to plan.
---

# Slack Thread → Plan

흐름: Slack URL → 스레드 fetch → 요구사항 분석 → 프로젝트 적용 방안 → 작업 계획 → Plan 파일 저장 → 다음 행동 질문.

산출물은 **분석 + 계획까지**. 사용자가 Step 7 에서 "지금 구현"을 고르기 전엔 코드를 건드리지 않는다.

원칙:
- 원문에 없는 요구사항을 지어내지 않는다. 모호·충돌은 AskUserQuestion 으로 확정.
- 스레드 원문을 통째로 쏟지 말고 핵심 인용 + 요약.
- 토큰 값은 출력/로깅/echo 하지 않는다.
- Plan 파일 덮어쓰기는 사용자 확인 후.

## 사전 조건

- 환경변수 `SLACK_USER_TOKEN` (xoxp-). scope: `channels:history` `groups:history` `im:history` `mpim:history` `users:read`
- 토큰 소유 계정이 해당 채널 멤버여야 함 (private/DM 포함)
- `~/.bashrc` 에 export 되어 있으나 셸에 따라 안 보일 수 있다 → 실패 시 [troubleshooting](references/troubleshooting.md)

## Fetch

PowerShell 도구로 실행 (Bash 에서는 `$SLACK_USER_TOKEN` 이 비는 경우가 있음):

```powershell
$env:PYTHONIOENCODING="utf-8"; python "${CLAUDE_PLUGIN_ROOT}/skills/slack-thread-to-plan/scripts/fetch_thread.py" "<SLACK_PERMALINK_URL>"
```

- `PYTHONIOENCODING=utf-8` 필수 — 없으면 cp949 콘솔에서 한글/em-dash 로 `UnicodeEncodeError` 종료(실제 발생). PowerShell 도구는 호출마다 env 가 초기화되므로 매번 prefix.
- 출력: 정제된 마크다운(작성자명·시각·본문·첨부·리액션, 멘션은 이름으로 치환). 원시 JSON 은 `--json`.
- 첨부 이미지는 기본 메타만. 내용이 필요하면 `--download-files [--files-dir <DIR>]` (기본 `./slack-files`) 후 Read 로 확인.
- URL 은 따옴표로 감싼다 (`&` 포함 query). 댓글 permalink 의 `?thread_ts=` 는 자동으로 부모 기준 처리.

## 워크플로우

1. **URL 확보** — 없으면 요청. 형식 `https://<workspace>.slack.com/archives/<CHANNEL>/p<digits>`.
2. **Fetch** — 종료 코드 ≠ 0 이면 멈추고 보고 ([troubleshooting](references/troubleshooting.md)).
3. **요구사항 분석** — [analysis-framework](references/analysis-framework.md) 체크리스트 기준. 모호점은 AskUserQuestion.
4. **적용 방안** — 프로젝트 `CLAUDE.md`, `docs/CHECKPOINT.md`, `docs/WORK_QUEUE.md`(있으면)를 읽고 요구사항별 파일/모듈/레이어 매핑. 기존 결정과 충돌하면 명시하고 판단을 구한다.
5. **작업 계획** — 순서 있는 task (의존성·검증 방법 포함). 대화창에 먼저 요약 출력.
6. **Plan 저장** — 사용자 확인 후 `~/.claude/plans\{plan-name}.md`. 포맷/분할 규칙은 [plan-output](references/plan-output.md). multi-file 변경이면 `/review` 실행 여부를 AskUserQuestion 으로 확인 (임의 스킵 금지).
7. **다음 행동 질문 (필수, skill 종료 지점)** — plain text 가 아니라 AskUserQuestion 으로. 라벨/설명은 이모지·장식문자 없이 한글+ASCII. 상황에 맞게 옵션 가감:
   - 지금 구현 시작 (권장) — Pre-work 규칙대로 worktree 생성(`.claude/worktrees/`) → 코드 읽기 → 구현
   - 여기서 종료 — Plan 경로 한 줄 안내
   - GitHub Issue 발행 — Plan 요약을 Issue 로 (`gh issue create`)
   - WORK_QUEUE 에 추가 — `docs/WORK_QUEUE.md` 대기 큐에 삽입

   "지금 구현 시작" 외에는 코드를 건드리지 않는다.

## References

- [slack-api.md](references/slack-api.md) — permalink 파싱, 사용 API, 텍스트 정제, 종료 코드. 스크립트를 이해/수정할 때.
- [analysis-framework.md](references/analysis-framework.md) — 추출 체크리스트 + 대화창 출력 템플릿. Step 3~5.
- [plan-output.md](references/plan-output.md) — Plan 파일 경로/포맷/task 분해. Step 6.
- [troubleshooting.md](references/troubleshooting.md) — 종료 코드별 대응, scope/토큰/한글 깨짐. fetch 실패 시.
