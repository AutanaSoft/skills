---
title: Own shared E2E context and lifecycle in the orchestrator
impact: HIGH
impactDescription: Prevents order-dependent suites, leaked state, and premature application shutdown
tags: nestjs, e2e, lifecycle, test-context
---

## Own shared E2E context and lifecycle in the orchestrator

**Impact: HIGH (prevents order-dependent suites, leaked state, and premature application shutdown)**

### Rule

Define a typed shared context for identifiers, credentials or tokens, and created state. In a
composed suite, the orchestrator owns setup, deterministic cleanup, and the singleton application's
close and cache reset when it owns that application. Clean dependent resources in reverse creation
order. Pass the context to sub-suites; sub-suites never close the global app.

### Why it matters

- A typed context makes data dependencies visible instead of hiding them in global records.
- Reverse-order cleanup respects relationships such as child records depending on a parent.
- One owner prevents one sub-suite from closing an application still needed by another suite.
- Resetting a closed singleton prevents later callers from receiving a stale application or a
  rejected initialization promise.

### Exceptions and limits

- Prefer independent tests. Share state only when its creation is deliberately part of the E2E flow
  and the dependency is easier to verify as one orchestrated scenario.
- If the test harness owns the application lifecycle, the orchestrator cleans data but does not call
  `app.close()`.
- If a shared `getAppInstance` utility exposes closure, its close operation must also clear the
  cached instance or promise before another suite can acquire it.
- Never print passwords, access tokens, refresh tokens, or other secrets in logs, failure messages,
  or reports. Log stable identifiers only after confirming they are safe.

### Examples

**Incorrect (untyped global state and competing lifecycle owners):**

```typescript
const context: Record<string, any> = {};

beforeAll(async () => {
  context.app = await getAppInstance();
  context.token = 'secret-token';
});

describe('users', () => {
  afterAll(async () => {
    await context.app.close();
  });
});

afterAll(async () => {
  await context.app.close();
});
```

**Correct (the orchestrator owns typed state, cleanup, and closure):**

```typescript
type Cleanup = () => Promise<void>;

interface E2EContext {
  app: INestApplication;
  userId: string;
  credentials: { email: string; password: string };
  accessToken: string;
  created: Array<{ label: string; cleanup: Cleanup }>;
}

let context: E2EContext;
let ownsApp = false;

beforeAll(async () => {
  const app = await getAppInstance();
  ownsApp = !isHarnessOwnedApp();
  context = await createE2EContext(app);
});

afterAll(async () => {
  try {
    for (const resource of [...context.created].reverse()) {
      await resource.cleanup();
    }
  } finally {
    if (ownsApp) {
      await closeAppInstanceAndReset();
    }
  }
});

registerUserSuite(() => context); // Sub-suites resolve context after setup and never close the app.
```

The helpers are project-defined. `closeAppInstanceAndReset` is the sole singleton close path, and
`createE2EContext` must not log the credential or token fields.

### Related cards

- [Replicate the production bootstrap in E2E tests](./test-e2e-replicate-production-bootstrap.md)
- [Organize E2E suites by flow and discovery rules](./test-e2e-organize-suites-by-size.md)
- [Exercise real application dependencies in E2E tests](./test-e2e-use-real-dependencies.md)

### References

- [Jest setup and teardown](https://jestjs.io/docs/setup-teardown)
- [NestJS unit testing](https://docs.nestjs.com/fundamentals/unit-testing)
- [Fastify server lifecycle](https://fastify.dev/docs/latest/Reference/Server/)
