# Slack API Reference (`scripts/fetch_thread.py`)

## Permalink parsing

```
https://<workspace>.slack.com/archives/<CHANNEL>/p<DIGITS>[?thread_ts=<TS>&cid=<CHANNEL>]
```

- `<CHANNEL>`: `C..` public / `G..` private / `D..` DM. If `?cid=` exists, it takes precedence.
- `p<DIGITS>` → ts: insert a decimal point before the last 6 digits (`p1700000000123456` → `1700000000.123456`).
- If `?thread_ts=` (reply permalink) exists, the whole thread is fetched from that parent ts.

## APIs used (Bearer `SLACK_USER_TOKEN`)

- `conversations.replies` (`channel`, `ts`=parent, cursor pagination) — `*:history` scope. messages[0] is the parent, the rest are replies in time order.
- `users.info` — `users:read`. Name priority `profile.display_name` → `profile.real_name` → `real_name` → `name`. On failure, falls back to user ID (flow continues).
- `conversations.info` — for channel name display (`channels:read`/`groups:read`). DM shows `(DM)`; no permission shows the ID.
- `ratelimited` is retried by the script with backoff.

## Text cleanup (clean_text)

`<@U..>` → `@name`, `<#C..|name>` → `#name`, `<url|label>` → `label (url)`, `<!here>`/`<!channel>` → `@here`/`@channel`, `<!subteam^S..|@team>` → `@team`, HTML entities decoded.

## Exit codes

0 success / 2 argument error / 3 `SLACK_USER_TOKEN` not set / 4 URL parse failure / 5 Slack API error. Handling in [troubleshooting.md](troubleshooting.md).
