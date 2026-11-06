# Criteria

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

## More examples and when NOT to subdivide

### By project type

| Project Type | Subdivision Unit |
|-------------|-----------------|
| Adding entities | Domain → Repository → Service → Controller → Test |
| API development | Per endpoint or per CRUD operation |
| Refactoring | Per module or per layer |
| Migration | Preparation → Execution → Verification → Cleanup |
| Adding features | Backend → Frontend → Integration tests |

### When NOT to Subdivide

- Tasks completable within 5 minutes
- Single file modifications
- Tasks with dependencies too tightly coupled to separate
