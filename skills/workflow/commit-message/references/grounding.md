---
title: Ground the Message in Real Evidence
impact: HIGH
impactDescription: A speculative message misrepresents the change and erodes review trust
tags: grounding, diff, conventions
---

## Ground the Message in Real Evidence

**Impact: HIGH (A speculative message misrepresents the change and erodes review trust)**

The commit message describes what actually changed. Filenames, branch names, and memory are clues,
not evidence. Always read the real `git diff` first, then draft the message from what you saw there.
Never invent identifiers the diff does not show.

**Incorrect (drafts a message from the filename alone, never inspecting the diff):**

```text
feat(auth): add login form
```

```bash
# Filename hint: src/auth/login-form.tsx
# What the agent did: wrote a header from the filename and never ran git diff.
```

**Correct (inspects the real diff and grounds the header in what it shows):**

```bash
git status
git diff
```

```text
feat(auth): add login form with rate limiting

Add rate limiting (5 attempts per minute) to the login endpoint and surface a
generic error to the user when the limit is hit.
```

**Incorrect (invents an issue ID and a product name not present in the diff):**

```text
fix(autana-7421): resolve AutanaCRM session timeout
```

**Correct (drops the invented IDs; describes the actual behavior change):**

```text
fix(sessions): keep session alive across token refresh
```

**Incorrect (invents a project-specific rule like `type(JIRA-1234): description`):**

```text
ENG-1234(sessions): rotate refresh tokens on every login
```

**Correct (uses the Conventional Commit format already visible in `git log`):**

```text
feat(sessions): rotate refresh tokens on every login

# Verify the repo convention with:
git log --oneline -20
```

Reference: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
