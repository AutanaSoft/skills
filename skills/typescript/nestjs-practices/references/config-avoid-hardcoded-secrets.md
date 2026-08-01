---
title: Avoid hardcoded secrets
impact: CRITICAL
impactDescription: Prevents credential exposure through source control and deployments
tags: nestjs, configuration, secrets, security
---

## Avoid hardcoded secrets

**Impact: CRITICAL (prevents credential exposure through source control and deployments)**

Do not place passwords, API keys, tokens, or private keys in source code. Load them from validated
runtime configuration so repositories and deployed artifacts do not contain credentials.

**Incorrect (embeds an API key in source code):**

```typescript
const client = new PaymentClient({
  apiKey: 'sk_live_example',
});
```

**Correct (receives the key from validated configuration):**

```typescript
type PaymentConfig = {
  apiKey: string;
};

const createClient = (config: PaymentConfig) =>
  new PaymentClient({
    apiKey: config.apiKey,
  });
```

The value must come from validated configuration as described in
[Validate environment with Zod](./config-validate-environment-with-zod.md).

Reference:
[OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
