# Requirements Analysis Framework

Write only what the source supports; mark inferences as "inferred".

## Extract

- Requirements: functional / non-functional (performance, security, UX, compatibility, schedule), explicit vs inferred
- Context: background/problem, agreements, open questions, objections/concerns
- Meta: priority, owner (@mentions), deadline cues, references (attachments, links, issue/PR numbers)

## Resolve with AskUserQuestion

Conflicting requirements, dependence on context outside the thread ("that thing", "what I mentioned last time"), unclear scope ("improve it"), missing priority/deadline cues that affect the plan. Make options concrete, plain text only, no emoji or decorative characters.

## Chat output template

```
## Thread summary
{3-5 lines: who, what, why}

## Requirements
| # | Type | Requirement | Evidence (quote/author) | Explicit/Inferred |
|---|------|-------------|-------------------------|-------------------|
| R1 | Functional | ... | "..." — @author | Explicit |

## Agreed / Open
- Agreed: ...
- Open: ... (→ needs confirmation)

## Priority · Owner · Deadline
- ...

## Project application plan
| Requirement | Location (file/module) | Approach | Consistency with existing decisions |
|-------------|------------------------|----------|-------------------------------------|
| R1 | packages/.../x.js | ... | Matches / conflicts with CHECKPOINT §N |

## Work plan (draft)
1. {task} — depends on: none — verify: {command/method}
2. {task} — depends on: 1 — verify: ...
```

The application plan respects `CLAUDE.md`, `docs/CHECKPOINT.md` (design decisions), `docs/WORK_QUEUE.md` (duplicates/priority). On conflict, state "conflicts with CHECKPOINT §N" and ask for a decision.
