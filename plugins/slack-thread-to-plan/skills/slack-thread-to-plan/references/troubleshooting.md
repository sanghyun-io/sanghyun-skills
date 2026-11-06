# Troubleshooting

On failure, stop and report to the user. Do not continue with guessed retries.

## By exit code

- **2 argument error** — check the URL is quoted (a query with `&` gets cut by the shell). A missing path after `--files-dir` is also 2.
- **3 token not set** — the variable isn't visible to this shell (e.g. exported only in `~/.bashrc` while commands run in PowerShell). Ask the user to set `SLACK_USER_TOKEN` themselves (shell profile, OS environment, or `env` in Claude Code settings) and restart the session if needed. Never ask them to paste the token into chat (it stays in the session log), and never print or echo it.
- **4 URL parse failure** — must be a message permalink ("Copy link"), not a channel link or short URL.
- **5 Slack API error** — `error` in stderr:
  - `not_in_channel` / `channel_not_found` → token account is not a channel member. Join, then retry
  - `missing_scope` → token must be reissued (scopes below)
  - `invalid_auth` / `token_revoked` → issue a new token and update the env var
  - `thread_not_found` → ts is not a parent. Check for `?thread_ts=`
  - `ratelimited` → retried automatically. If it persists, try again later

## Scopes

- `channels:history` / `groups:history` / `im:history` / `mpim:history` — public / private / DM / group DM respectively. Missing → fetch fails (code 5).
- `users:read`, `channels:read`/`groups:read` — works without them, showing IDs instead of names.

## Exit 0 but 0 messages

Empty thread or a permission boundary. A private channel with only public scopes can return ok=true + empty array → recheck scopes.

## Garbled Korean

If output is still garbled through a pipe even with `PYTHONIOENCODING=utf-8`, redirect output to the current project's `tmp-debug/` (`> tmp-debug\slack-thread.md`) and Read it.
