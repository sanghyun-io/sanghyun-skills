---
name: multi-hypothesis
description: |
  여러 원인 가설을 병렬로 깊게 파는 RCA(Root Cause Analysis) 방법.
  첫 가설에 단정 짓지 않고 "이게 원인이 아니라면?"을 반복해 다중 가설을 동시에 끝까지 추적한다.
  TRIGGER: "원인 분석", "근본 원인", "왜 이렇게 됐는지", "여러 가능성", "다중 가설", "multi-hypothesis", "multiple working hypotheses", "root cause", "RCA" 류 발화.
  구조: Opus 관리자 + Sonnet 팀원 병렬 조사 + Codex(Sonnet 경유) 위임. 가설별 general-purpose Agent 를 병렬 spawn (팀은 첫 spawn 시 자동 형성 — v2.1.178+).
invocation:
  command: multi-hypothesis
  user_invocable: true
  args:
    - name: symptom
      description: 분석할 증상/관찰/문제 설명 (생략 시 사용자에게 질문)
      required: false
---

# Multi-Hypothesis RCA

기반: T.C. Chamberlin (1890), *The Method of Multiple Working Hypotheses* — 첫 가설에 애착을 갖지 말고 여러 가설을 살려둔 채 동시에 끝까지 추적한다. **분석 전용 스킬 — 복구/수정안은 제안하지 않는다** (RCA 메모리 피드백).

## 절차

1. **증상 확정** (Opus) — 발화/인자에서 증상 추출, 부족하면 AskUserQuestion.
2. **가설 도출** (Opus) — 상호 독립적·상호배타적이고 검증 가능·반증 가능·구체적인("환경 문제" 말고 "DNS 캐시 stale") 가설 3–5개. 누락 방지를 위해 카테고리를 한 번씩 훑는다: 코드/로직(경계조건·off-by-one), 상태/데이터(마이그레이션·캐시), 환경/설정(환경변수·권한·의존성 버전), 동시성/타이밍(race·deadlock·retry storm), 인프라/네트워크(DNS·TLS·proxy·rate limit), 인적 요인(최근 변경·배포·수동 개입), 외부 의존(third-party API·모니터링 사각지대).
3. **승인** — 가설 목록을 사용자에게 제시하고 AskUserQuestion 으로 진행 승인.
4. **병렬 spawn** (Opus) — 가설마다 `subagent_type: "general-purpose"` Agent 를 **한 메시지에서 병렬로** spawn. 팀은 첫 spawn 시 자동 형성된다(`TeamCreate`/`TeamDelete` 는 v2.1.178 에서 폐지).
   - `explore` 금지 — `SendMessage` 가 없어 보고를 못 한다.
   - 다른 작업의 Agent 가 활성 중이면(`ListAgents` 로 확인) 이름에 `mh-{N}` prefix 를 붙이고, 가설 Agent 에는 이번 RCA 범위만 전달한다. 병행 여부가 애매하면 "병행 / 대기"를 사용자에게 묻는다.
5. **조사** (팀원) — 반증을 먼저 찾으며 깊이 제한 없이 검증 가능한 결론까지. 새 하위 가설이 생기면 재귀적으로 `general-purpose` Agent 를 추가 spawn. 필요 시 Codex 위임(아래).
6. **보고** (팀원) — `SendMessage` 로 Opus 에 보고.
7. **종합** (Opus) — 모든 줄기가 끝나기 전 결론 금지. 형식은 결과 모양에 맞춘다(고정 템플릿 없음): 단일 원인 → 서사형 + 반증 가설 부록 / 다중 원인 → 인과 다이어그램 또는 가설×기여도 표 / 전부 INCONCLUSIVE → 가설×필요 증거 표 / 깊이별 분기 → 트리 / 가설 간 상호작용 → 매트릭스.
8. **정리** — 이 RCA 가 spawn 한 Agent 가 모두 보고를 마쳤는지 확인. 에러/중단 시 그 Agent 들에만 shutdown_request/cancel 을 보낸다. **다른 작업의 Agent 는 건드리지 않는다**(컨텍스트 손실).

## Codex 위임 (선택, 팀원만)

[codex-core](https://github.com/sanghyun-io/codex-app-server-plugin) 같은 Codex 위임 플러그인이 설치돼 있을 때만 쓴다. 없으면 이 절을 건너뛰고 Glob/Grep/Read/Bash 로 조사한다. Opus 는 Codex 를 직접 호출하지 않는다 — 반드시 팀원이 위임한다.

- INCONCLUSIVE 로 수렴 중이고 코드 내부 동작이 원인일 가능성 → 결론 전에 `/codex-core:delegate --read-only` 위임.
- 보안/취약점 관점 필요 → 팀원은 red-review 권한이 없으므로 Opus 에 에스컬레이션.
- 단순 grep/glob 수준 → 직접 처리 (Codex 호출은 토큰 낭비).
- Codex 실패(미설치 / 인증 실패 → `codex login` / rate limit / crash) → Glob/Grep/Read/Bash 로 한계까지 조사하고, 그래도 INCONCLUSIVE 면 **Codex 필요 사유 / 불가 사유 / 다음 검증 액션(구체적 파일·쿼리·실험)** 을 명시해 보고.

## 팀원 프롬프트 템플릿

```
You are a Sonnet investigator on a multi-hypothesis RCA team.

## Your Hypothesis
{가설 N: 한 줄 요약 + 상세 정의}

## Symptoms / Observations
{증상 전체 컨텍스트}

## Your Job
1. 이 가설을 깊게 조사한다. 깊이 제한 없음.
2. 반증을 먼저 찾는다.
3. 새 하위 가설이 생기면 general-purpose agent 를 재귀 spawn 한다.
4. 깊은 코드 분석이 필요하고 Codex 위임 플러그인이 있으면 /codex-core:delegate --read-only 로 위임한다.
5. 분석만 한다 — 복구/수정안 제안 금지.
6. 결과는 SendMessage 로 관리자에게 보고한다.

## Report Format
- 결론: CONFIRMED / REFUTED / INCONCLUSIVE
- 근거: 파일 경로 + 라인 + 인용
- 반증 시도: 어떤 관찰이 이 가설을 깨뜨릴 수 있는지 + 시도 결과
- 잔여 불확실성: 더 파면 검증할 수 있는 부분
- 하위 가설: 추가 spawn 한 sub-agent 결과 요약
```

예: `/multi-hypothesis 배포 후 일부 사용자만 401 에러 발생`

*Created 2026-04-29 · Last modified 2026-10-06 (condensed; v2.1.178 auto-team 반영)*
