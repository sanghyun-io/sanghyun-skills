# Frontmatter Writing Guide

`description` is the only input Claude uses to decide whether to invoke a skill. If it is weak, the skill will not trigger.

```yaml
---
name: kebab-case-name    # same as directory name, lowercase letters + hyphens
description: |
  {1-2 sentences: what it does}
  Use when the user mentions {Korean keywords}, {English keywords}, or {specific situation}.
---
```

## Bad / good examples

- `description: Writes resumes.` — no trigger condition.
- `description: 이력서를 작성하는 도구입니다.` ("A tool that writes resumes.") — Korean only, no keywords.
- `This skill helps you write resumes when needed.` — "when needed" is not a trigger condition.

```yaml
description: |
  Takes a job posting URL and the user's profile and drafts a tailored resume/cover letter.
  Automatically applies ATS-friendly format, the STAR method, and keyword matching.
  Use when the user mentions 이력서, 자소서, 자기소개서, 지원서, resume, cover letter, CV,
  shares a job posting URL and asks for a document, or asks to tailor a resume/cover letter
  for a specific job posting.
```

## Keyword principles

- Both Korean and English, every synonym (이력서/자소서/자기소개서/지원서), and verbs too ("리뷰해", "review").
- Be slightly pushy — trigger whenever keywords appear, even without an explicit request.
- If misfires are a risk, add non-trigger conditions: `Do NOT trigger when ...`.
- Multiple conditions may be listed as bullets under `Use when:` (keywords / actions / file patterns).

## Checklist

- `name` kebab-case + matches directory name
- Includes both what + when; a "Use when ..." sentence exists
- Korean/English keywords + synonyms
- Length roughly 80-600 characters
