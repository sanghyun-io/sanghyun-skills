---
name: team-launch
description: |
  Manager pattern that delegates multiple independent coding tasks in parallel via a Team Agent structure.
  Use when the user explicitly hands you the "manager" (관리자) role: split N tasks into N worktrees,
  attach a Sonnet teammate agent to each, and let them implement + commit + open PRs autonomously.
  The Opus manager only does integration verification + merging + conflict resolution.

  TRIGGER example utterances:
    - "Team Agent 구성해서 (너가 관리자)" (build a Team Agent, you're the manager)
    - "팀 만들어서 각자 위임해" (make a team and delegate to each)
    - "Team 으로 병렬 진행" (proceed in parallel as a team)
    - "관리자 역할로 N개 작업 위임" (delegate N tasks as manager)
    - "팀원들에게 분배" (distribute to teammates)

  vs Agent (simple delegation):
    - Agent delegates a single task and integrates the result
    - Team Agent delegates N tasks at once + explicit manager duties (resource isolation / integration verification / sequential merge)
    - If the user says "관리자" (manager), they intend the Team Agent structure
    - (v2.1.178+) The team forms automatically on the first teammate Agent spawn and is cleaned up at session end; TeamCreate/TeamDelete tools are removed
invocation:
  command: team-launch
  user_invocable: true
  args:
    - name: tasks
      description: List of tasks to delegate (if omitted, ask via AskUserQuestion)
      required: false
---

# Team Launch

Giving you the "manager" role is a request for an organizational structure, not simple delegation. The manager (Opus = self) owns resource isolation, conflict avoidance, integration verification, sequential merging, and cleanup. Spawning Agents in parallel without these duties defeats the purpose of this skill.

## Procedure

1. **Fix the task list**: extract from the utterance; if insufficient, AskUserQuestion (N tasks / priority / dependencies).
2. **Conflict analysis**: check whether tasks touch the same files. If they overlap, report to the user and have them choose: (a) serialize (b) merge then reorder (c) delegate the combined work to one teammate.
3. **Resource isolation**: each task gets its own branch (`feat/{task}`), worktree path, and dev server port.
   - Ports: main/default 8080, teammates 8081, 8082, 8083 ... max 5 teammates (8081-8085). Beyond that, serialize.
4. **Create worktrees**: `git worktree add ../{name} -b feat/{branch} origin/main` + link dependency folders (`node_modules`, `.venv`) to main instead of copying or reinstalling (junction on Windows, symlink elsewhere). Teammates must not run `npm install`/`pip install` inside the worktree; it overwrites the link with a real folder.
5. **Spawn teammates**: `Agent` tool, `subagent_type: "general-purpose"`, `model: sonnet`, set `name` (addressable via SendMessage). **Spawn in parallel in one message.** The team forms automatically on the first spawn (no separate creation step; `TeamCreate`/`TeamDelete` do not exist).
6. **Track tasks**: register with `TaskCreate`, set owner/blockedBy with `TaskUpdate`, monitor with `TaskList`/`TaskGet`.
7. **Teammate execution**: inside its own worktree, implement -> verify on dev server -> commit -> push -> PR -> report PR URL via `SendMessage` + mark done with `TaskUpdate`.
8. **Integration verification**: teammates' in-worktree verification is not enough. After merging, run the dev server from main and confirm no conflicts, zero console errors, and no visual regressions.
9. **Sequential merge**: order: independent PRs with zero file overlap -> foundation/lower-layer PRs -> PRs most likely to conflict (last). Pre-check by comparing `git diff --name-only origin/main origin/{branch}` per branch. After each merge, wait for GitHub to recompute mergeable; on conflict, rebase in that worktree + `--force-with-lease`. The manager resolves any conflicts the pre-analysis missed.
10. **Cleanup**: see "Cleanup" below. If teammates must be stopped before merging, send shutdown_request via `SendMessage`. The team itself is cleaned up automatically at session end.

## Teammate prompt template

```
You own {task name} for {project name}.
N other teammates are working concurrently in separate worktrees, so work only inside your worktree.

# Worktree
- Path: {absolute path}
- Branch: {branch name} (based on origin/main)
- Dependency folders are linked to main; do not run npm install / pip install
- Dev server port: {N}

# Background
{needed context: existing PRs / token system / components, etc.}

# Task
{concrete change spec}

# Work rules
{visual parity / risky areas / prohibitions}

# Verification
Start dev server on port {N} -> confirm 200 response -> confirm compile success and console errors -> visually check with Playwright if possible -> stop dev server

# Commit + PR
Korean conventional commit (attribution per harness rules); proceed autonomously through gh pr create.

# Report
PR URL + change summary + risky areas + verification results, in Korean, within 250 words

# Prohibited
- Modifying files outside the worktree, accessing other worktrees
- npm install / modifying package.json
- {task-specific prohibitions}
```

## Windows specifics

- If the project's dev server script doesn't recognize a side worktree path, start it directly in that worktree with an explicit port.
- Write Korean prompts/commit messages to files instead of passing them through pipes (encoding breaks).
- If Playwright MCP is occupied by another task, don't force-kill it (requires user approval); use the `npx playwright` CLI.

## Cleanup

1. Kill the PIDs of dev servers LISTENING on team ports (8081~).
2. Remove worktrees: move the manager shell/session cwd out of the worktree, then **detach links first** (Windows junction: `cmd /c rmdir <path>`, symlink: `rm <link>`; no recursive delete). Confirm no links remain, then `git worktree remove <path>`. If the project has a worktree cleanup script, use it.
   - Never `git worktree remove --force` / `rm -rf` with links still attached; it follows the junction and deletes main's node_modules/.venv.
3. Delete local branches (`git branch -D ...`), `git pull origin main --ff-only`.

*Related*: `multi-hypothesis` (Team pattern for analysis)
*Last modified*: 2026-10-06 (condensed for frontier models)
