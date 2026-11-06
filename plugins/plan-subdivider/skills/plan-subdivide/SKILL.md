---
name: plan-subdivide
description: |
  Splits a plan file into ordered task files (one per deliverable) with checklists, completion criteria, verification commands, and prev/next links, plus a table of contents in the main plan.
  Use when a plan with 3 or more tasks is about to be executed (e.g. right after plan mode, or when a saved plan in ~/.claude/plans/ is resumed), or when the user mentions subdivide, split the plan, break down into tasks, task files, 플랜 쪼개기, 계획 세분화, 태스크 파일로 나눠, 작업 단위로 나눠줘.
  Before implementing such a plan, ask the user (AskUserQuestion) whether to subdivide; do not skip that question on your own.
  Do NOT use for tasks finishable in a few minutes, single-file changes, or work too tightly coupled to split.
---

# Plan Subdivide

Break an existing plan into task files the user (or a later session) can execute one by one.

## Rules

- If in plan mode, run `ExitPlanMode` first: in plan mode a Write is treated as a new plan.
- Plan already in the conversation: use it, don't re-read or re-search.
- Confirm with AskUserQuestion, never plain text: once for the subdivision plan (Step 3), once for the next step (Step 5).
- After Step 3 approval, write every file in one message, in parallel. No per-file confirmation.
- If a git command fails, stop and report. Don't retry on your own.

## Steps

1. **Locate the plan**, first match wins: path argument → plan in the current context (prefer the one just created by ExitPlanMode) → newest `.md` in `~/.claude/plans/`. If `~/.claude/plans/{plan-name}/` already exists, warn and ask before overwriting.
2. **Analyze**: overall objective, tasks, dependencies/order, source section per task. Split by independent, verifiable deliverables in logical order; see [criteria](references/criteria.md).
3. **Confirm**: show a table (order / task / one-line description, source file, task count), then AskUserQuestion: `Proceed` (tip: Shift+Tab allows all writes at once) / `Needs revision` / `Cancel`.
4. **Write files**: `~/.claude/plans/{plan-name}/{NN}-{task-kebab}.md` per task, and prepend a task table to the main plan. Formats in [templates](references/templates.md).
5. **Report + next step**: list the created files, then AskUserQuestion: `Start first task` / `Review entire plan` / `Later`.
6. **Work environment** (only if `Start first task`): AskUserQuestion `Current environment` / `New branch` (`git switch -c feature/{plan-name}`) / `Git worktree` (`git worktree add ../{repo}-{plan-name} -b feature/{plan-name}`, then tell the user the path). Don't assume the current environment. Then open Task 01 and start.

Invoke directly: `/plan-subdivider:plan-subdivide [plan_path]`.

## References

- **Templates**: task file, main-plan table of contents, worked example. Read in Step 4. See [references/templates.md](references/templates.md)
- **Criteria**: when and how to split, naming, checklist quality. Read in Step 2. See [references/criteria.md](references/criteria.md)
