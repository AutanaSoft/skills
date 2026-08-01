---
title: Prevent direct environment access
impact: HIGH
impactDescription: Prevents hidden runtime dependencies in business services
tags: nestjs, configuration, environment, services
---

## Prevent direct environment access

**Impact: HIGH (prevents hidden runtime dependencies in business services)**

Read `process.env` only in configuration factories and environment validation. Business services
receive validated configuration through dependency injection instead of reading process state.

**Incorrect (a business service reads the environment directly):**

```typescript
class BillingService {
  getCurrency() {
    return process.env.DEFAULT_CURRENCY ?? 'USD';
  }
}
```

**Correct (a business service receives configuration through injection):**

```typescript
type BillingConfig = {
  currency: string;
};

class BillingService {
  constructor(private readonly config: BillingConfig) {}

  getCurrency() {
    return this.config.currency;
  }
}
```

For a concrete namespaced dependency, use
[typed configuration injection](./config-inject-namespaced-configuration.md).

Reference: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
