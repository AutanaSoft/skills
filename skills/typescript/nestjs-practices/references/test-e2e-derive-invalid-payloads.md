---
title: Derive invalid E2E payloads from canonical valid constants
impact: HIGH
impactDescription: Keeps invalid cases isolated and prevents fixture contamination between tests
tags: nestjs, e2e, fixtures, validation
---

## Derive invalid E2E payloads from canonical valid constants

**Impact: HIGH (keeps invalid cases isolated and prevents fixture contamination between tests)**

### Rule

Define canonical valid payload constants or factories and derive every invalid case from a local
copy. Change only the property that represents the scenario under test. Never mutate the canonical
fixture or reuse a mutable invalid object across tests.

### Why it matters

- Starting from a valid payload isolates the reason a validation request should fail.
- Shared canonical data keeps setup and request examples aligned and reduces fixture drift.
- Local copies prevent one test's mutation from changing later requests or making results depend on
  execution order.

### Exceptions and limits

- Object and array spread create shallow copies. A top-level spread does not copy nested objects or
  arrays.
- A shallow copy is safe when changing a first-level property or replacing the entire nested branch.
  When changing a nested value, copy every modified level explicitly or use a factory that creates
  fresh nested values.
- Use a factory when fields must be unique per execution. Do not treat JSON serialization as a
  universal deep-clone strategy because it changes supported values and can hide the intended shape.

### Examples

**Incorrect (mutates the canonical nested fixture):**

```typescript
const VALID_USER_PAYLOAD = {
  email: 'user@example.test',
  password: 'test-password',
  profile: { displayName: 'Test User', roles: ['member'] },
};

VALID_USER_PAYLOAD.profile.displayName = '';
const invalidUserPayload = VALID_USER_PAYLOAD;
```

**Correct (copies the changed boundary locally):**

```typescript
type UserPayload = {
  email: string;
  password: string;
  profile: { displayName: string; roles: string[] };
};

export const VALID_USER_PAYLOAD: UserPayload = {
  email: 'user@example.test',
  password: 'test-password',
  profile: { displayName: 'Test User', roles: ['member'] },
};

export const createValidUserPayload = (): UserPayload => ({
  email: VALID_USER_PAYLOAD.email,
  password: VALID_USER_PAYLOAD.password,
  profile: {
    ...VALID_USER_PAYLOAD.profile,
    roles: [...VALID_USER_PAYLOAD.profile.roles],
  },
});

const invalidEmail = { ...createValidUserPayload(), email: '' };
const validPayload = createValidUserPayload();
const invalidDisplayName = {
  ...validPayload,
  profile: { ...validPayload.profile, displayName: '' },
};
```

The first variant needs only a top-level spread. The nested variant copies `profile` explicitly, so
the canonical payload and its nested arrays remain unchanged.

### Related cards

- [Organize E2E suites by flow and discovery rules](./test-e2e-organize-suites-by-size.md)
- [Assert explicit public contracts in E2E tests](./test-e2e-assert-public-contracts.md)

### References

- [MDN spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
- [NestJS validation](https://docs.nestjs.com/techniques/validation)
