# Plan Subdivider

Splits a large plan into ordered task files you can execute one at a time, in this session or a later one. Each task file has an objective, a checklist, completion criteria, verification commands, and links to the previous and next task. The main plan gets a table of contents.

[한국어](README.ko.md)

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install plan-subdivider@sanghyun-skills
```

The plugin adds one skill and nothing else: no hooks, no files written at session start.

## Usage

1. Write a plan (plan mode, or any plan saved in `~/.claude/plans/`).
2. Before executing a plan with 3+ tasks, Claude offers to subdivide it. You can also ask directly ("split this plan into task files") or run `/plan-subdivider:plan-subdivide [plan_path]`.
3. Claude shows the proposed tasks and asks for approval, then writes:

```
~/.claude/plans/
├── user-authentication.md          # main plan + task table
└── user-authentication/
    ├── 01-user-entity.md
    ├── 02-user-repository.md
    ├── 03-auth-service.md
    ├── 04-auth-controller.md
    └── 05-integration-tests.md
```

4. Pick the next step (start Task 01, review, or later) and, if starting, where to work: current directory, a new branch, or a git worktree.

Not worth it for tasks that take a few minutes, single-file edits, or work too tightly coupled to split.

## Optional: enforce the pre-work question

By default the skill offers subdivision based on its description, so Claude may occasionally go straight to implementation. To make it a hard rule ("always ask before executing a plan with 3+ tasks, never skip on your own judgment"), copy the rule file yourself:

```bash
cp "<plugin dir>/rules/plan-structure.md" ~/.claude/rules/      # all projects
cp "<plugin dir>/rules/plan-structure.md" .claude/rules/        # one project
```

Find `<plugin dir>` with `/plugin` (Installed tab) or under `~/.claude/plugins/cache/sanghyun-skills/plan-subdivider/`.

## Permissions (optional)

To avoid a prompt for every task file, allow writes to the plans folder in `settings.json`:

```json
{ "permissions": { "allow": ["Write(~/.claude/plans/**)"] } }
```

## Upgrading from 1.x

- The command is now `/plan-subdivider:plan-subdivide` (was `/subdivide`).
- Rule files are no longer copied into `.claude/rules/` automatically. Earlier versions may have left `plan-structure.md` and `rule-format.md` in your projects' `.claude/rules/`; delete them unless you want the enforced rule above.

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT
