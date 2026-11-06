# api-flow-diagram

Trace every API a user journey calls and draw it as a left-to-right flow diagram.

The skill delegates code tracing (frontend and backend) to a sub-agent, spot-checks the key claims against the source, and renders one self-contained HTML file: columns per step, nodes per screen or button, the endpoints each one calls (method, path, FE/BE file:line, auth requirement, risk note), arrows for normal, error, and back paths, plus a full endpoint table.

The layout code is fixed (`assets/template.html`); only a data JSON changes. `scripts/render.py` validates the JSON (unknown node ids, duplicate ids, invalid values, orphan nodes) before rendering.

> The skill instructions are written in Korean. Claude follows them regardless of the language you use.

## Install

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install api-flow-diagram@sanghyun-skills
```

## Usage

```bash
# <skill dir> = ~/.claude/plugins/cache/sanghyun-skills/api-flow-diagram/<version>/skills/api-flow-diagram
python "<skill dir>/scripts/render.py" flow.json flow.html
python "<skill dir>/scripts/render.py" --self-test
```
Try it with the bundled example: `assets/example-shop.json` (a fictional sign-up and first order flow).

Example prompts:
- "회원가입 흐름에서 호출되는 API 전부 흐름도로 그려줘"
- "map every endpoint the checkout page calls"

## Requirements

Python 3.9+ (standard library only). A browser automation tool (Playwright) is optional, for visual checks.

## License

MIT
