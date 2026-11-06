---
name: parallel-team
description: |
  Manager pattern for several independent coding tasks at once: one git worktree, branch, port, and sub-agent per task, each implementing through a PR, while you (the manager) handle conflict analysis, integration verification on the merged result, ordered merges, and safe cleanup.
  Use when the user hands you the manager role or asks for a team, e.g. "관리자", "Team Agent 구성해서 (너가 관리자)", "팀 만들어서 각자 위임해", "팀원들에게 분배", "Team 으로 병렬 진행", "you're the manager", "split these across a team", "run these tasks in parallel".
  Do NOT use for a single task (use one Agent) or for root-cause analysis (use multi-hypothesis).
---

# Parallel Team

Being made "manager" means owning the organization, not just spawning agents: resource isolation, conflict avoidance, integration verification, ordered merging, and cleanup. Parallel spawns without these duties miss the point.

## Defaults (read from the repo, don't assume)

- **Base branch**: the repo default (`git symbolic-ref refs/remotes/origin/HEAD`), not a hard-coded `main`.
- **Ports**: the project's dev port from its config; teammates get base+1, base+2, ... Up to 5 teammates; more than that, serialize.
- **Commit and report language**: follow the repo's recent commit history and the user's language.
- **Models**: keep conflict analysis, merge order, and integration judgment on the strongest model you have. Teammates implement: a balanced tier suits well-specified tasks, the strongest for tricky ones; pure lookups can go to the cheapest tier. Pick from the models this agent actually offers (rough tiers: fast/cheap = Haiku-, mini-, flash-class; balanced = Sonnet-class; strongest = Opus-class or top reasoning models); don't assume a name.

## Procedure

1. **Task list**: extract from the request; if unclear, AskUserQuestion (tasks / priority / dependencies).
2. **Conflict analysis**: do tasks touch the same files? If so, report and let the user choose: (a) serialize (b) merge then rebase the rest (c) give the overlapping work to one teammate.
3. **Isolation**: per task a branch (`feat/{task}`), a worktree, and a port.
4. **Worktrees**: `git worktree add ../{repo}-{task} -b feat/{task} origin/{base}`. Link dependency folders (`node_modules`, `.venv`) to the main checkout instead of copying or reinstalling (Windows junction, symlink elsewhere). Teammates must not run `npm install`/`pip install` in the worktree: it replaces the link with a real folder.
5. **Spawn**: one `Agent` per task (`subagent_type: "general-purpose"`, a `name` so it is addressable), **all in one message**. Use the template below.
6. **Track**: if task tools exist (`TaskCreate`/`TaskUpdate`/`TaskList`), register tasks with owner and blockedBy; otherwise keep a table in chat.
7. **Teammates**: implement in their worktree → verify on their port → commit → push → open PR → final report with the PR URL.
8. **Integration verification**: per-worktree checks are not enough. After merging, run the app from the base branch and confirm no conflicts, zero console errors, no visual regressions.
9. **Merge order**: PRs with zero file overlap → foundation/lower-layer PRs → most conflict-prone last. Pre-check with `git diff --name-only origin/{base}...origin/{branch}`. After each merge wait for GitHub to recompute mergeability; on conflict rebase in that worktree and `push --force-with-lease`. Resolve conflicts the pre-check missed yourself.
10. **Cleanup**: below. To stop a teammate early, send it a shutdown request via `SendMessage`.

## Teammate prompt template

```
You own {task} in {project}. {N} other teammates work at the same time in separate worktrees: stay inside yours.

Worktree: {absolute path} | Branch: {branch} (from origin/{base}) | Port: {port}
Dependency folders are linked to the main checkout: do not run npm install / pip install or edit lockfiles.

Background: {context the task needs: related PRs, components, conventions}
Task: {concrete change spec}
Rules: {visual parity, risky areas, task-specific prohibitions}

Verify: start the app on port {port} → HTTP 200 → build/compile passes, no console errors → visual check with Playwright if available → stop the server.
Commit + PR: conventional commit in the repo's language and style; push and open the PR with `gh pr create` without asking.
Report (final message, under 250 words): PR URL, change summary, risky areas, verification results.
Never: modify files outside your worktree, touch other worktrees, change dependencies.
```

## Platform notes

- If the project's dev script can't handle a side worktree, start the server in that worktree with an explicit port.
- On Windows, write non-ASCII prompts and commit messages to files instead of piping them (encoding breaks).
- If Playwright MCP is busy with another task, don't kill it without the user's approval; use the `npx playwright` CLI.

## Cleanup

1. Stop dev servers listening on the team ports.
2. Remove each worktree: move your shell/session cwd outside it, **detach links first** (Windows junction: `cmd /c rmdir <path>`; symlink: `rm <link>`; never recursive), confirm none remain, then `git worktree remove <path>`. Prefer the project's own worktree cleanup script if it has one.
   - Never `git worktree remove --force` or `rm -rf` with links attached: it follows the junction and deletes the main checkout's `node_modules`/`.venv`.
3. Delete local branches (`git branch -D ...`) and `git pull --ff-only` on the base branch.
