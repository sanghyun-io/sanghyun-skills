# Flow data JSON schema

Validated by `scripts/render.py`, drawn by `assets/template.html`. Complete example: `assets/example-shop.json` (fictional shop signup + first order flow).

## Top level

```json
{
  "title": "Signup + first order flow - API calls per screen/button",
  "meta": ["Entry: `https://...` | FE `repo` | BE `repo` at commit `abc1234`", "second line"],
  "legend": [{"text": "Shared HTTP client", "tone": "purple", "desc": "On 401, go to login screen"}],
  "cols": [ ... ],
  "edges": [ ... ],
  "risks": ["**Title:** content `code`", "..."]
}
```

- `meta` and `risks` support only two inline markups: `` `code` `` and `**bold**`. Everything else is escaped.
- `legend` is project-specific tag descriptions appended after the default legend (forward/error/back/method/highlight). Omit if none.
- If `risks` is empty, the "점검 결과" (review results) section disappears.

## cols: left-to-right order

```json
{"title": "Step 1", "sub": "Member info", "nodes": [ ... ]}
```

One column = one screen step or one group of branches. Many columns are fine; view with horizontal scroll. For a step with many branches, split into two columns like "Step 2" / "Step 2 branches" to reduce arrow tangling.

## node

```json
{"id": "submit", "kind": "button", "title": "[Sign up] button",
 "trig": "onSubmit SignupForm.vue:88",
 "desc": "Optional. What it does when there are no calls",
 "calls": [ ... ]}
```

| Field | Value |
|---|---|
| `id` | Unique across all. Referenced by edges |
| `kind` | `screen` screen entry / `button` button·input / `system` internal processing·external callback / `end` final screen / `fail` failure·error modal |
| `trig` | Trigger (event handler, file:line). Shown in monospace |
| `calls` | Calls made from this node. If order matters, prefix `p` with `(1)` `(2)` |

## call

```json
{"m": "POST", "p": "/api/v1/orders",
 "fe": "api/order.ts:10", "be": "routes/orders.py:20",
 "auth": {"level": "none", "text": "optional: override badge text"},
 "tags": [{"text": "Shared HTTP client", "tone": "purple"}],
 "note": "one-line behavior description", "risk": "red text if present", "highlight": true}
```

- `m`: `GET POST PUT PATCH DELETE` have fixed colors. External SDK/PG/server-to-server callbacks use `EXT`.
- `auth.level`: `none` no auth, badge "인증 없음" (green) / `cond` conditional, "조건부 인증" (orange) / `login` login required, "로그인 필요" (blue) / `admin` admin, "관리자 필요" (purple) / `unknown` not verified, "확인 못 함" (gray). If not confirmed in code, it must be `unknown`.
- `tags.tone`: `green orange red blue purple gray`.
- With `risk`, the card turns pink; `highlight: true` gives a red border (only one or two spots, e.g. failure points).

## edges

```json
{"from": "submit", "to": "cart", "label": "201 + token", "type": "fwd"}
```

- `type`: `fwd` forward (gray) / `err` error·failure (red) / `back` going back (dashed, label only on hover).
- Labels sit in the empty space right of the source node. Keep to ~20 chars; put detailed conditions in node `desc`.
- Arrows skipping two or more columns are auto-routed through a channel below the diagram. Labels on vertical arrows within the same column show only on hover.
- The source node's right edge is split evenly by the number of outgoing arrows to place start points. More than 4 makes labels overlap, so split the node.

## Errors render.py catches

Duplicate/missing ids, unknown kind/type/auth.level/tone, call missing m/p/fe/be, edges referencing nonexistent nodes, isolated nodes with no arrows.
