# Plan Output

This document is the reference for the Plan file format.

## Path / naming

- Main Plan: `~/.claude/plans/{plan-name}.md` (`{plan-name}` = thread topic in kebab-case, e.g. `slack-pdf-margin-fix`)
- When splitting tasks: `~/.claude/plans/{plan-name}/{2-digit-seq}-{kebab}.md` (e.g. `01-fetch-thread.md`)
- Absolute paths only — relative paths fail permission matching and trigger an approval prompt every time.
- If the name exists, say so and propose a new name. Overwrite only after confirmation.
- With fewer than 3 tasks, you may skip splitting and keep everything in the main file.

## Main Plan structure

```markdown
# {plan title}

> **Created**: YYYY-MM-DD
> **Purpose**: {one-line purpose}
> **Source**: Slack thread — {channel name} ({permalink})

## Implementation Tasks

| Order | Task Name | File | Description |
|:-----:|-----------|------|-------------|
| 1 | **Task 1** | [01-...](./plan-name/01-....md) | ... |

### Task Rules
1. Execute sequentially
2. Finish each task's checklist before the next
3. Run verification commands on completion

## Requirements (from thread)
{requirements table from analysis, as is, with quoted evidence}

## Project Application Plan
{location/approach table}

## Core Content
{work plan body}
```

## Task file structure

```markdown
# Task {n}: {name}

> **Order**: {n}/{total}
> **Previous task**: [...] or (none)
> **Next task**: [...] or (none)

## Objective
## Checklist
- [ ] {concrete, verifiable item}
## Completion Criteria
1. Checklist complete
2. Build/tests pass (if applicable)
## Verification Commands
## Next Task
[Task {n+1}: ...](./{file})
```

Each task is a unit that can be completed and verified on its own; split along dependency order and file/layer boundaries.

## Right after saving

For multi-file changes, if a plan-review command is available, confirm via AskUserQuestion whether to run it. Never skip on your own (e.g. "already detailed enough"); skip only if the user explicitly says so. Then go to SKILL.md Step 7.
