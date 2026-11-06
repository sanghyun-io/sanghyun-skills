---
name: multi-hypothesis
description: |
  RCA (Root Cause Analysis) method that digs deep into multiple cause hypotheses in parallel.
  Instead of settling on the first hypothesis, repeatedly ask "what if this isn't the cause?" and trace multiple hypotheses to the end simultaneously.
  TRIGGER: utterances like "원인 분석" (cause analysis), "근본 원인" (root cause), "왜 이렇게 됐는지" (why did this happen), "여러 가능성" (multiple possibilities), "다중 가설" (multiple hypotheses), "multi-hypothesis", "multiple working hypotheses", "root cause", "RCA".
  Structure: Opus manager + Sonnet teammates investigating in parallel + Codex delegation (via Sonnet). Spawn one general-purpose Agent per hypothesis in parallel (team forms automatically on first spawn; v2.1.178+).
invocation:
  command: multi-hypothesis
  user_invocable: true
  args:
    - name: symptom
      description: Symptom/observation/problem to analyze (if omitted, ask the user)
      required: false
---

# Multi-Hypothesis RCA

Basis: T.C. Chamberlin (1890), *The Method of Multiple Working Hypotheses*: don't get attached to the first hypothesis; keep several alive and trace them all to the end simultaneously. **Analysis-only skill: do not propose recovery/fixes** (RCA memory feedback).

## Procedure

1. **Fix the symptom** (Opus): extract the symptom from the utterance/args; if insufficient, AskUserQuestion.
2. **Derive hypotheses** (Opus): 3-5 hypotheses that are mutually independent, mutually exclusive, testable, falsifiable, and specific ("stale DNS cache", not "environment issue"). To avoid gaps, sweep each category once: code/logic (boundary conditions, off-by-one), state/data (migrations, cache), environment/config (env vars, permissions, dependency versions), concurrency/timing (race, deadlock, retry storm), infra/network (DNS, TLS, proxy, rate limit), human factors (recent changes, deploys, manual intervention), external dependencies (third-party APIs, monitoring blind spots).
3. **Approval**: present the hypothesis list to the user and get approval to proceed via AskUserQuestion.
4. **Parallel spawn** (Opus): spawn one `subagent_type: "general-purpose"` Agent per hypothesis **in parallel in one message**. The team forms automatically on the first spawn (`TeamCreate`/`TeamDelete` removed in v2.1.178).
   - No `explore`: it lacks `SendMessage` and cannot report.
   - If Agents from another task are active (check with `ListAgents`), prefix names with `mh-{N}` and give hypothesis Agents only this RCA's scope. If it's unclear whether to run concurrently, ask the user "run concurrently / wait".
5. **Investigate** (teammates): look for disconfirming evidence first, with no depth limit, until reaching a verifiable conclusion. If new sub-hypotheses emerge, recursively spawn additional `general-purpose` Agents. Delegate to Codex if needed (below).
6. **Report** (teammates): report to Opus via `SendMessage`.
7. **Synthesize** (Opus): no conclusion before every branch finishes. Fit the format to the shape of the result (no fixed template): single cause -> narrative + appendix of refuted hypotheses / multiple causes -> causal diagram or hypothesis x contribution table / all INCONCLUSIVE -> hypothesis x needed-evidence table / branching by depth -> tree / interactions between hypotheses -> matrix.
8. **Cleanup**: confirm every Agent this RCA spawned has finished reporting. On error/abort, send shutdown_request/cancel only to those Agents. **Do not touch Agents from other tasks** (context loss).

## Codex delegation (optional, teammates only)

Use only when a Codex delegation plugin such as [codex-core](https://github.com/sanghyun-io/codex-app-server-plugin) is installed. Otherwise skip this section and investigate with Glob/Grep/Read/Bash. Opus never calls Codex directly; teammates must delegate.

- Converging on INCONCLUSIVE and internal code behavior may be the cause -> delegate via `/codex-core:delegate --read-only` before concluding.
- Security/vulnerability perspective needed -> teammates lack red-review permission, so escalate to Opus.
- Simple grep/glob-level work -> handle directly (calling Codex wastes tokens).
- Codex failure (not installed / auth failure -> `codex login` / rate limit / crash) -> investigate as far as possible with Glob/Grep/Read/Bash; if still INCONCLUSIVE, report stating **why Codex is needed / why it was unavailable / next verification action (specific files, queries, experiments)**.

## Teammate prompt template

```
You are a Sonnet investigator on a multi-hypothesis RCA team.

## Your Hypothesis
{Hypothesis N: one-line summary + detailed definition}

## Symptoms / Observations
{full symptom context}

## Your Job
1. Investigate this hypothesis in depth. No depth limit.
2. Look for disconfirming evidence first.
3. If new sub-hypotheses emerge, recursively spawn general-purpose agents.
4. If deep code analysis is needed and a Codex delegation plugin is available, delegate via /codex-core:delegate --read-only.
5. Analysis only: do not propose recovery/fixes.
6. Report results to the manager via SendMessage.

## Report Format
- Conclusion: CONFIRMED / REFUTED / INCONCLUSIVE
- Evidence: file path + line + quote
- Falsification attempts: which observations could break this hypothesis + results of trying
- Remaining uncertainty: what further digging could verify
- Sub-hypotheses: summary of results from additionally spawned sub-agents
```

Example: `/multi-hypothesis only some users get 401 errors after deploy`

*Created 2026-04-29 · Last modified 2026-10-06 (condensed; reflects v2.1.178 auto-team)*
