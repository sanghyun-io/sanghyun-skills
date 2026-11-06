---
name: skill-scaffolder
description: |
  Claude Code skill을 새로 만들거나 기존 skill을 리팩토링할 때 이 컨벤션을 적용한다.
  Anthropic 공식 skill-creator + google/skills 베스트 프랙티스 기반. SKILL.md frontmatter, progressive disclosure(references/), 트리거 문장 작성, 디렉토리 구조 검증을 다룬다.
  Use when the user mentions '스킬 만들기', '스킬 작성', '스킬 생성', 'SKILL.md', '커스텀 스킬', '스킬 구조 정리', '스킬 리팩토링', 'skill 스캐폴딩', 'new skill', 'create skill', 'scaffold skill', 'restructure skill', or asks to design/refactor a skill directory. 새 skill 디렉토리 생성 또는 기존 SKILL.md 편집이 감지되면 트리거한다.
---

# Skill Scaffolder

skill 생성·리팩토링용 메타 스킬. Anthropic `skill-creator` + google/skills 컨벤션을 Claude Code 환경(user `~/.claude/skills/`, project `.claude/skills/`)에 맞춘 것.

## 구조

```
skill-name/
├── SKILL.md      # 필수, < 500줄
├── references/   # 토픽별 분리, lazy-load
├── scripts/      # 실행 스크립트 (필요할 때만)
└── assets/       # 템플릿·이미지·예시 (필요할 때만)
```

## 규칙

- `name`: kebab-case, 디렉토리명과 동일.
- `description`: **무엇을 하는지 + 언제 트리거되는지**. "Use when ..." 문장 + 한/영 트리거 키워드(동의어 포함). 필요하면 비-트리거 조건도. 상세는 [references/frontmatter.md](references/frontmatter.md).
- 분할 기준: SKILL.md 300줄 초과 또는 본문 코드 샘플 5개 초과 → `references/{topic}.md` 로 분리(필수). 토픽 3개 이상이면 분리 권장. 500줄은 hard limit.
- 같은 도메인 skill끼리 references 파일명 통일 (예: SaaS 도메인은 `core-concepts.md / api-usage.md / deployment.md`).
- Body 순서: 한 줄 정의 → 핵심 규칙(DO/DO NOT) → 빠른 시작(가장 흔한 호출 1개) → 워크플로우 개요 → References 목차.
- SKILL.md 끝 References 목차는 각 파일을 **언제 읽어야 하는지** 명시:
  `- **{Topic}**: {요약 + 언제 읽는지}. See [references/{file}.md](references/{file}.md)`

## 작업 흐름

1. 의도·트리거 키워드·출력 형식, 이름, 위치(user `~/.claude/skills/` vs project `.claude/skills/`)를 대화 맥락에서 파악한다. **정말 모호할 때만** AskUserQuestion으로 묻고, 아니면 기존 컨벤션(기본: user level)을 따른 뒤 결정 내용을 보고한다.
2. 디렉토리 생성 (`references/`만 기본, `scripts/`·`assets/`는 실제로 필요할 때).
3. frontmatter 먼저 → body 작성. 분할 기준에 걸리면 즉시 references/ 로.
4. 완료 보고에 기대 트리거 샘플 발화 2~3개를 함께 적어 사용자가 누락을 지적할 수 있게 한다.

기존 skill 리팩토링은 [references/refactoring.md](references/refactoring.md).

## References

- **Frontmatter**: description 좋은/나쁜 예, 트리거 문장 패턴, 검증 체크리스트. 새 skill 작성 시 먼저 읽기. See [references/frontmatter.md](references/frontmatter.md)
- **워크플로우**: 단계별 스캐폴딩 세부(분할 판단, 흔한 실수). 실제 스캐폴딩 진행 시. See [references/workflow.md](references/workflow.md)
- **리팩토링**: 진단 기준 + 단일 SKILL.md → references/ 분할 절차. 기존 skill 손볼 때. See [references/refactoring.md](references/refactoring.md)
