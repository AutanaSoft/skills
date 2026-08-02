---
title: Replicate the production bootstrap in E2E tests
impact: CRITICAL
impactDescription: Prevents green tests from exercising a runtime different from production
tags: nestjs, e2e, bootstrap, fastify
---

## Replicate the production bootstrap in E2E tests

**Impact: CRITICAL (prevents green tests from exercising a runtime different from production)**

### Rule

Acquire the application through a shared `getAppInstance`-style test utility. Build it from the same
production root module and mirror the production HTTP adapter, global pipes, global prefix, and
request or correlation ID behavior when those features exist. Treat `FastifyAdapter` and
`ZodValidationPipe` as conditional examples, not NestJS-wide requirements.

The acquisition utility owns initialization and adapter readiness. It does not silently decide who
closes a shared application; the context and lifecycle owner must define that contract in
[Own shared E2E context and lifecycle in the orchestrator](./test-e2e-own-shared-context-lifecycle.md).

### Why it matters

- The adapter can change request injection, serialization, hooks, and shutdown behavior.
- Global pipes and prefixes determine which routes and validation rules the HTTP client actually
  sees.
- Request or correlation IDs affect middleware behavior and the diagnostic context available during
  a failure.
- A cached initialization promise prevents concurrent suites from creating competing infrastructure
  instances.

### Exceptions and limits

- Use the adapter and global features that production actually configures. If production uses a
  different adapter or no global pipe, reproduce that choice instead of adding Fastify or Zod for
  convenience.
- A test that intentionally examines an alternate bootstrap must declare that scope and must not
  masquerade as the shared production-like E2E application.
- Call `init()` and any adapter-specific readiness operation before returning the app. Leave close,
  cache reset, and ownership to the lifecycle contract.

### Examples

**Incorrect (creates a divergent application for one suite):**

```typescript
const testingModule = await Test.createTestingModule({
  imports: [FeatureModule],
}).compile();

const app = testingModule.createNestApplication();
// Production uses a different root module, adapter, global validation, and prefix.
await app.init();
```

**Correct (shares a production-derived bootstrap):**

```typescript
let appPromise: Promise<INestApplication> | undefined;

export function getAppInstance(): Promise<INestApplication> {
  appPromise ??= createProductionLikeApp();
  return appPromise;
}

async function createProductionLikeApp(): Promise<INestApplication> {
  const app = await NestFactory.create(
    AppModule,
    new FastifyAdapter(), // Include only when production uses Fastify.
  );

  app.useGlobalPipes(new ZodValidationPipe()); // Include only when production uses this pipe.
  app.setGlobalPrefix('api'); // Include only when production sets this prefix.
  configureRequestOrCorrelationId(app); // Include only when production installs this behavior.

  await app.init();
  await app.getHttpAdapter().getInstance().ready(); // Only for an adapter that requires readiness.
  return app;
}
```

The example is illustrative: replace `AppModule`, the adapter, pipes, prefix, ID configuration, and
readiness operation with the decisions in the real production bootstrap. Do not call `app.close()`
in this acquisition function.

### Related cards

- [Exercise real application dependencies in E2E tests](./test-e2e-use-real-dependencies.md)
- [Own shared E2E context and lifecycle in the orchestrator](./test-e2e-own-shared-context-lifecycle.md)
- [Use structured runtime logging](./error-use-structured-logging.md)

### References

- [NestJS unit testing](https://docs.nestjs.com/fundamentals/unit-testing)
- [Fastify testing](https://fastify.dev/docs/latest/Guides/Testing/)
- [Fastify server lifecycle](https://fastify.dev/docs/latest/Reference/Server/)
