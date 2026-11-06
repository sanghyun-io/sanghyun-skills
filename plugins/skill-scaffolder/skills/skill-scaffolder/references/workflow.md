# Skill 스캐폴딩 워크플로우

1. **의도·트리거·출력 형식 파악** — 대화에서 이미 드러나면 그대로 진행. 정말 모호할 때만 AskUserQuestion (질문 필드에 이모지·장식 문자 금지 — CLAUDE.md 5.1).
2. **이름·위치** — kebab-case 이름 제안. 위치 기본은 user level `~/.claude/skills/{name}/`(모든 프로젝트 공유); 특정 프로젝트 전용이 분명하면 `{project}/.claude/skills/{name}/`.
3. **디렉토리** — `mkdir -p ~/.claude/skills/{name}/references`. `scripts/`·`assets/`는 실제로 필요할 때만.
4. **SKILL.md** — frontmatter 먼저([frontmatter.md](frontmatter.md)), body는 SKILL.md "규칙"의 순서를 따른다.
5. **분할 판단** — SKILL.md 300줄 초과 조짐, 한 섹션 코드 샘플 80줄 초과, 토픽 3개 이상 중 하나라도 해당하면 references/로 분리.
6. **보고** — 생성 경로, 기대 트리거 샘플 발화 2~3개. 새 skill은 다음 세션부터 자동 로드되며, 현재 세션에서 바로 테스트하려면 트리거 키워드가 든 발화를 시도하라고 안내.

## 흔한 실수

- description 한 줄로 끝냄 / 트리거 키워드 누락
- name이 CamelCase이거나 디렉토리명과 불일치
- 300줄 넘는 단일 SKILL.md, 본문에 코드 샘플 5개 이상
