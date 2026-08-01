---
title: Use namespaced registerAs factories
impact: HIGH
impactDescription: Provides stable, typed configuration boundaries
tags: nestjs, configuration, register-as, zod
---

## Use namespaced registerAs factories

**Impact: HIGH (provides stable, typed configuration boundaries)**

Export an explicit factory and register it with a stable namespace. Parse environment input in the
factory and infer the returned type from its schema so consumers receive typed configuration.

**Incorrect (uses an untyped inline factory and string values):**

```typescript
import { registerAs } from '@nestjs/config';

export default registerAs('app', () => ({
  port: process.env.PORT,
}));
```

**Correct (exports a typed parsing factory with a stable namespace):**

```typescript
import { registerAs } from '@nestjs/config';
import { z } from 'zod';

const appConfigSchema = z.object({
  port: z.coerce.number().int().positive().default(3000),
});

export type AppConfig = z.infer<typeof appConfigSchema>;

export const appConfigFactory = (): AppConfig =>
  appConfigSchema.parse({
    port: process.env.PORT,
  });

const appConfig = registerAs('app', appConfigFactory);

export default appConfig;
```

Place this factory in `src/config/<name>.config.ts` according to
[the file placement rule](./config-place-files-under-src-config.md).

Reference: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
