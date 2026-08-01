---
title: Inject namespaced configuration
impact: HIGH
impactDescription: Preserves typed and explicit configuration dependencies
tags: nestjs, configuration, dependency-injection, typescript
---

## Inject namespaced configuration

**Impact: HIGH (preserves typed and explicit configuration dependencies)**

Inject a single known namespace with `@Inject(config.KEY)` and `ConfigType`. Reserve `ConfigService`
for dynamic lookup or consumers that genuinely need multiple namespaces.

**Incorrect (uses ConfigService for one known namespace):**

```typescript
constructor(private readonly configService: ConfigService) {}

getPort() {
  return this.configService.get<number>("app.port")
}
```

**Correct (injects the known namespace with its inferred type):**

```typescript
import { Inject, Injectable } from '@nestjs/common';
import type { ConfigType } from '@nestjs/config';
import appConfig from './config/app.config';

@Injectable()
export class HttpServer {
  constructor(
    @Inject(appConfig.KEY)
    private readonly config: ConfigType<typeof appConfig>,
  ) {}

  getPort() {
    return this.config.port;
  }
}
```

The injected namespace comes from
[the registered configuration factory](./config-use-namespaced-register-as-factories.md).

Reference: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)
