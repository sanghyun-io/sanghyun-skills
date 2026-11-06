---
name: session-handoff
description: |
  현재 세션의 진행 상황을 새 세션에서 그대로 이어갈 수 있는 "인계(handoff) 프롬프트"로 만든다.
  우선순위 3단계로 전달한다 (위에서부터 시도, 첫 성공에서 멈춤):
  (1) 인계문 전문을 클립보드에 자동 복사 — 새 세션에서 Ctrl+V →
  (2) 실패 시 파일로 저장하고 경로 제공 →
  (3) tool 이 안 먹히는 열화 상태면 순수 텍스트 인라인 출력.
  긴 인계문을 fullscreen 에서 드래그·복사하는 수고를 없애는 게 목적.
  Use when the user mentions 인계, 인계 프롬프트, 핸드오프, 핸드오버, 세션 이어가기, 세션 인계,
  이 세션 그대로 이어갈, 새 세션에서 이어서, handoff, hand-off, resume session, continue in a new session,
  session handoff prompt, or when the current session starts leaking raw tool-call syntax as plain text
  and the user wants to restart cleanly in a fresh session.
  Do NOT trigger for a general "요약해줘"/"summarize" request that is not about continuing work in a new session.
---

# Session Handoff

지금 하던 작업을 새 세션이 끊김 없이 이어받을 인계문으로 만든다. 인자로 강조점을 줄 수 있다 (예: `/session-handoff 디버깅 맥락 위주로`).

## 원칙

- 본문은 **현재 대화 컨텍스트만으로** 쓴다. 채우려고 소스를 새로 Read/Grep/Bash 하지 않는다 — 모르면 `(확인 필요)`. 이 스킬이 필요한 시점엔 tool 이 불안정할 수 있고, 확인은 새 세션이 한다.
- 요약하지 않는다. 이어가는 데 필요하면 길어도 다 담는다.
- NEXT ACTION 은 파일:라인·명령어까지 구체적으로. 워크트리/브랜치/포트/실행 명령 등 환경 상태 필수 (이 사용자는 worktree 를 많이 쓴다).
- 코드 수정·커밋 금지. 쓰는 파일은 2단계의 인계문 `.md` 하나뿐.

## 전달 (위에서부터, 첫 성공에서 멈춤 — 실패하면 재시도로 늘어지지 말고 바로 다음 단계)

**1. 클립보드 (최우선)** — Windows 는 PowerShell 단일따옴표 here-string 으로 전문을 넣는다 (macOS/Linux 는 아래 bash):

```powershell
@'
<채운 템플릿 전문>
'@ | Set-Clipboard
```

```bash
# macOS: pbcopy / Linux(Wayland): wl-copy / Linux(X11): xclip -selection clipboard
pbcopy <<'HANDOFF_EOF'
<채운 템플릿 전문>
HANDOFF_EOF
```

- 보고: "인계문 전문을 클립보드에 복사했습니다. 새 세션에서 Ctrl+V 후 엔터." 클립보드는 휘발성이라 "파일로도 저장할까요?" 한 줄 덧붙여도 된다 (요청 시 2단계).
- 본문에 `'@` 로 시작하는 줄이 있으면 here-string 이 깨진다 → 그 줄 앞에 공백을 넣거나 2단계로.

**2. 파일 (1 실패 시)** — Write 로 `~/.claude/handoffs\<slug>.md` 저장 (slug = 작업 주제 kebab, 불명확하면 `handoff-latest`, 같은 slug 는 덮어씀). 보고: 경로 + 새 세션용 한 줄
`이전 세션 인계 파일을 읽고 그대로 이어가줘 (먼저 "바로 다음 할 일"부터): ~/.claude/handoffs\<slug>.md`

**3. 인라인 (tool 열화 — 호출이 평문으로 샐 때)** — 전문을 코드펜스 하나로 출력하고, 뒤에 "새 세션에 위 블록을 붙여넣으세요" 한 줄.

## 템플릿 (형식 그대로 채움)

```
[세션 인계문 — 이전 세션에서 이어감]
아래 컨텍스트를 그대로 이어받아 작업을 계속하세요. 먼저 "바로 다음 할 일"부터 수행하세요.

## 1. 목표 / 작업 개요
- 무엇을, 왜 하고 있는지 (한두 문장)
- 최종 완료 기준(Done)

## 2. 작업 환경
- 저장소:
- 워크트리 경로:
- 브랜치:
- 심링크/포트/실행 명령 등 기동에 필요한 것:
- 관련 서비스·의존성:

## 3. 지금까지 한 일
- 변경한 파일 (경로 + 요지):
- 내린 핵심 결정 / 접근 방식:
- 검증한 것 (테스트/빌드/실행 결과):

## 4. 현재 상태 / 멈춘 지점
- 정확히 어디까지 됐고 어디서 멈췄는지:

## 5. 바로 다음 할 일 (NEXT ACTION)
- 새 세션이 가장 먼저 해야 할 구체적 행동 (파일:라인, 명령어까지):

## 6. 미해결 / 블로커 / 열린 질문
- 아직 못 정한 것, 막힌 것, 사용자 확인이 필요한 것:

## 7. 참고 파일·경로
- file_path:line 형태로 관련 위치 나열:

## 8. 이 세션에서 확립된 사용자 제약·선호
- 반드시 지켜야 할 규칙/선호 (예: 특정 라이브러리 금지, 워크트리 규칙 등):
```

## 열화 재발 줄이기 (참고)

tool-call 이 평문으로 새는 건 고컨텍스트에서의 모델 레벨 현상이다 (`anthropics/claude-code#64108`, open; harness 는 fail-closed 라 샌 XML 은 실행 안 됨). 설정으로 완전 차단 불가, 빈도만 줄인다:
- `/clear` 가 가장 확실 — tool call 이 두 번 연속 새면 인계문 뽑고 `/clear`. `/compact` 는 차선 (압축 블록 자체가 트리거가 되기도 함).
- 긴 세션엔 Opus 대신 Fable/Sonnet (Opus 가 가장 취약 — 더 큰 컨텍스트를 다뤄 임계점에 먼저 도달. Fable 은 빈도가 낮다).
- 큰 파일은 라인 범위로 읽고, 큰 작업은 서브에이전트로 분리. 거대한 CLAUDE.md/rules 경량화.
