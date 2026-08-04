---
title: Build and validate namespaced configuration
impact: HIGH
impactDescription:
  Prevents partial, inconsistent, or invalid runtime configuration from reaching application
  consumers.
tags: nestjs, configuration, validation, register-as
---

## Build and validate namespaced configuration

**Impact: HIGH (prevents partial, inconsistent, or invalid runtime configuration from reaching
application consumers)**

Give each namespace a short, stable semantic name and keep its file, namespace, and exported type
aligned. The factory must construct the complete final object, including required values, defaults,
explicit overrides, transformations, and derived values. Apply this precedence: defaults, defined
overrides, transformations or derived values, then one final validation of the complete object.

Determine whether an override is present with an explicit `undefined` check rather than truthiness;
an empty value may be invalid and must not silently select a default. Keep the rule independent of a
particular validation library; the example uses Zod because it is a common implementation. The
factory owns the authoritative validation for its namespace. A global `validate` function passed to
`ConfigModule.forRoot` is optional and complementary: use it for cross-namespace invariants, shared
globals, aggregate reporting, or an established project convention, never to duplicate a namespace
schema. Configuration contracts should be read-only. Do not put request data, domain state, or
mutable runtime settings in a bootstrap configuration namespace.

**Incorrect (returns partial environment input and uses truthiness for a default):**

```typescript
import { registerAs } from '@nestjs/config';

export default registerAs('payments', () => ({
  apiUrl: process.env.PAYMENTS_API_URL,
  timeoutMs: process.env.PAYMENTS_TIMEOUT_MS || 5_000,
}));
```

**Correct (builds the complete namespace and validates it once at the boundary):**

```typescript
import { registerAs } from '@nestjs/config';
import { z } from 'zod';

export const paymentsSchema = z
  .object({
    apiUrl: z.string().url(),
    timeoutMs: z.number().int().positive(),
    requestPath: z.string().startsWith('/'),
    endpoint: z.string().url(),
  })
  .readonly();

export type PaymentsConfig = Readonly<z.infer<typeof paymentsSchema>>;

export default registerAs('payments', (): PaymentsConfig => {
  const apiUrlOverride = process.env.PAYMENTS_API_URL;
  const pathOverride = process.env.PAYMENTS_PATH;
  const timeoutOverride = process.env.PAYMENTS_TIMEOUT_MS;

  const apiUrl = apiUrlOverride === undefined ? undefined : apiUrlOverride.trim();
  const requestPath = pathOverride === undefined ? '/v1/payments' : pathOverride.trim();
  const timeoutMs = timeoutOverride === undefined ? 5_000 : Number(timeoutOverride);

  const candidate = {
    apiUrl,
    timeoutMs,
    requestPath,
    endpoint: apiUrl === undefined ? undefined : `${apiUrl.replace(/\/$/, '')}${requestPath}`,
  };

  return paymentsSchema.parse(candidate);
});
```

Register the namespace in the application context described by
[Register configuration per application context](./config-register-configuration-per-application-context.md)
and inject it through the typed contract described by
[Inject typed namespaced configuration](./config-inject-namespaced-configuration.md).

References:

- [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
- [Zod documentation](https://zod.dev/)
