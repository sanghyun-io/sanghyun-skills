---
name: session-handoff
description: |
  Turns the current session's progress into a "handoff prompt" that a new session can pick up exactly where this one left off.
  Delivers in 3 priority tiers (try top-down, stop at the first success):
  (1) auto-copy the full handoff to the clipboard — Ctrl+V in the new session →
  (2) on failure, save to a file and give the path →
  (3) if tools are degraded and not working, print plain text inline.
  Goal: remove the chore of drag-copying a long handoff in fullscreen.
  Use when the user mentions 인계, 인계 프롬프트, 핸드오프, 핸드오버, 세션 이어가기, 세션 인계,
  이 세션 그대로 이어갈, 새 세션에서 이어서, handoff, hand-off, resume session, continue in a new session,
  session handoff prompt, or when the current session starts leaking raw tool-call syntax as plain text
  and the user wants to restart cleanly in a fresh session.
  Do NOT trigger for a general "요약해줘"/"summarize" request that is not about continuing work in a new session.
---

# Session Handoff

Write a handoff that lets a new session take over the current work without a gap. An argument can set the emphasis (e.g. `/session-handoff focus on debugging context`).

## Principles

- Write the body **from the current conversation context only**. Do not Read/Grep/Bash sources to fill it in — if unknown, write `(needs check)`. When this skill is needed, tools may be unstable; the new session does the checking.
- Do not summarize. If it's needed to continue, include it even if long.
- NEXT ACTION must be concrete down to file:line and commands. Environment state (worktree/branch/port/run commands) is mandatory (this user uses worktrees heavily).
- No code edits or commits. The only file written is the tier-2 handoff `.md`.

## Delivery (top-down, stop at first success — on failure, don't drag out retries; go straight to the next tier)

**1. Clipboard (top priority)** — On Windows, pipe the full text via a PowerShell single-quoted here-string (macOS/Linux: bash below):

```powershell
@'
<filled template>
'@ | Set-Clipboard
```

```bash
# macOS: pbcopy / Linux(Wayland): wl-copy / Linux(X11): xclip -selection clipboard
pbcopy <<'HANDOFF_EOF'
<filled template>
HANDOFF_EOF
```

- Report: "Copied the full handoff to the clipboard. In the new session, Ctrl+V then Enter." The clipboard is volatile, so you may add one line: "Save it to a file too?" (tier 2 if requested).
- A body line starting with `'@` breaks the here-string → put a space before it, or go to tier 2.

**2. File (if 1 fails)** — Write to `~/.claude/handoffs\<slug>.md` (slug = task topic in kebab-case, `handoff-latest` if unclear; same slug overwrites). Report: the path + a one-liner for the new session:
`Read the previous session's handoff file and continue as-is (start with "NEXT ACTION"): ~/.claude/handoffs\<slug>.md`

**3. Inline (tools degraded — calls leaking as plain text)** — Print the full text in a single code fence, followed by one line: "Paste the block above into a new session."

## Template (fill in this exact format)

```
[Session handoff — continuing from previous session]
Take over the context below as-is and continue the work. Start with "NEXT ACTION".

## 1. Goal / overview
- What is being done and why (one or two sentences)
- Final completion criteria (Done)

## 2. Environment
- Repository:
- Worktree path:
- Branch:
- Symlinks/ports/run commands needed to start:
- Related services/dependencies:

## 3. Done so far
- Files changed (path + gist):
- Key decisions / approach:
- Verified (test/build/run results):

## 4. Current state / where it stopped
- Exactly how far it got and where it stopped:

## 5. NEXT ACTION
- The concrete first action for the new session (down to file:line, commands):

## 6. Unresolved / blockers / open questions
- Undecided, blocked, or needing user confirmation:

## 7. Reference files & paths
- List relevant locations as file_path:line:

## 8. User constraints & preferences established this session
- Rules/preferences that must be followed (e.g. banned libraries, worktree rules):
```

## Reducing recurrence of degradation (reference)

Tool calls leaking as plain text is a model-level phenomenon at high context (`anthropics/claude-code#64108`, open; the harness is fail-closed, so leaked XML is not executed). Settings can't fully block it, only reduce frequency:
- `/clear` is most reliable — if tool calls leak twice in a row, produce a handoff and `/clear`. `/compact` is second-best (the compacted block itself can be a trigger).
- For long sessions use Fable/Sonnet instead of Opus (Opus is most vulnerable — it handles larger context and hits the threshold first; Fable has lower frequency).
- Read big files by line range, split big tasks into subagents. Slim down huge CLAUDE.md/rules.
