# Packaging skills as plugins

Read when a skill should be shared: installed by others, kept in a repo, or listed in a marketplace.

## Layout (marketplace repo with one plugin per skill)

```
.claude-plugin/marketplace.json
plugins/{name}/.claude-plugin/plugin.json
plugins/{name}/skills/{name}/SKILL.md      # + references/ scripts/ assets/
plugins/{name}/README.md                   # required for the plugin directory
```

- One plugin per skill lets people install only what they need.
- `marketplace.json`: `name`, `owner.name`, `plugins[]` with `name` + `source` (`"./plugins/{name}"`, must start with `./`), plus `description`, `category`, `tags`.
- `plugin.json`: only `name` is required; add `description`, `version`, `author`, `repository`, `license`, `keywords`.
- Names: kebab-case. Plugin names must not start with `claude-`, `anthropic-`, `cc-plugin-`; marketplace names like `agent-skills`, `claude-code-plugins` are reserved.
- Bump `version` on every change; users stay on the installed version until it changes.

## Make skills portable

- Paths: use `${CLAUDE_SKILL_DIR}` (the skill's own folder) and `${CLAUDE_PLUGIN_ROOT}` (the plugin root) in SKILL.md; both are substituted at invocation and work whether the skill is a plugin or a user skill. Never hard-code a home directory.
- Strip personal context: private rule files, local scripts, company names/URLs, real data in examples. Replace examples with fictional ones.
- Prefer no hooks. A SessionStart hook that writes files or prints text runs in every project for every user; put triggers in the skill `description` instead.
- Don't depend on other plugins silently; mark such steps optional ("only if X is installed").
- Unknown frontmatter keys are ignored; keep only `name`, `description` and documented keys.

## Validate and test

```bash
claude plugin validate --strict .                            # marketplace
claude plugin validate --profile directory plugins/{name}    # what the plugin directory checks
```

Test a real install without touching your own config:

```bash
export CLAUDE_CONFIG_DIR="$(mktemp -d)"
claude plugin marketplace add {owner}/{repo}
claude plugin install {name}@{marketplace}
```

Skills from a plugin are invoked as `/{plugin}:{skill}`. To submit to Anthropic's plugin directory, use https://claude.ai/directory/manage (paid plan; reviewed). The listing icon (square PNG, 512-2048 px, `.claude-plugin/icon.png`) is fixed at first submission.
