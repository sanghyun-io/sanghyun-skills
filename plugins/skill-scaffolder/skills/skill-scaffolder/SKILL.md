---
name: skill-scaffolder
description: |
  Applies this convention when creating a new Claude Code skill or refactoring an existing one.
  Based on Anthropic's official skill-creator + google/skills best practices. Covers SKILL.md frontmatter, progressive disclosure (references/), trigger sentence writing, and directory structure validation.
  Use when the user mentions '스킬 만들기', '스킬 작성', '스킬 생성', 'SKILL.md', '커스텀 스킬', '스킬 구조 정리', '스킬 리팩토링', 'skill 스캐폴딩', 'new skill', 'create skill', 'scaffold skill', 'restructure skill', or asks to design/refactor a skill directory. Also triggers when creating a new skill directory or editing an existing SKILL.md is detected.
---

# Skill Scaffolder

Meta skill for creating and refactoring skills. Adapts Anthropic `skill-creator` + google/skills conventions to the Claude Code environment (user `~/.claude/skills/`, project `.claude/skills/`).

## Structure

```
skill-name/
├── SKILL.md      # required, < 500 lines
├── references/   # split by topic, lazy-load
├── scripts/      # executable scripts (only when needed)
└── assets/       # templates, images, examples (only when needed)
```

## Rules

- `name`: kebab-case, same as the directory name.
- `description`: **what it does + when it triggers**. A "Use when ..." sentence + Korean/English trigger keywords (including synonyms). Add non-trigger conditions if needed. Details in [references/frontmatter.md](references/frontmatter.md).
- Split criteria: SKILL.md over 300 lines or more than 5 code samples in the body → split into `references/{topic}.md` (required). 3+ topics → splitting recommended. 500 lines is the hard limit.
- Skills in the same domain use the same references file names (e.g. SaaS domain: `core-concepts.md / api-usage.md / deployment.md`).
- Body order: one-line definition → core rules (DO/DO NOT) → quick start (the single most common invocation) → workflow overview → References index.
- The References index at the end of SKILL.md states **when to read** each file:
  `- **{Topic}**: {summary + when to read}. See [references/{file}.md](references/{file}.md)`

## Workflow

1. Infer intent, trigger keywords, output format, name, and location (user `~/.claude/skills/` vs project `.claude/skills/`) from conversation context. Ask via AskUserQuestion **only when truly ambiguous**; otherwise follow existing convention (default: user level) and report the decision.
2. Create directories (`references/` only by default; `scripts/`/`assets/` only when actually needed).
3. Frontmatter first → then body. If a split criterion is hit, move to references/ immediately.
4. In the completion report, list 2-3 expected trigger sample utterances so the user can point out gaps.

For refactoring an existing skill, see [references/refactoring.md](references/refactoring.md).

## References

- **Frontmatter**: good/bad description examples, trigger sentence patterns, validation checklist. Read first when writing a new skill. See [references/frontmatter.md](references/frontmatter.md)
- **Workflow**: step-by-step scaffolding details (split decisions, common mistakes). When actually scaffolding. See [references/workflow.md](references/workflow.md)
- **Refactoring**: diagnostic criteria + procedure for splitting a single SKILL.md into references/. When reworking an existing skill. See [references/refactoring.md](references/refactoring.md)
