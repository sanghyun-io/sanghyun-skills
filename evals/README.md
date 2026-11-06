# Evals

Skill trigger evals run with [Harbor](https://github.com/harbor-framework/harbor) (Claude Code agent in Docker).

- `trigger/cases.json`: prompts and the skill each one should (or should not) invoke. All repo skills are installed in every trial so they compete.
- `trigger/build_tasks.py`: turns cases into Harbor task folders.
- `trigger/score.py`: reads Skill tool calls from `agent/trajectory.json` and reports recall (should trigger) and specificity (should not trigger) per skill, plus agent cost. `--self-test` checks the scorer.
- `trigger/run.sh <model> <attempts> <job-name>`: builds tasks, runs Harbor with `max_turns=3` and verification disabled, then scores. `SKILLS_REF=<commit>` measures the skills as of that commit (baseline).

Manual, paid runs (not CI). Each trial installs all repo skills so they compete. Covers `api-flow-diagram` and `multi-hypothesis` only; the other skills and output quality (A/B) are not measured yet.

Run on Linux or WSL (Harbor on native Windows has install and CRLF issues). Keep files LF (`.gitattributes`).

```bash
uv tool install harbor
export HARBOR_ANTHROPIC_API_KEY=...        # or KEY_VAR=ANTHROPIC_API_KEY
evals/trigger/run.sh anthropic/claude-sonnet-5-5 1 trig-dev
```

## Results (2026-11-06, Claude Code + claude-opus-5-5, 30 cases x 3 attempts)

Baseline = skills at `2b70c3f` (before the review fixes in #7).

| skill | version | should trigger | should not trigger |
|---|---|---|---|
| multi-hypothesis | 1.2.1 (intermittent/flaky trigger) | 21/21 | 21/21 |
| multi-hypothesis | 1.2.0 | 18/21 | 21/21 |
| multi-hypothesis | baseline | 10/21 | 21/21 |
| api-flow-diagram | current | 21/21 | 27/27 |
| api-flow-diagram | baseline | 21/21 | 27/27 |

- multi-hypothesis: the new "cause unclear, several explanations plausible" trigger catches RCA requests that don't say "RCA"/"root cause" (latency spike, nightly batch failures, conversion drop). `mh-edge-4` (flaky CI failure, "figure out why") was missed by 1.2.0 and the baseline; 1.2.1 adds intermittent/flaky failures to the trigger and catches it 3/3 with no new false triggers.
- api-flow-diagram: no difference. The model didn't over-trigger on the old broad keywords (flowchart, sequence, diagram) even without the narrowed description, so these cases are a regression guard, not evidence the narrowing was needed.
- Sonnet 5.5 (1 attempt) showed the same pattern: multi-hypothesis 6/7 vs 3/7 recall.
- Cost: about $3.8 per 90 Opus trials, $0.8 per 30 Sonnet trials (agent cost reported by Harbor).
