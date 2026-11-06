# sanghyun-skills

Personal Claude Code skills by [sanghyun-io](https://github.com/sanghyun-io), published as a plugin marketplace. Each skill is its own plugin, so you can install only what you need.

This repository was previously `plan-subdivider`. That plugin now lives in [`plugins/plan-subdivider`](plugins/plan-subdivider).

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install <plugin>@sanghyun-skills
```

From a shell: `claude plugin marketplace add sanghyun-io/sanghyun-skills` then `claude plugin install <plugin>@sanghyun-skills`.

## Plugins

| Plugin | What it does |
|---|---|
| [plan-subdivider](plugins/plan-subdivider) | Breaks large plans into sequential task files with checklists and verification steps |
| [api-flow-diagram](plugins/api-flow-diagram) | Traces every API a user journey calls (FE + BE) and renders a left-to-right flow diagram HTML |
| [multi-hypothesis](plugins/multi-hypothesis) | Root cause analysis with several hypotheses investigated in parallel by sub-agents |
| [session-handoff](plugins/session-handoff) | Turns the current session into a handoff prompt for a fresh session |
| [skill-scaffolder](plugins/skill-scaffolder) | Scaffolds or refactors skills with progressive disclosure and trigger-rich descriptions |
| [slack-thread-to-plan](plugins/slack-thread-to-plan) | Reads a Slack thread from its permalink and writes an implementation plan |
| [team-launch](plugins/team-launch) | Runs several coding tasks in parallel (one worktree and sub-agent each), then integrates and merges |

Most skill instructions are written in Korean; Claude follows them whatever language you use.

## Upgrading from plan-subdivider

The marketplace name changed from `plan-subdivider` to `sanghyun-skills`. If you installed the old one:

```
/plugin marketplace remove plan-subdivider
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install plan-subdivider@sanghyun-skills
```

## Layout

```
.claude-plugin/marketplace.json      # marketplace manifest
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
plugins/<name>/README.md
```

Validate before pushing: `claude plugin validate --strict .` and `claude plugin validate --profile directory plugins/<name>`.

## License

MIT
