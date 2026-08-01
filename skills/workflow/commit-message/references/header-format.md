---
title: Header Format
impact: CRITICAL
impactDescription: A malformed header breaks parsing, changelog generation, and review tooling
tags: header, conventional-commit, scope, breaking-change
---

## Header Format

**Impact: CRITICAL (A malformed header breaks parsing, changelog generation, and review tooling)**

The header is the only line many tools parse. A missing scope, an oversized line, or a missing
`BREAKING CHANGE` footer silently breaks changelog generators, semver tooling, and code review
searches.

A valid header is `type(scope): description` with a mandatory scope, a total length at or under 100
characters, and one or more `BREAKING CHANGE:` footers whenever the change alters an API or response
contract.

**Incorrect (drops the mandatory scope):**

```text
feat: implement refresh token rotation
```

**Correct (mandatory scope inside the parentheses):**

```text
feat(sessions): implement refresh token rotation
```

**Incorrect (breaking contract change with no scope and no `BREAKING CHANGE:` footer):**

```text
refactor: align update and verification response contracts
```

**Correct (specific scope plus a `BREAKING CHANGE:` footer for each contract change):**

```text
refactor(api): align update and verification response contracts

Standardize service output validation with safeParse and improve persistence error mapping reuse.
Move Prisma error translation into shared database utilities for cross-module adoption.

BREAKING CHANGE: PATCH /resources/:id now returns the updated resource payload.
BREAKING CHANGE: Verification endpoints now return 204 with no response body.
```

**Correct (chore example: short, well-fitted header at 44 characters):**

```text
chore(ui): align dashboard header typography

Match section title weight with the design tokens and drop the legacy uppercase variant from the
shared typography helper.
```

Reference: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
