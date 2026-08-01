---
title: Eight-Step Commit Workflow
impact: MEDIUM
impactDescription: Following each step prevents skipped reviews, hidden scope, and rejected commits
tags: workflow, procedure, approval
---

## Eight-Step Commit Workflow

**Impact: MEDIUM (Following all eight steps prevents skipped reviews and rejected commits)**

A commit is the unit of review. The eight steps exist so that no step silently shapes the next:
inspect the diff, infer the type, draft the message, surface breaking changes, then ask before
running `git commit`. Skipping any step usually means a hidden assumption entered the message.

**Incorrect (skips inspection, drafts from filenames, and commits without approval):**

```bash
# What the agent did: read src/auth/login-form.tsx, drafted, and ran git commit in one move.
git add src/auth/login-form.tsx
git commit -m "feat: add login form"
```

**Correct (follows the 8 steps from `git status` to approved `git commit`):**

```bash
git status
git diff
git diff --staged
# (infer type and scope from the diff)
# (draft the message)
# (ask for approval)
git commit -m "feat(auth): add login form with rate limiting"
```

### The Eight Steps

1. Run `git status` to inspect modified, staged, and untracked files.
2. Run `git diff` to inspect unstaged changes.
3. Run `git diff --staged` when staged files exist.
4. Determine the best `type` and infer a concise `scope`.
5. Draft a clear commit message based on the observed changes.
6. Add body or footer when the change is non-trivial, cross-module, or includes behavioral or API
   impact.
7. If changes are breaking, include one or more `BREAKING CHANGE:` footer lines.
8. Display the proposed commit message and obtain explicit user approval, then run `git commit`.

### Example: Full Pass

```bash
git status
git diff --staged
```

```text
feat(sessions): implement refresh token rotation

Add token family tracking and invalidate previous refresh tokens on rotation.

BREAKING CHANGE: previous refresh tokens are invalidated on rotation.
```

```bash
# After explicit user approval:
git commit -F /tmp/commit-msg.txt
```

### Output Contract

Always return the same three pieces after a successful commit:

```text
- Message used: feat(sessions): implement refresh token rotation
- Commit: 1a2b3c4 feat(sessions): implement refresh token rotation
- Status: committed to <branch>
```

Reference: [Git — git-commit documentation](https://git-scm.com/docs/git-commit)
