# Refactoring an Existing Skill

## Diagnosis (refactor if any applies)

- SKILL.md over 300 lines (create references/ if missing)
- description < 80 characters, keywords in only one of Korean/English, no "Use when ..."
- more than 5 code samples in the body, or more than 3 topics

## Procedure

1. Group sections by topic — based on the user's real invocation situations (what info is needed when). E.g. concepts → `core-concepts.md`, API → `api-usage.md`, examples → `examples.md`, troubleshooting → `troubleshooting.md`; keep the core workflow in SKILL.md.
2. Move each topic to `references/{topic}.md` (original content as is, not summarized). Add a one-line "This file covers ..." at the top; update internal anchor links to the new paths.
3. Leave only frontmatter, core rules, quick start, workflow overview, and References index in SKILL.md (do not leave an empty shell of just links).
4. If the description is weak, strengthen it using the [frontmatter.md](frontmatter.md) patterns.

## Verification

- SKILL.md < 300 lines
- Every references file is linked from the SKILL.md index
- references file names consistent with other skills in the same domain
