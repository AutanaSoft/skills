---
title: Use statuses, versioning, and changelog in SDD artifacts
impact: HIGH
impactDescription: Keeps traceability and makes it clear which artifacts are source of truth
tags: lifecycle, status, versioning, frontmatter, changelog
---

## Use statuses, versioning, and changelog in SDD artifacts

**Impact: HIGH (keeps traceability and makes it clear which artifacts are source of truth)**

SDD artifacts must declare their status, version, and relevant changes to prevent drafts from being
treated as implementation contracts.

### Allowed Statuses

| Status        | Meaning                                             |
| ------------- | --------------------------------------------------- |
| `draft`       | Generated or edited, not yet approved.              |
| `reviewed`    | Reviewed but not approved as source of truth.       |
| `approved`    | Accepted as source of truth for downstream phases.  |
| `in_progress` | Implementation or verification is actively running. |
| `implemented` | Implementation tasks are complete.                  |
| `verified`    | Verification passed.                                |
| `failed`      | Verification failed and requires follow-up.         |
| `archived`    | Change is closed and should not be edited casually. |
| `superseded`  | Replaced by a newer artifact or change.             |

### Versioning

Use semantic versioning for documents:

| Change  | When to Use                                                      |
| ------- | ---------------------------------------------------------------- |
| `0.x.x` | Draft or exploration.                                            |
| `1.0.0` | First approved baseline.                                         |
| `PATCH` | Editorial fixes with no meaning change.                          |
| `MINOR` | Compatible additions, clarifications, or technical capabilities. |
| `MAJOR` | Scope, product behavior, or public contract change.              |

Examples:

- Add verifiable criteria without changing behavior: `1.0.0` → `1.1.0`.
- Fix typos: `1.1.0` → `1.1.1`.
- Add sorting to a DataTable that explicitly excluded it: `1.1.0` → `2.0.0`.

### Frontmatter

```yaml
---
status: draft
version: 0.1.0
last_updated: 2026-05-02
change: data-table
artifact: prd
---
```

Recommended values for `artifact`:

- `idea`
- `prd`
- `component-spec`
- `page-spec`
- `design`
- `tasks`
- `apply-progress`
- `verify-report`
- `archive-report`

### Change Log

Every lifecycle-managed artifact should end with:

```md
## Change Log

| Version | Date       | Status | Summary                     |
| ------- | ---------- | ------ | --------------------------- |
| 0.1.0   | 2026-05-02 | draft  | Initial generated artifact. |
```

When updating, append a new row. Do not remove previous history.
