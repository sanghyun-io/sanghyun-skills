# multi-hypothesis

Root cause analysis that keeps several hypotheses alive at once.

Instead of locking onto the first plausible cause, the skill lists competing hypotheses, gets your approval, then spawns one investigator sub-agent per hypothesis in parallel. Each investigator looks for disconfirming evidence first and reports CONFIRMED / REFUTED / INCONCLUSIVE with file:line evidence. The manager synthesizes only after every line of inquiry is finished, choosing the report shape that fits the result (single cause, contributing causes, or open questions).

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install multi-hypothesis@sanghyun-skills
```

## Usage

Invoke with `/multi-hypothesis:multi-hypothesis <symptom>` or just describe a problem and ask for a root cause analysis.

Example prompts:
- "배포 후 일부 사용자만 401 이 나는 원인 분석해줘"
- "root cause of the intermittent timeout, check multiple hypotheses"

## Requirements

Sub-agent support (Agent and SendMessage tools). Codex delegation is optional and used only when a Codex plugin such as codex-core is installed.

## License

MIT
