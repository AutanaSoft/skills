---
title: Treat SDD artifacts as living documents
impact: HIGH
impactDescription: Prevents losing approved decisions or regenerating inconsistent artifacts
tags: lifecycle, sdd, artifacts, changelog
---

## Treat SDD artifacts as living documents

**Impact: HIGH (prevents losing approved decisions or regenerating inconsistent artifacts)**

Existing SDD artifacts are living documents. If an artifact already exists, do not overwrite or
blindly regenerate it. Read it first, preserve valid decisions, and update only the sections
affected by the new context.

### Rule

If the target artifact already exists:

1. Read the existing artifact first.
2. Preserve approved decisions.
3. Update only the sections affected by the new context.
4. Do not overwrite or recreate valid content unless explicitly instructed.
5. Update frontmatter when present.
6. Append a `Change Log` entry.
7. Keep the artifact internally consistent with related PRD/spec/design/tasks.

### Create vs Update Decision

| Situation                                               | Action                                                          |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| The artifact does not exist                             | Create it with lifecycle metadata.                              |
| The artifact exists and is structurally valid           | Update it incrementally.                                        |
| The artifact exists but has no metadata                 | Add metadata and preserve content.                              |
| The artifact conflicts with approved upstream decisions | Ask before replacing.                                           |
| The user explicitly asks for a full rewrite             | Rewrite, preserving decisions in the changelog when applicable. |
| New product behavior or scope appears                   | Update PRD/spec first.                                          |
| New technical capability appears                        | Update design/tasks first.                                      |
| Only checklist or evidence changed                      | Update tasks/apply-progress/verify only.                        |

**Incorrect:**

```md
Regenerate the entire spec from scratch because a minor clarification appeared.
```

**Correct:**

```md
Read the existing spec, preserve approved decisions, update the affected section, and append a
Change Log entry.
```
