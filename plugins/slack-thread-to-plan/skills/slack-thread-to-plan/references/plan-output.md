# Plan 출력

이 문서가 Plan 파일 포맷의 기준이다.

## 경로 / 네이밍

- 메인 Plan: `~/.claude/plans\{plan-name}.md` (`{plan-name}` = 스레드 주제 kebab-case, 예 `slack-pdf-margin-fix`)
- task 분할 시: `~/.claude/plans\{plan-name}\{2자리순번}-{kebab}.md` (예 `01-fetch-thread.md`)
- 절대경로만 사용 — 상대경로는 permission 매칭 실패로 매번 승인 프롬프트가 뜬다.
- 같은 이름이 있으면 알리고 새 이름 제안. 덮어쓰기는 확인 후.
- task 3개 미만이면 분할하지 않고 메인 파일에 담아도 된다.

## 메인 Plan 구조

```markdown
# {plan title}

> **Created**: YYYY-MM-DD
> **Purpose**: {한 줄 목적}
> **Source**: Slack 스레드 — {채널명} ({permalink})

## Implementation Tasks

| Order | Task Name | File | Description |
|:-----:|-----------|------|-------------|
| 1 | **Task 1** | [01-...](./plan-name/01-....md) | ... |

### Task Rules
1. 순차 실행
2. 각 task 체크리스트 완료 후 다음
3. 완료 시 검증 명령 실행

## 요구사항 (스레드 출처)
{분석 단계 요구사항 표 — 근거 인용 포함 그대로}

## 프로젝트 적용 방안
{적용 위치/방법 표}

## Core Content
{작업 계획 본문}
```

## task 파일 구조

```markdown
# Task {n}: {name}

> **Order**: {n}/{total}
> **Previous task**: [...] or (none)
> **Next task**: [...] or (none)

## Objective
## Checklist
- [ ] {구체적·검증가능한 항목}
## Completion Criteria
1. 체크리스트 완료
2. 빌드/테스트 통과 (해당 시)
## Verification Commands
## Next Task
[Task {n+1}: ...](./{file})
```

task 는 단독 완료·검증 가능한 단위로, 의존 순서와 파일/레이어 경계를 따라 나눈다.

## 저장 직후

multi-file 변경이면 `/review` 실행 여부를 AskUserQuestion 으로 확인한다. "이미 충분히 상세함" 등으로 임의 스킵하지 않고, 사용자가 명시적으로 스킵해야만 건너뛴다. 이후 SKILL.md Step 7 로.
