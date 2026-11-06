# parallel-team

Run several independent coding tasks in parallel with you as the manager.

When you hand Claude the manager role, this skill splits N tasks into N git worktrees (own branch and dev-server port each), checks for file overlap first, spawns one sub-agent per task in a single message, and tracks them. Each member implements, verifies, commits, and opens a PR. The manager then runs integration checks on the merged result, merges in a safe order, and cleans up worktrees without destroying linked dependency folders.

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install parallel-team@sanghyun-skills
```

## Usage

Say "Team Agent 구성해서 (너가 관리자)", "팀원들에게 분배", or "run these in parallel as a team", or run `/parallel-team:parallel-team <tasks>`.

Base branch, ports, and commit language are read from the repo (default branch, dev-server config, recent commit history) rather than hard-coded.

Formerly named `team-launch` (renamed in 2.0.0).

Example prompts:
- "Team Agent 구성해서 이 세 작업 병렬로 (너가 관리자)"
- "split these tasks across a team and merge them"

## Requirements

Git, GitHub CLI (`gh`) for PRs, and sub-agent support.

## License

MIT
