---
title: Safety Boundaries
impact: CRITICAL
impactDescription: Destructive Git commands, empty commits, and secret leaks are hard to undo
tags: safety, git, secrets, hooks
---

## Safety Boundaries

**Impact: CRITICAL (Destructive Git commands, empty commits, and secret leaks are hard to undo)**

A commit is permanent history. Destructive operations, empty commits, secret-bearing files, and
bypassed hooks turn a routine commit into data loss, a leaked credential, or a broken review
pipeline. Pause and confirm before any of these moves.

**Incorrect (runs a destructive reset without an explicit ask):**

```bash
git reset --hard origin/main
```

**Correct (confirms the intent before running a destructive command):**

```bash
# Ask: "Confirm: discard all local commits and match origin/main? Type 'yes' to proceed."
# Wait for explicit "yes", then:
git reset --hard origin/main
```

**Incorrect (creates an empty commit to silence a hook):**

```bash
git commit --allow-empty -m "chore: trigger CI"
```

**Correct (no commit when there is no change; report the situation instead):**

```bash
# Detect no staged changes with `git status`; do not run `git commit`.
# Report: "Nothing to commit; the working tree is clean."
```

**Incorrect (commits a `.env` file that may contain secrets):**

```bash
git add .env
git commit -m "feat: load env config"
```

**Correct (warns and excludes the file, then adds the rest):**

```bash
# Detect a secret-bearing file in `git status`.
# Warn: ".env may contain secrets. Add it to .gitignore instead."
git add .gitignore src/config.ts
git commit -m "feat: load env config from .env"
```

**Incorrect (bypasses a failed hook to push the commit through):**

```bash
git commit --no-verify -m "feat: ship it"
```

**Correct (reports the hook failure and stops for human review):**

```bash
# Detect a non-zero exit from pre-commit or commit-msg.
# Report: "Hook '<name>' failed: <output>. Fix the reported issue or ask the user before
# bypassing with --no-verify."
```

Reference: [Git — git-commit documentation](https://git-scm.com/docs/git-commit)
