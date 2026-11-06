# Templates

## Task file

Each task file is generated with the following structure:

```markdown
# Task {order}: {task name}

> **Order**: {current}/{total}
> **Previous task**: [{previous task name}](./{previous file}) or (none - first task)
> **Next task**: [{next task name}](./{next file}) or (none - last task)
> **Reference**: Original plan {section reference}

---

## Objective

{Objective for this task extracted from the original plan}

---

## Checklist

### 1. {First step}

- [ ] {Sub-task 1}
- [ ] {Sub-task 2}

### 2. {Second step}

- [ ] {Sub-task 3}

---

## Completion Criteria

1. All Checklist items checked
2. Build succeeds (if applicable)
3. Tests pass (if applicable)

---

## Verification Commands

```bash
# Auto-detected based on project context
# Kotlin/Java: ./gradlew build or ./gradlew ktlintCheck
# Node.js: npm test or npm run lint
# Python: pytest or ruff check
```

---

## Next Task

After verification passes, proceed to the next task:

**[Task {next}: {next task name}](./{next file})**

In the next task:
- {Next task summary}

---

*Created: {today's date}*
```

---

## Main plan table of contents

Add a table of contents to the top of the main plan file:

```markdown
## Implementation Tasks

This plan has been divided into {N} detailed tasks.

| Order | Task Name | File | Description |
|:-----:|-----------|------|-------------|
| 1 | **{task1}** | [01-{filename}.md](./{folder}/01-{filename}.md) | {description} |
| 2 | **{task2}** | [02-{filename}.md](./{folder}/02-{filename}.md) | {description} |
...

### Task Rules

1. **Sequential execution**: Proceed in order starting from Task 01
2. **Checklist**: Check all items in each task before moving to the next
3. **Run verification**: Execute verification commands upon completing each task
4. **Follow links**: Navigate using the "Next Task" link at the bottom of each task file

---
```

## Worked example

### Input (Original Plan)

```markdown
# Implement User Authentication

## Objective
Implement JWT-based authentication system

## Implementation
1. Create User entity
2. Create UserRepository
3. Implement AuthService
4. Write AuthController API
5. Write tests
```

### Output (Subdivision Result)

```
user-authentication/
├── 01-user-entity.md
├── 02-user-repository.md
├── 03-auth-service.md
├── 04-auth-controller.md
└── 05-integration-tests.md
```
