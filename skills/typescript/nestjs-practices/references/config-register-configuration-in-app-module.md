---
title: Register configuration in AppModule
impact: HIGH
impactDescription: Ensures configuration is loaded and validated during bootstrap
tags: nestjs, configuration, app-module, bootstrap
---

## Register configuration in AppModule

**Impact: HIGH (ensures configuration is loaded and validated during bootstrap)**

Register configuration once in `AppModule` with `isGlobal`, the namespace `load` list, and the Zod
`validate` function so all modules start from validated configuration.

**Incorrect (loads a namespace without global access or validation):**

```typescript
ConfigModule.forRoot({
  load: [appConfig],
});
```

**Correct (wires global loading and validation in AppModule):**

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import appConfig from './config/app.config';
import { validate } from './config/env.validation';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [appConfig],
      validate,
    }),
  ],
})
export class AppModule {}
```

Load the factory described in
[Use namespaced registerAs factories](./config-use-namespaced-register-as-factories.md) and the
validator described in [Validate environment with Zod](./config-validate-environment-with-zod.md).

Reference: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
