---
name: slack-thread-to-plan
description: |
  Takes a Slack thread permalink URL, reads the whole thread (parent + all replies) via the conversations.replies API,
  analyzes the requirements, and saves a work plan for applying them to the current project as a Plan file (same layout plan-subdivider uses).
  Use when the user mentions 슬랙 스레드, 슬랙 대화, Slack 스레드, Slack thread, 슬랙 요구사항, 스레드 분석,
  or shares a Slack link asking "이거 분석해줘 / 요구사항 정리해줘 / 작업 계획 세워줘" (analyze this / organize requirements / make a work plan),
  or shares a slack.com/archives/... permalink and asks to analyze it, extract requirements, or build a work plan.
  Do NOT trigger for general Slack API questions with no thread URL and no intent to plan.
---

# Slack Thread → Plan

Flow: Slack URL → fetch thread → analyze requirements → project application plan → work plan → save Plan file → ask next action.

Deliverable is **analysis + plan only**. Do not touch code until the user picks "Start implementing now" in Step 7.

Principles:
- Never invent requirements not in the source. Resolve ambiguity/conflicts with AskUserQuestion.
- Do not dump the raw thread; give key quotes + summary.
- Never print/log/echo the token value.
- Overwrite a Plan file only after user confirmation.

## Prerequisites

- Env var `SLACK_USER_TOKEN` (xoxp-). Scopes: `channels:history` `groups:history` `im:history` `mpim:history` `users:read`
- The token owner must be a member of the channel (including private/DM)
- The variable must be visible to the shell Claude runs commands in (shell profile, or `env` in Claude Code settings). If missing, see [troubleshooting](references/troubleshooting.md); never ask the user to paste the token into chat.

## Fetch

Windows (PowerShell):

```powershell
$env:PYTHONIOENCODING="utf-8"; python "${CLAUDE_SKILL_DIR}/scripts/fetch_thread.py" "<SLACK_PERMALINK_URL>"
```

macOS/Linux: `PYTHONIOENCODING=utf-8 python "${CLAUDE_SKILL_DIR}/scripts/fetch_thread.py" "<SLACK_PERMALINK_URL>"`

- Keep `PYTHONIOENCODING=utf-8`: on a non-UTF-8 console (e.g. Windows cp949) the script otherwise exits with `UnicodeEncodeError` on non-ASCII text. Tool shells may reset env per call, so prefix it every time.
- Output: cleaned markdown (author name, time, body, attachments, reactions; mentions replaced with names). Raw JSON with `--json`.
- Image attachments are metadata only by default. If content is needed, use `--download-files [--files-dir <DIR>]` (default `./slack-files`), then Read them.
- Quote the URL (query contains `&`). `?thread_ts=` in a reply permalink is automatically resolved to the parent.

## Workflow

1. **Get URL** — ask if missing. Format `https://<workspace>.slack.com/archives/<CHANNEL>/p<digits>`.
2. **Fetch** — if exit code ≠ 0, stop and report ([troubleshooting](references/troubleshooting.md)).
3. **Analyze requirements** — per the [analysis-framework](references/analysis-framework.md) checklist. Ambiguities via AskUserQuestion.
4. **Application plan** — read the project's `CLAUDE.md`, `docs/CHECKPOINT.md`, `docs/WORK_QUEUE.md` (if present) and map each requirement to files/modules/layers. If it conflicts with an existing decision, state it and ask for a decision.
5. **Work plan** — ordered tasks (with dependencies and verification method). Print a summary in chat first.
6. **Save Plan** — after user confirmation, to `~/.claude/plans/{plan-name}.md`. Format/split rules in [plan-output](references/plan-output.md). For multi-file changes, if a plan-review command is available, ask via AskUserQuestion whether to run it (never skip on your own).
7. **Ask next action (required, skill exit point)** — via AskUserQuestion, not plain text. Labels/descriptions in plain text only, no emoji or decorative characters. Add/remove options as fits:
   - Start implementing now (Recommended) — create a branch or worktree the way the project prefers → read code → implement
   - Stop here — one line with the Plan path
   - Create GitHub Issue — Plan summary as an Issue (`gh issue create`)
   - Add to WORK_QUEUE — insert into the `docs/WORK_QUEUE.md` pending queue

   Do not touch code for any choice other than "Start implementing now".

## References

- [slack-api.md](references/slack-api.md) — permalink parsing, APIs used, text cleanup, exit codes. When understanding/modifying the script.
- [analysis-framework.md](references/analysis-framework.md) — extraction checklist + chat output template. Steps 3-5.
- [plan-output.md](references/plan-output.md) — Plan file path/format/task breakdown. Step 6.
- [troubleshooting.md](references/troubleshooting.md) — handling per exit code, scope/token/garbled Korean. When fetch fails.
