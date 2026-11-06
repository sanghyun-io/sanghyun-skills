---
name: team-launch
description: |
  여러 개의 독립적 코딩 작업을 Team Agent 구조로 병렬 위임하는 매니저 패턴.
  사용자가 "관리자" 역할을 명시적으로 위임할 때 — 작업 N개를 worktree N개로 분리하고
  각 worktree 에 Sonnet 팀원 agent 를 붙여 동시 구현 + 커밋 + PR 까지 자율 진행.
  Opus 매니저는 통합 검증 + 머지 + conflict 해결만 담당.

  TRIGGER 예시 발화:
    - "Team Agent 구성해서 (너가 관리자)"
    - "팀 만들어서 각자 위임해"
    - "Team 으로 병렬 진행"
    - "관리자 역할로 N개 작업 위임"
    - "팀원들에게 분배"

  vs Agent (단순 위임) 와의 차이:
    - Agent 는 단일 작업 위임, 결과 받아 통합
    - Team Agent 는 N개 작업 동시 위임 + 매니저 책임 (자원 분리 / 통합 검증 / 순차 머지) 명시
    - 사용자가 "관리자" 단어를 쓰면 Team Agent 구조를 의도한 것
    - (v2.1.178+) 팀은 첫 팀원 Agent spawn 시 자동 형성되고 세션 종료 시 자동 정리됨 — TeamCreate/TeamDelete 도구는 폐지됨
invocation:
  command: team-launch
  user_invocable: true
  args:
    - name: tasks
      description: 위임할 작업 목록 (생략 시 AskUserQuestion 으로 입력 받음)
      required: false
---

# Team Launch

사용자가 "관리자" 역할을 준 것은 단순 위임이 아니라 조직 구조를 요청한 것이다. 매니저(Opus = self)는 자원 분리, 충돌 회피, 통합 검증, 순차 머지, 정리까지 책임진다. Agent 병렬 spawn 만 하고 이 책임을 빼면 이 스킬을 쓴 의미가 없다.

## 절차

1. **작업 목록 확정** — 발화에서 추출, 부족하면 AskUserQuestion (작업 N개 / 우선순위 / 의존성).
2. **충돌 분석** — 작업들이 같은 파일을 건드리는지 점검. 겹치면 사용자에게 보고하고 (a) 직렬화 (b) 머지 후 재정렬 (c) 한 명에게 통합 위임 중 선택받는다.
3. **자원 분리** — 작업마다 고유한 브랜치(`feat/{task}`), worktree 경로, dev 서버 포트.
   - 포트: main/기본 8080, 팀원 8081, 8082, 8083 … 최대 5명(8081-8085). 그 이상은 직렬화.
4. **worktree 생성** — `git worktree add ../{name} -b feat/{branch} origin/main` + 의존성 폴더(`node_modules`, `.venv`)는 복사·재설치하지 말고 main 쪽으로 링크한다(Windows 는 junction, 그 외 symlink). 팀원은 worktree 안에서 `npm install`/`pip install` 금지 — 링크를 실제 폴더로 덮어쓴다.
5. **팀원 spawn** — `Agent` 도구, `subagent_type: "general-purpose"`, `model: sonnet`, `name` 지정(SendMessage 로 addressable). **한 메시지에서 병렬 spawn**. 팀은 첫 spawn 시 자동 형성된다 (별도 생성 단계 없음, `TeamCreate`/`TeamDelete` 는 존재하지 않음).
6. **작업 추적** — `TaskCreate` 로 작업 등록, `TaskUpdate` 로 owner·blockedBy 설정, `TaskList`/`TaskGet` 으로 모니터.
7. **팀원 실행** — 자기 worktree 안에서 구현 → dev 서버 검증 → 커밋 → push → PR → `SendMessage` 로 PR URL 보고 + `TaskUpdate` 완료.
8. **통합 검증** — 팀원의 worktree 내 검증만으로는 부족. 머지 후 main 기준으로 dev 서버를 띄워 충돌·콘솔 에러 0·시각 회귀 없음을 확인.
9. **순차 머지** — 순서: 파일 겹침 0 인 독립 PR → 기반/하부 PR → 충돌 가능성 높은 PR(마지막). 사전 점검은 각 브랜치의 `git diff --name-only origin/main origin/{branch}` 비교. 머지마다 GitHub mergeable 재계산을 기다리고, conflict 나면 해당 worktree 에서 rebase + `--force-with-lease`. 사전 분석에서 놓친 충돌은 매니저가 직접 해결한다.
10. **정리** — 아래 "정리". 머지 전에 팀원을 내려야 하면 `SendMessage` 로 shutdown_request. 팀 자체는 세션 종료 시 자동 정리.

## 팀원 프롬프트 템플릿

```
너는 {프로젝트명} 의 {작업명} 담당이야.
다른 팀원 N명이 별도 worktree 에서 동시 작업 중이므로 너의 worktree 안에서만 작업해.

# 워크트리
- 경로: {절대 경로}
- 브랜치: {브랜치명} (origin/main 기반)
- 의존성 폴더는 main 으로 링크됨 — npm install / pip install 금지
- dev 서버 포트: {N}

# 배경
{기존 PR / 토큰 시스템 / 컴포넌트 등 필요한 컨텍스트}

# 작업
{구체적 변경 명세}

# 작업 규칙
{시각 동등성 / 위험 영역 / 금지 사항}

# 검증
포트 {N} 으로 dev 서버 기동 → 200 응답 확인 → compile 성공·콘솔 에러 확인 → 가능하면 Playwright 로 시각 확인 → dev 서버 종료

# 커밋 + PR
한국어 conventional commit (attribution 은 하네스 규칙), gh pr create 까지 자율 진행.

# 보고
PR URL + 변경 요약 + 위험 영역 + 검증 결과, 한국어 250단어 이내

# 금지
- worktree 외부 파일 수정, 다른 worktree 접근
- npm install / package.json 수정
- {작업별 추가 금지사항}
```

## Windows 특이사항

- 프로젝트 dev 서버 스크립트가 사이드 worktree 경로를 인식 못 하면 그 worktree 에서 포트를 지정해 직접 기동한다.
- 한글 프롬프트/커밋 메시지는 파이프를 거치지 말고 파일로 작성 (인코딩 깨짐).
- Playwright MCP 가 다른 작업에 점유돼 있으면 강제 종료하지 말고(사용자 승인 필요) `npx playwright` CLI 를 쓴다.

## 정리

1. 팀 포트(8081~)의 LISTENING dev 서버 PID 종료.
2. worktree 제거: 매니저 셸/세션 cwd 를 그 worktree 밖으로 옮긴 뒤, **링크부터 뗀다** (Windows junction 은 `cmd /c rmdir <path>`, symlink 는 `rm <link>` — 재귀 삭제 금지). 링크가 남지 않았는지 확인한 다음 `git worktree remove <path>`. 프로젝트에 worktree 정리 스크립트가 있으면 그것을 쓴다.
   - 링크를 떼지 않은 채 `git worktree remove --force` / `rm -rf` 금지 — junction 을 따라 들어가 main 의 node_modules·.venv 를 지운다.
3. 로컬 브랜치 삭제 (`git branch -D ...`), `git pull origin main --ff-only`.

*Related*: `multi-hypothesis` (분석용 Team 패턴)
*Last modified*: 2026-10-06 (frontier 모델용 축약)
