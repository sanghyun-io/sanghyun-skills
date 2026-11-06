"""Score trigger evals from Harbor job directories.

usage: python score.py <job_dir> [<job_dir> ...]
       python score.py --self-test

A trial counts as "invoked X" if its trajectory has a Skill tool call whose skill name is X
(plugin-qualified names like "plugin:skill" are reduced to "skill").
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def skill_calls(trajectory: dict) -> list:
    names = []

    def walk(t):
        for step in t.get("steps") or []:
            for call in step.get("tool_calls") or []:
                if call.get("function_name") == "Skill":
                    args = call.get("arguments") or {}
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except ValueError:
                            args = {}
                    name = str(args.get("skill") or args.get("name") or "")
                    names.append(name.split(":")[-1])
        for sub in t.get("subagent_trajectories") or []:
            walk(sub)

    walk(trajectory)
    return names


def score(trials: list) -> dict:
    """trials: [(case_id, expect or None, [invoked skill names], cost_usd)]"""
    per_case = defaultdict(lambda: {"n": 0, "hit": 0, "expect": None, "invoked": defaultdict(int)})
    invalid = []
    for case_id, expect, invoked, _ in trials:
        if invoked is None:  # agent never ran (setup failure): not a trigger result
            invalid.append(case_id)
            continue
        c = per_case[case_id]
        c["n"] += 1
        c["expect"] = expect
        for name in set(invoked):
            c["invoked"][name] += 1
        if expect is None:
            c["hit"] += int(not invoked)
        else:
            c["hit"] += int(expect in invoked)
    per_skill = defaultdict(lambda: {"pos_n": 0, "pos_hit": 0, "neg_n": 0, "neg_hit": 0})
    for case_id, c in per_case.items():
        skill = case_id.split("-")[0]
        s = per_skill[skill]
        key = "neg" if c["expect"] is None else "pos"
        s[f"{key}_n"] += c["n"]
        s[f"{key}_hit"] += c["hit"]
    return {"cases": per_case, "skills": per_skill, "cost": sum(t[3] for t in trials), "invalid": invalid}


def load(job_dirs: list) -> list:
    cases = {c["id"]: c["expect"] for c in json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]}
    trials = []
    for job in job_dirs:
        for trial in sorted(Path(job).glob("*__*")):
            case_id = trial.name.split("__")[0]
            if case_id not in cases:
                continue
            traj_path = trial / "agent" / "trajectory.json"
            invoked = skill_calls(json.loads(traj_path.read_text(encoding="utf-8"))) if traj_path.exists() else None
            cost = 0.0
            result = trial / "result.json"
            if result.exists():
                cost = ((json.loads(result.read_text(encoding="utf-8")).get("agent_result") or {}).get("cost_usd")) or 0.0
            trials.append((case_id, cases[case_id], invoked, cost))
    return trials


def report(result: dict) -> str:
    lines = ["| skill | should trigger (recall) | should not trigger (specificity) |", "|---|---|---|"]
    for skill, s in sorted(result["skills"].items()):
        rec = f"{s['pos_hit']}/{s['pos_n']}" if s["pos_n"] else "-"
        spec = f"{s['neg_hit']}/{s['neg_n']}" if s["neg_n"] else "-"
        lines.append(f"| {skill} | {rec} | {spec} |")
    lines += ["", "| case | expect | ok | invoked |", "|---|---|---|---|"]
    for case_id, c in sorted(result["cases"].items()):
        inv = ", ".join(f"{k} x{v}" for k, v in sorted(c["invoked"].items())) or "-"
        lines.append(f"| {case_id} | {c['expect'] or 'none'} | {c['hit']}/{c['n']} | {inv} |")
    if result["invalid"]:
        lines.append(f"\nexcluded (agent never ran): {len(result['invalid'])} -> {', '.join(sorted(result['invalid']))}")
    lines.append(f"\nagent cost: ${result['cost']:.2f}")
    return "\n".join(lines)


def self_test():
    traj = {"steps": [{"tool_calls": [{"function_name": "Skill", "arguments": {"skill": "api-flow-diagram:api-flow-diagram"}}]}],
            "subagent_trajectories": [{"steps": [{"tool_calls": [{"function_name": "Skill", "arguments": "{\"skill\": \"x\"}"}]}]}]}
    assert skill_calls(traj) == ["api-flow-diagram", "x"], skill_calls(traj)
    r = score([("afd-pos-1", "api-flow-diagram", ["api-flow-diagram"], 0.1),
               ("afd-neg-1", None, ["api-flow-diagram"], 0.1),
               ("afd-neg-2", None, [], 0.1),
               ("afd-neg-3", None, None, 0.0)])
    assert r["invalid"] == ["afd-neg-3"], r["invalid"]
    s = r["skills"]["afd"]
    assert (s["pos_hit"], s["pos_n"], s["neg_hit"], s["neg_n"]) == (1, 1, 1, 2), s
    print("self-test ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) >= 2:
        print(report(score(load(sys.argv[1:]))))
    else:
        print(__doc__)
