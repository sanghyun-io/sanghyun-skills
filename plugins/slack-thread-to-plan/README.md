# slack-thread-to-plan

Turn a Slack thread into an implementation plan for the current project.

Given a Slack permalink, the skill fetches the whole thread (parent and replies, with names resolved and attachments listed or downloaded), extracts requirements and open questions, maps them to files and modules in the current project, and saves a structured plan to `~/.claude/plans/`. It asks before writing anything and never touches code unless you choose to start implementing.

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install slack-thread-to-plan@sanghyun-skills
```

## Usage

Share a permalink such as `https://<workspace>.slack.com/archives/C0123/p1700000000000000` and ask to analyze it or build a plan.

Example prompts:
- "이 슬랙 스레드 요구사항 정리해서 작업 계획 세워줘"
- "analyze this Slack thread and plan the work"

## Requirements

A Slack user token in `SLACK_USER_TOKEN` (xoxp-) with `channels:history`, `groups:history`, `im:history`, `mpim:history`, `users:read`. The token owner must be a member of the channel. Python 3.9+.

## License

MIT
