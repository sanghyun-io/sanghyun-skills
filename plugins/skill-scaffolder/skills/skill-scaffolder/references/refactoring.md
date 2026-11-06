# 기존 Skill 리팩토링

## 진단 (하나라도 해당하면 리팩토링)

- SKILL.md 300줄 초과 (references/ 없으면 생성)
- description < 80자, 한/영 중 한쪽 키워드만, "Use when ..." 없음
- 본문 코드 샘플 5개 초과 또는 토픽 3개 초과

## 절차

1. 섹션을 토픽 단위로 분류 — 사용자의 실제 호출 상황(언제 어떤 정보가 필요한지) 기준. 예: 개념 → `core-concepts.md`, API → `api-usage.md`, 예제 → `examples.md`, 트러블슈팅 → `troubleshooting.md`, 핵심 워크플로우는 SKILL.md에 유지.
2. 각 토픽을 `references/{topic}.md` 로 이동(원본 내용 그대로, 요약하지 않음). 파일 상단에 "이 파일은 ~를 다룬다" 한 줄, 내부 앵커 링크는 새 경로로 갱신.
3. SKILL.md에는 frontmatter, 핵심 규칙, 빠른 시작, 워크플로우 개요, References 목차만 남긴다 (링크만 남은 빈 껍데기가 되지 않게).
4. description이 부실하면 [frontmatter.md](frontmatter.md) 패턴으로 보강.

## 검증

- SKILL.md < 300줄
- 모든 references 파일이 SKILL.md 목차에서 링크됨
- 같은 도메인 다른 skill과 references 파일명 일관
