---
name: api-flow-diagram
description: |
  Traces a user flow (signup, application, payment, onboarding, etc.) end to end through FE and BE code and produces a left-to-right flow diagram HTML showing which API each screen/button calls. One file holds branch arrows (forward/error/back), FE·BE file:line per endpoint, auth requirements, risk points, and a full endpoint table.
  Use when the user wants the API calls of a user journey traced and drawn: API 흐름도, API 호출 흐름 도식, 화면별 API, 버튼별 엔드포인트, 어떤 API 가 호출되는지 정리, API 호출 점검, user flow API map, endpoint flow diagram, API call flow chart, or asks to trace every API called during a user journey (FE+BE).
  Do NOT trigger for generic flowcharts or sequence diagrams unrelated to API calls, DB ERDs, infra architecture diagrams, or a single endpoint question.
---

# API Flow Diagram

Trace one user flow's screens/buttons → API calls → branches in code, and build the flow diagram HTML from a single data JSON. The drawing code is fixed (`assets/template.html`); only the data changes each time.

Works with any coding agent (Claude Code, Codex, others). All paths below are relative to **this skill's folder** (the directory containing this SKILL.md; Claude Code exposes it as `${CLAUDE_SKILL_DIR}`). The only runtime dependency is Python 3.9+.

## Rules

- DO: if your agent can start sub-agents, delegate tracing to one with [trace-prompt](references/trace-prompt.md); otherwise trace yourself using the same prompt as a checklist. Either way, verify 2–3 key claims at file:line yourself before drawing.
- DO: tracing is mostly reading and searching code, so give it a fast or balanced model; keep verification and the final conclusions on the strongest model you have. Pick from the models this agent actually offers (rough tiers: fast/cheap = Haiku-, mini-, flash-class; balanced = Sonnet-class; strongest = Opus-class or top reasoning models); don't assume a name.
- DO: record the base commit (deployed sha) in `meta`. Auth and branches change per commit.
- DO: auth not confirmed in code → `auth.level: "unknown"`. Guesses get "(guess)" in note.
- DO: output as local files in a git-ignored temp folder of the project (e.g. `tmp-debug/`).
- DO NOT: hand-write HTML/SVG. Change only the data and run `render.py`. Fix layout problems in the template.
- DO NOT: publish the HTML to any external sharing service or hosted page (only when the user asks directly).
- DO NOT: open `.env` or the DB to check. If needed, leave it in risks as "not verified".

## Quick start

```bash
S="<this skill's folder>"     # Claude Code: ${CLAUDE_SKILL_DIR}
PYTHONIOENCODING=utf-8 python "$S/scripts/render.py" tmp-debug/<name>-flow.json tmp-debug/<name>-flow.html
```

Try with example data: `python "$S/scripts/render.py" "$S/assets/example-shop.json" tmp-debug/example.html`.
Script self-check: `python "$S/scripts/render.py" --self-test`. Use `python3` where `python` is not Python 3.

## Workflow

1. **Scope**: flow name, entry point (URL/route), FE repo, BE repo and base commit, specific concerns (e.g. 401 when logged out). Ask only if missing from the conversation.
2. **Trace**: fill [trace-prompt](references/trace-prompt.md) and give it to a sub-agent, or follow it yourself. Output is JSON in [data-schema](references/data-schema.md) format.
3. **Verify**: open and check the claims that decide the conclusion (failure points, auth conditions). Fix the data if wrong.
4. **Render**: save JSON to `tmp-debug/<name>-flow.json` and run `render.py`. On validation errors, fix the data and rerun.
5. **Visual check** (if you have a browser tool): many automation tools block `file:`, so serve `tmp-debug/` with `python -m http.server <port> --bind 127.0.0.1` and screenshot at a wide viewport (3000px+). If labels cover nodes or arrows tangle, split nodes or columns. Stop the server when done. Without a browser tool, tell the user to open the HTML and say the layout was not checked.
6. **Report**: HTML path, column/call/arrow counts, and separate what you verified directly from what relies only on a sub-agent's report.

## References

- **Data schema**: top-level/column/node/call/edge fields, allowed values, label length and branch count guidance, render.py checks. When creating or fixing the JSON. See [references/data-schema.md](references/data-schema.md)
- **Trace prompt**: prompt template for a sub-agent (or your own checklist) and what to do after tracing. In step 2. See [references/trace-prompt.md](references/trace-prompt.md)
- **Example data**: fictional shop signup + first order flow (5 cols/7 calls/13 arrows). To get a feel for splitting columns and shortening labels. See [assets/example-shop.json](assets/example-shop.json)
