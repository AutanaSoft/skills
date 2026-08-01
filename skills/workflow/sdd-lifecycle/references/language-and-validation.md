---
title: Respect SDD language and validation policy
impact: MEDIUM
impactDescription:
  Keeps documentation consistent and avoids expensive validation that was not requested
tags: validation, language, commands, operations
---

## Respect SDD language and validation policy

**Impact: MEDIUM (keeps documentation consistent and avoids expensive validation that was not
requested)**

Communication with the user must remain in Spanish, while SDD artifacts and generated technical
documentation must be written in English unless explicitly requested otherwise.

### Language Policy

- Write SDD artifacts, technical documentation, product documentation, comments, JSDoc, and code in
  English.
- Communicate with the developer/user in Spanish.
- If a question is needed, ask one question at a time with progress and context, then stop.

### Reference Validation Commands

```bash
pnpm --filter @repo/ui lint
pnpm --filter @repo/ui typecheck
pnpm --filter @repo/ui test

pnpm --filter web lint
pnpm --filter web typecheck
pnpm --filter web test
```

Do not run build unless the user explicitly requests it.
