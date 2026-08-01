---
title: Validate environment with Zod
impact: HIGH
impactDescription: Stops bootstrap when required environment input is invalid
tags: nestjs, configuration, zod, validation
---

## Validate environment with Zod

**Impact: HIGH (stops bootstrap when required environment input is invalid)**

Keep Zod validation in `src/config/env.validation.ts` and throw from `validate` when parsing fails.
When a project uses Zod, do not introduce a separate Joi-only validation path.

**Incorrect (returns invalid input and delegates validation to Joi):**

```typescript
import * as Joi from 'joi';

export const validate = (config: Record<string, unknown>) => config;
export const validationSchema = Joi.object({
  PORT: Joi.number().required(),
});
```

**Correct (parses environment input with Zod and fails bootstrap):**

```typescript
// src/config/env.validation.ts
import { z } from 'zod';

const envSchema = z.object({
  PORT: z.coerce.number().int().positive(),
});

export function validate(config: Record<string, unknown>) {
  const result = envSchema.safeParse(config);

  if (!result.success) {
    throw new Error(`Configuration validation error: ${result.error.message}`);
  }

  return result.data;
}
```

Register `validate` during bootstrap with
[AppModule configuration wiring](./config-register-configuration-in-app-module.md).

Reference: [Zod: Basic usage](https://zod.dev/basics)
