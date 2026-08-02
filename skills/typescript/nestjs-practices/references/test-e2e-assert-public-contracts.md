---
title: Assert explicit public contracts in E2E tests
impact: CRITICAL
impactDescription: Detects response-shape regressions and accidental exposure of sensitive fields
tags: nestjs, e2e, api-contract, security
---

## Assert explicit public contracts in E2E tests

**Impact: CRITICAL (detects response-shape regressions and accidental exposure of sensitive
fields)**

### Rule

Assert the status code and the explicit public response structure for every important HTTP outcome.
Assert the absence of sensitive fields such as passwords, password hashes, and internal secrets.
Treat tokens as public only when the endpoint intentionally returns them as part of its contract.

### Why it matters

- A successful status does not prove that serialization exposes the right fields or hides secrets.
- Partial or opaque assertions can allow accidental contract changes to pass review.
- Explicit absence checks make a security expectation executable.
- Focused structural matchers expose meaningful API changes without freezing irrelevant timestamps,
  generated IDs, or other volatile fields.

### Exceptions and limits

- Replace illustrative fields with the actual public contract of the endpoint under test.
- For a large response, use explicit structural matchers or a public schema, then keep separate
  assertions for forbidden fields. Do not use an opaque snapshot as the only contract assertion.
- A login endpoint may intentionally return an access token. Assert its documented shape there,
  while asserting that unrelated endpoints do not expose tokens or internal secrets.
- For invalid input, assert the status and the documented error body structure without depending on
  unrelated volatile details.

### Examples

**Incorrect (checks status while hiding the response contract):**

```typescript
const response = await httpClient.post('/users', { body: payload });

expect(response.statusCode).toBe(201);
expect(response.body).toMatchSnapshot();
```

**Correct (checks public shape, forbidden fields, and invalid response contract):**

```typescript
const response = await httpClient.post('/users', { body: payload });

expect(response.statusCode).toBe(201);
expect(response.body).toEqual(
  expect.objectContaining({
    id: expect.any(String),
    email: payload.email,
    status: 'active',
  }),
);
expect(response.body).not.toHaveProperty('password');
expect(response.body).not.toHaveProperty('passwordHash');
expect(response.body).not.toHaveProperty('internalSecret');
expect(response.body).not.toHaveProperty('accessToken'); // This endpoint does not return a token.

const invalidResponse = await httpClient.post('/users', {
  body: { ...payload, email: '' },
});

expect(invalidResponse.statusCode).toBe(400);
expect(invalidResponse.body).toEqual(
  expect.objectContaining({
    statusCode: 400,
    message: expect.anything(),
    error: expect.any(String),
  }),
);
expect(invalidResponse.body).not.toHaveProperty('passwordHash');
```

The HTTP client and matcher syntax are illustrative. Keep assertions aligned with the project's
runner and endpoint schemas, and omit volatile fields unless they are part of the public contract.

### Related cards

- [Exercise real application dependencies in E2E tests](./test-e2e-use-real-dependencies.md)
- [Derive invalid E2E payloads from canonical valid constants](./test-e2e-derive-invalid-payloads.md)
- [Validate external service contracts](./api-use-external-service-contracts.md)

### References

- [NestJS serialization](https://docs.nestjs.com/techniques/serialization)
- [NestJS unit testing](https://docs.nestjs.com/fundamentals/unit-testing)
- [Jest expect matchers](https://jestjs.io/docs/expect)
