---
title: Place configuration files under src/config
impact: MEDIUM
impactDescription: Keeps configuration discoverable and consistently named
tags: nestjs, configuration, file-layout
---

## Place configuration files under src/config

**Impact: MEDIUM (keeps configuration discoverable and consistently named)**

Keep each configuration namespace in `src/config/<name>.config.ts`, where `<name>` is kebab-case.
This makes configuration easy to locate and separates it from application behavior.

**Incorrect (places a namespace outside the configuration directory):**

```typescript
// src/databaseConfig.ts
export const databaseConfig = {};
```

**Correct (uses the configuration directory and filename convention):**

```typescript
// src/config/database.config.ts
export const databaseConfig = {};
```

Pair this layout rule with
[Use namespaced registerAs factories](./config-use-namespaced-register-as-factories.md) when
implementing the file's contents.

Reference: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
