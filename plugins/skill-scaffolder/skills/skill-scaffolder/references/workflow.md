# Skill Scaffolding Workflow

1. **Intent, triggers, output format** — if already clear from the conversation, proceed. Use AskUserQuestion only when truly ambiguous (no emoji or decorative characters in question fields — CLAUDE.md 5.1).
2. **Name, location** — propose a kebab-case name. Default location is user level `~/.claude/skills/{name}/` (shared across all projects); if clearly specific to one project, `{project}/.claude/skills/{name}/`.
3. **Directory** — `mkdir -p ~/.claude/skills/{name}/references`. `scripts/`/`assets/` only when actually needed.
4. **SKILL.md** — frontmatter first ([frontmatter.md](frontmatter.md)); body follows the order in SKILL.md "Rules".
5. **Split decision** — if any applies: SKILL.md likely to exceed 300 lines, a code sample over 80 lines in one section, or 3+ topics → split into references/.
6. **Report** — created path, 2-3 expected trigger sample utterances. Tell the user a new skill auto-loads from the next session; to test in the current session, try an utterance containing a trigger keyword.

## Common mistakes

- description ends at one line / missing trigger keywords
- name is CamelCase or does not match the directory name
- single SKILL.md over 300 lines, 5+ code samples in the body
