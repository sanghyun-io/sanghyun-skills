# Frontmatter 작성 가이드

`description`은 Claude가 skill 호출 여부를 판단하는 유일한 입력이다. 부실하면 트리거되지 않는다.

```yaml
---
name: kebab-case-name    # 디렉토리명과 동일, 영문 소문자 + 하이픈
description: |
  {1-2문장: 무엇을 하는지}
  Use when the user mentions {한국어 키워드}, {영어 키워드}, or {특정 상황}.
---
```

## 나쁜 예 / 좋은 예

- `description: Writes resumes.` — 트리거 조건 없음.
- `description: 이력서를 작성하는 도구입니다.` — 한국어만, 키워드 없음.
- `This skill helps you write resumes when needed.` — "when needed"는 트리거 조건이 아님.

```yaml
description: |
  채용 공고 URL과 사용자 프로필을 입력받아 맞춤형 이력서/자기소개서 초안을 작성한다.
  ATS 친화 포맷·STAR 기법·키워드 매칭을 자동 적용.
  Use when the user mentions 이력서, 자소서, 자기소개서, 지원서, resume, cover letter, CV,
  채용 공고 URL을 공유하면서 문서 작성을 요청할 때, or asks to tailor a resume/cover letter
  for a specific job posting.
```

## 키워드 원칙

- 한/영 양쪽, 동의어 전부(이력서/자소서/자기소개서/지원서), 동사도 포함("리뷰해", "review").
- 약간 pushy하게 — 명시적 요청이 없어도 키워드가 나오면 발동하도록.
- 오발동 우려가 있으면 비-트리거 조건 추가: `Do NOT trigger when ...`.
- 다중 조건은 `Use when:` 아래 bullet(키워드 / 동작 / 파일 패턴)로 나열해도 된다.

## 체크리스트

- `name` kebab-case + 디렉토리명 일치
- 무엇 + 언제 둘 다 포함, "Use when ..." 문장 존재
- 한/영 키워드 + 동의어
- 길이 대략 80~600자
