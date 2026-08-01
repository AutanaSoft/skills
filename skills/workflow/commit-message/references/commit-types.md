---
title: Conventional Commit Types and Scope Inference
impact: MEDIUM
impactDescription: The right type makes release notes, changelogs, and scope filters accurate
tags: types, scope, conventional-commit
---

## Conventional Commit Types and Scope Inference

**Impact: MEDIUM (The right type makes release notes, changelogs, and scope filters accurate)**

Pick the `type` from the observed change, not from intent. The same change has one correct type:
`fix` for a bug, `feat` for a new capability, `refactor` for behavior-preserving cleanup. Use the
scope to name the affected module, not to summarize the change.

### Conventional Commit Types

| Type       | Use for                                             |
| ---------- | --------------------------------------------------- |
| `feat`     | A new feature                                       |
| `fix`      | A bug fix                                           |
| `docs`     | Documentation only changes                          |
| `style`    | Formatting-only changes that do not affect behavior |
| `refactor` | Code change that is neither a fix nor a feature     |
| `perf`     | Performance improvements                            |
| `test`     | Add or update tests                                 |
| `build`    | Build system or dependency changes                  |
| `ci`       | CI configuration or pipeline changes                |
| `chore`    | Other maintenance changes                           |
| `revert`   | Revert a previous commit                            |

**Correct (`feat` example with a specific module scope):**

```text
feat(sessions): implement refresh token rotation

Add token family tracking and invalidate previous refresh tokens on rotation.
Improve session security by detecting token reuse.
```

**Correct (`refactor` example with `BREAKING CHANGE:` footers for contract changes):**

```text
refactor(api): align update and verification response contracts

Standardize service output validation with safeParse and improve persistence error mapping reuse.
Move Prisma error translation into shared database utilities for cross-module adoption.

BREAKING CHANGE: PATCH /resources/:id now returns the updated resource payload.
BREAKING CHANGE: Verification endpoints now return 204 with no response body.
```

**Correct (`chore` example with a short, well-fitted header):**

```text
chore(ui): align dashboard header typography

Match section title weight with the design tokens and drop the legacy uppercase variant from the
shared typography helper.
```

**Incorrect (infers a vague `core` scope when a precise module name is in the path):**

```text
fix(core): reject expired refresh tokens
```

The diff only touches `src/auth/token.ts`; `core` hides the real affected module.

**Correct (uses the module name from the diff path):**

```text
fix(auth): reject expired refresh tokens
```

### Scope Inference Heuristics

If scope is not provided, infer it from staged paths without assuming a specific project layout:

- A single package, app, or workspace path -> the nearest meaningful directory name.
- A single feature or module path -> the feature or module name from the path.
- Documentation-only changes -> `docs`.
- Test-only changes -> `test`.
- Build, dependency, or tooling config changes -> `build`, `ci`, or `tooling`.
- Multiple related areas for one feature -> use the feature or public API name.
- Multiple unrelated areas -> choose `core` only when no more precise neutral scope exists.

Reference: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
