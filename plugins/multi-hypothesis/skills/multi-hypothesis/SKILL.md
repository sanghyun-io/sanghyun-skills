---
name: multi-hypothesis
description: |
  Root cause analysis that keeps several competing hypotheses alive and investigates them in parallel with one sub-agent each, looking for disconfirming evidence first, instead of settling on the first plausible cause. Analysis only; no fixes.
  Use when the cause is unclear and several explanations are plausible, or the user asks for it: "원인 분석", "근본 원인", "왜 이렇게 됐는지", "여러 가능성", "다중 가설", "multi-hypothesis", "multiple working hypotheses", "root cause", "RCA", "postmortem".
  Do NOT use when one clue already points to a single cause (just debug it), for a quick "why does this line fail" question, or when the user wants a fix rather than an analysis.
---

# Multi-Hypothesis RCA

Basis: T.C. Chamberlin (1890), *The Method of Multiple Working Hypotheses*: don't get attached to the first explanation; keep several alive and trace each to the end. **Analysis only: do not propose recovery or fixes.**

## Cost check first

This spawns 3-5 agents. Use it only when it pays off:
- Fewer than 3 independent, plausible hypotheses → investigate directly instead.
- The symptom reproduces locally and the stack trace points at one place → debug normally.
- Otherwise say up front that you will run parallel investigators, and get approval in Step 3.

## Procedure

1. **Fix the symptom**: from the request or args; if insufficient, AskUserQuestion (what happens, since when, who is affected, what changed).
2. **Derive 3-5 hypotheses**: independent, mutually exclusive where possible, testable, falsifiable, specific ("stale DNS cache", not "environment issue"). Sweep each category once to avoid gaps: code/logic (boundaries, off-by-one), state/data (migrations, cache), environment/config (env vars, permissions, dependency versions), concurrency/timing (races, deadlocks, retry storms), infra/network (DNS, TLS, proxy, rate limits), human factors (recent changes, deploys, manual steps), external dependencies (third-party APIs, monitoring blind spots).
3. **Approval**: show the hypotheses and get approval via AskUserQuestion.
4. **Parallel spawn**: one `general-purpose` Agent per hypothesis, **all in one message**, using the template below. Investigators can use a cheaper model (e.g. `model: sonnet`) than the main session. Their final message is their report.
   - If agents from other work are running, give yours distinct names (`mh-1`...) and pass only this RCA's scope.
5. **Investigate** (each agent): disconfirming evidence first, no depth limit, until a verifiable conclusion. A real sub-hypothesis may get its own sub-agent.
6. **Synthesize** (you): no conclusion until every line of inquiry has reported. Shape the report to the result, no fixed template: single cause → narrative + appendix of refuted hypotheses; several causes → causal diagram or hypothesis × contribution table; all INCONCLUSIVE → hypothesis × evidence-needed table; interacting causes → matrix.
7. **Cleanup**: confirm all agents this RCA started have finished; on abort, stop only those. **Never touch agents from other work.**

## Optional: Codex delegation (investigators only)

Only if a Codex delegation plugin such as [codex-core](https://github.com/sanghyun-io/codex-app-server-plugin) is installed; otherwise skip and use Glob/Grep/Read/Bash.
- Converging on INCONCLUSIVE and the cause may be deep in code behavior → `/codex-core:delegate --read-only` before concluding.
- Grep-level lookups → do them directly.
- Codex unavailable or failing → investigate as far as possible, and if still INCONCLUSIVE state why Codex was needed, why it was unavailable, and the next concrete verification step (file, query, experiment).

## Investigator prompt template

```
You are one investigator on a multi-hypothesis root cause analysis. Analysis only: do not propose fixes.

Hypothesis: {N: one-line summary + precise definition}
Symptoms / observations: {full symptom context}
Other hypotheses being checked in parallel (don't duplicate them): {list}

Job:
1. Look for evidence that would REFUTE this hypothesis first, then for confirming evidence.
2. Go as deep as needed to reach a verifiable conclusion.
3. If a distinct sub-hypothesis appears, you may spawn a general-purpose sub-agent for it.

Final report:
- Conclusion: CONFIRMED / REFUTED / INCONCLUSIVE
- Evidence: file path + line + quote, or command + output
- Falsification attempts: what could have broken the hypothesis, and what happened
- Remaining uncertainty: what further checks would settle it
- Sub-hypotheses: results from any sub-agents
```

Example: `/multi-hypothesis:multi-hypothesis only some users get 401 errors after deploy`
