# session-handoff

Turn the current session into a prompt a fresh session can continue from.

When a session gets long or degraded, this skill writes a handoff prompt: goal, decisions made, current state, files touched, and the exact next step. It delivers it in the first way that works: copy to the clipboard, then save to `~/.claude/handoffs/<slug>.md`, then print inline as plain text.

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install session-handoff@sanghyun-skills
```

## Usage

Say "handoff", "인계 프롬프트 만들어줘", or "continue this in a new session". Paste the result into the new session.

Example prompts:
- "인계 프롬프트 만들어줘"
- "make a handoff so I can resume in a new session"

## Requirements

None. Clipboard copy uses `Set-Clipboard` on Windows, `pbcopy` on macOS, `wl-copy` or `xclip` on Linux; if none works it falls back to a file.

## License

MIT
