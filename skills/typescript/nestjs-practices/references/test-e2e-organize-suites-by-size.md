---
title: Organize E2E suites by flow and discovery rules
impact: MEDIUM
impactDescription: Keeps suites reviewable without accidental double execution
tags: nestjs, e2e, test-organization, test-discovery
---

## Organize E2E suites by flow and discovery rules

**Impact: MEDIUM (keeps suites reviewable without accidental double execution)**

### Rule

Keep a small E2E suite in one project-appropriate E2E file. For a large module with several flows,
use one E2E orchestrator that explicitly registers focused sub-suites. Choose sub-suite locations
and names only after inspecting the project's actual discovery patterns, roots, and configuration.

Do not assume that a suffix such as `*.spec.ts` is ignored. A file imported by the orchestrator may
also be discovered and executed independently, causing duplicate setup, data collisions, and cleanup
competition.

### Why it matters

- A single file keeps a small flow understandable without ceremonial structure.
- An orchestrator gives larger modules one owner for setup, context, and cleanup while preserving
  focused flow-level files.
- Discovery configuration is part of the test architecture; overlapping patterns can run the same
  assertions twice even when imports look intentional.

### Exceptions and limits

- Do not split a small suite merely to imitate another repository's layout.
- Inspect the runner's actual `testMatch`, `testRegex`, roots, ignore patterns, and project commands
  before composing files. Use the equivalent concepts for a non-Jest runner.
- If a sub-suite is discovered independently, move it to an excluded location, change the local
  pattern, or adjust the project configuration according to its established conventions.
- Never rely on incidental file order to provide shared state. The orchestrator must make
  registration and lifecycle ownership explicit.

### Examples

**Incorrect (the orchestrator imports a file the runner also discovers):**

```typescript
// Illustrative runner configuration discovers both patterns.
const testMatch = ['**/*.e2e-spec.ts', '**/*.spec.ts'];

// users.e2e-spec.ts
import './users-login.spec';

// users-login.spec.ts is both imported above and discovered as its own suite.
```

**Correct (composition follows inspected project configuration):**

```typescript
// Inspection of this project's E2E project found:
// - discovered files: **/*.e2e-spec.ts
// - test/e2e-suites/ is excluded from that discovery pattern
// The actual runner configuration, not this comment, is the source of truth.
import { registerUsersLoginSuite } from './e2e-suites/users-login.spec';
import { registerUsersProfileSuite } from './e2e-suites/users-profile.spec';

describe('users E2E', () => {
  let context: E2EContext;

  beforeAll(async () => {
    context = await createE2EContext(await getAppInstance());
  });

  registerUsersLoginSuite(() => context);
  registerUsersProfileSuite(() => context);

  afterAll(() => cleanupAndCloseOwnedContext(context));
});
```

The suffixes, discovery patterns, and configuration keys above are illustrative. Preserve the
project's runner and naming conventions after verifying how it discovers files.

### Related cards

- [Own shared E2E context and lifecycle in the orchestrator](./test-e2e-own-shared-context-lifecycle.md)
- [Derive invalid E2E payloads from canonical valid constants](./test-e2e-derive-invalid-payloads.md)

### References

- [Jest configuration](https://jestjs.io/docs/configuration)
- [Jest setup and teardown](https://jestjs.io/docs/setup-teardown)
