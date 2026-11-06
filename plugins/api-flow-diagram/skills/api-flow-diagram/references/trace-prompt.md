# Call tracing prompt

Following FE·BE code screen by screen to the end reads many files. If your agent can start sub-agents, hand this to one and keep only verification and rendering in the main session (Claude Code: `Agent` with `subagent_type: "general-purpose"` and a fast or balanced model from those available; other agents: their sub-agent or task feature). If not, follow the same prompt yourself as a checklist. Fill in the following.

```text
Read-only investigation. No code edits, commits, running servers, DB access, or opening .env.

Goal: list every API called in {flow name}, exhaustively, per screen/button.
The result is used to draw a left-to-right flow diagram (branch arrows, endpoints marked on each screen/button).

Targets
- Frontend: {FE repo path}. Entry point {route/URL/component}. {known step names}.
  Trace each step's component, store actions, and HTTP client calls to the end.
  Include entry guards, branches by response code, confirm/cancel modals, external SDK callbacks, and navigation after completion.
  If there are multiple HTTP client instances, note differences in headers/interceptors (401 handling, etc.).
- Backend: {BE repo path} (commit {sha}). For each endpoint: file:line, auth requirement
  (before_request, decorators, internal current_user checks, etc.), main behavior in 1 line.
  {Specific concerns: e.g. where 401/403 can occur in the logged-out flow}

Output (in the user's language): markdown summary + one JSON block at the very end.
The JSON follows this schema exactly:
{paste the top-level, node, call, edges example blocks from data-schema.md}

Rules
- cols follow screen progression order (left→right). Steps with many branches get a separate "branches" column.
- edges are based on actual code conditions. label ~20 chars; detailed conditions go in node.desc.
- Auth not confirmed in code: auth.level "unknown". Guesses get "(guess)" in note.
- Callbacks invoked by external servers (webhooks, etc.) are also calls: m is "EXT" or the actual method, and fe says "external server".
```

## After tracing

1. Open the file:line for the 2–3 claims that decide the conclusion (auth conditions, failure points, branch conditions) and verify directly. Do not copy a sub-agent's report as-is.
2. Save the JSON block as `tmp-debug/<name>-flow.json`. Convert field names that differ from the schema (e.g. `auth: "none"` as a string).
3. Reflect fixes made during verification and anything not verified in `risks`.
