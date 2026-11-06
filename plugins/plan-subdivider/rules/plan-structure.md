---
rule_type: workflow
applies_to:
  - "~/.claude/plans/*.md"
  - "Plan file creation"
  - "Plan execution"
triggers:
  - event: "plan_execute"
    description: "When plan file execution begins - perform Pre-work before implementation"
  - event: "plan_created"
    description: "When plan file creation is complete"
---

# Plan Structure Rules

Optional, opt-in rule. The plugin does not install it. Copy it to `~/.claude/rules/` (all projects) or `.claude/rules/` (one project) if you want Claude to be *forced* to ask about subdividing before executing any plan with 3+ tasks. Without it, the `plan-subdivide` skill still offers this based on its description.

---

## 🔴 Required Actions (Action Required)

> **MUST DO**: You must perform the following actions whenever this rule applies.

### First Task When Executing a Plan (Pre-work)

> ⛔ When the user selects "Start", you **must** perform the following **before reading code or beginning implementation**:

| Order | Check | Condition | Action |
|:-----:|-------|-----------|--------|
| 1 | Task count | Task ≥ 3 | Confirm whether to run `/plan-subdivider:plan-subdivide` **using AskUserQuestion** |
| 2 | Complexity | Multi-file changes | Confirm whether to run a plan review (your review command, if any) **using AskUserQuestion** |
| 3 | Pre-work complete | - | Then begin actual implementation |

#### ✅ AskUserQuestion Usage (Required)

> **CRITICAL**: In **all situations** requiring user confirmation, you **must use the AskUserQuestion tool** instead of plain text.

##### Scope

**Cases where AskUserQuestion is required**:
1. **Pre-work confirmation**: Whether to run `/plan-subdivider:plan-subdivide`, a plan review (your review command, if any) before plan execution
2. **In-skill confirmation**: Subdivision plan approval during `/plan-subdivider:plan-subdivide`, next step selection after completion
3. **Progress confirmation**: All decision points with multiple choices
4. **Dangerous operations**: Before irreversible operations such as file deletion or overwriting

##### Pre-work Confirmation Example

```json
{
  "questions": [{
    "question": "Would you like to run Pre-work before plan execution?",
    "header": "Pre-work",
    "multiSelect": false,
    "options": [
      {"label": "Skip and start now", "description": "Begin implementation without Pre-work"},
      {"label": "Run /plan-subdivider:plan-subdivide", "description": "Subdivide the plan into detailed task files"},
      {"label": "Run /review", "description": "Review the plan"}
    ]
  }]
}
```

##### In-skill Confirmation Example

Subdivision plan approval in `/plan-subdivider:plan-subdivide` skill:
```json
{
  "questions": [{
    "question": "Proceed with this subdivision plan?",
    "header": "Confirm",
    "multiSelect": false,
    "options": [
      {"label": "Proceed", "description": "Start creating files as planned"},
      {"label": "Needs revision", "description": "Review and revise the plan"},
      {"label": "Cancel", "description": "Abort subdivision"}
    ]
  }]
}
```

##### Prohibited

- ❌ Asking as plain text: "Shall I run subdivide?", "Proceed as planned?", "Would you like to start?"
- ❌ Giving instructions without choices: "Start the task with the following command"
- ✅ **All confirmations** must use the AskUserQuestion tool

#### ⛔ No Re-searching Plans

- If Plan content is **already in the current conversation context**, do not search/read it again
- When starting implementation after ExitPlanMode, use the Plan information from context
- Only read Plan files when a plan execution is requested in a new session

### ⛔ Prohibited

- Starting code reading/implementation without Pre-work
- Even when a plan execution is requested in a new session, Pre-work must be performed first
- Jumping straight into implementation after reading a Plan file
- **Claude must NOT decide to skip `/plan-subdivider:plan-subdivide` or a plan review (your review command, if any) on its own**
  - Cannot skip for reasons like "already detailed enough", "clearly separated", "well-structured"
  - When conditions are met, you **must ask** the user whether to run them
  - Skip is only allowed when the user explicitly answers "no"

---

## Linked Skills

<!-- @linked-skills: Skills in this table should be automatically suggested when conditions are met -->

| Skill | Trigger Condition | Execution Mode | Description |
|-------|-------------------|:--------------:|-------------|
| `/plan-subdivider:plan-subdivide` | Task ≥ 3 AND Plan execution starting (Pre-work) | confirm | Subdivide plan into detailed task files |
| your plan-review command (if you have one) | Multi-file changes AND Plan execution starting (Pre-work) | confirm | Review plan |
| `/plan` | When a new plan is needed | auto | Create plan |

