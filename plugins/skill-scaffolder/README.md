# skill-scaffolder

Scaffold or refactor Claude Code skills with a consistent structure.

Applies a skill layout based on Anthropic's skill-creator guidance: a short `SKILL.md` (under 500 lines) with a trigger-rich `description` (what it does plus "Use when ..." with Korean and English keywords), topic files in `references/` loaded on demand, and `scripts/` and `assets/` only when needed. For existing skills it diagnoses length and topic sprawl and splits them into references.

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install skill-scaffolder@sanghyun-skills
```

## Usage

Ask to create, scaffold, or restructure a skill, or edit a `SKILL.md`.

Example prompts:
- "새 스킬 만들어줘"
- "refactor this SKILL.md into references"

## Requirements

None.

## License

MIT