**Execution mode descriptions**:
- `auto`: Execute automatically when conditions are met
- `confirm`: **Must** ask the user whether to execute when conditions are met (Claude cannot decide to skip on its own)
- `ask`: Ask the user whether it is needed

**⚠️ `confirm` notes**:
- Claude cannot **decide to skip on its own** for reasons like "already detailed enough" or "well-separated by task"
- When the condition (Task ≥ 3) is met, you **must always ask the user**
- Skip is only allowed when the user explicitly answers "skip", "no", "not needed", etc.

**⛔ Important**: `/plan-subdivider:plan-subdivide` and a plan review (your review command, if any) are the **first actions (Pre-work)** of plan execution and must be confirmed before reading code or beginning implementation.

<!-- @/linked-skills -->

---

## When This Applies

- When writing plans in Plan mode
- When running `/plan`
- When creating complex work plans

---

## Main Plan File Structure

Main plan files follow this structure:

```markdown
# {plan title}

> **Created**: YYYY-MM-DD
> **Purpose**: {one-line description of the plan's purpose}

---

## Implementation Tasks

This plan has been divided into N detailed tasks. Execute them in order.

| Order | Task Name | File | Description |
|:-----:|-----------|------|-------------|
| 1 | **Task 1** | [01-task-name.md](./plan-name/01-task-name.md) | Task description |
| 2 | **Task 2** | [02-task-name.md](./plan-name/02-task-name.md) | Task description |
| ... | ... | ... | ... |

### Task Rules

1. **Sequential execution**: Proceed in order starting from Task 01
2. **Checklist**: Check all items in each task before moving to the next
3. **Lint check**: Run code verification upon completing each task
4. **Follow links**: Navigate using the "Next Task" link at the bottom of each task file

---

## Core Content

{Core content of the plan...}
```

---

## Task File Structure

Each task file follows this structure:

```markdown
# Task {order}: {task name}

> **Order**: {current}/{total}
> **Previous task**: [{previous task name}](./{previous file}) or (none - first task)
> **Next task**: [{next task name}](./{next file}) or (none - last task)
> **Reference**: Original plan {section reference}

---

## Objective

{Description of this task's objective}

---

## Checklist

### 1. {First step}

- [ ] {Sub-task 1}
- [ ] {Sub-task 2}
  - Code examples or detailed descriptions may be included

### 2. {Second step}

- [ ] {Sub-task 3}
- [ ] {Sub-task 4}

---

## Completion Criteria

1. All Checklist items checked
2. Build succeeds (if applicable)
3. Tests pass (if applicable)

---

## Verification Commands

Run the following commands after completing the task:

\`\`\`bash
{verification commands appropriate for the project}
\`\`\`

---

## Next Task

After verification passes, proceed to the next task:

**[Task {next order}: {next task name}](./{next file})**

In the next task:
- {Next task summary 1}
- {Next task summary 2}

---

*Created: YYYY-MM-DD*
```

---

## Subdivision Criteria

Criteria for splitting a plan into detailed tasks:

### When to Subdivide

1. **Independent deliverables**: Each task can be completed independently
2. **Logical stages**: Steps that must proceed sequentially
3. **Different areas**: Different code/file areas
4. **Verifiable**: Each task can be verified after completion

### Subdivision Examples

| Task Type | Subdivision Unit |
|-----------|-----------------|
| Adding entities | Domain → Repository → Service → Controller |
| API development | Per endpoint or per feature |
| Refactoring | Per module or per layer |
| Migration | By stage (Preparation → Execution → Verification → Cleanup) |

---

## File Naming Conventions

### Main Plan

- Location: `~/.claude/plans/{plan-name}.md`
- Naming: Use the auto-generated name from Claude

### Task Files Folder

- Location: `~/.claude/plans/{plan-name}/`
- Files: `{2-digit-order}-{task-name-kebab-case}.md`

### Example

```
~/.claude/plans/
├── jaunty-greeting-puffin.md           # Main plan
└── jaunty-greeting-puffin/             # Task files folder
    ├── 01-campaign-response-entity.md
    ├── 02-evaluation-result-entity.md
    ├── 03-audit-log-enhancement.md
    ├── 04-service-expansion.md
    ├── 05-api-migration.md
    └── 06-submission-removal.md
```

---

## Checklist Writing Guidelines

### Good Checklists

- [ ] **Specific**: Clearly states what needs to be done
- [ ] **Verifiable**: Completion can be determined
- [ ] **Independent**: No overlap with other items
- [ ] **Ordered**: Arranged by dependency order

### Including Code Examples

If a checklist item needs a code example, include it with indentation:

```markdown
- [ ] Create `UserService.kt`
  ```kotlin
  interface UserService {
      fun getUser(id: Long): User
  }
  ```
```

---

