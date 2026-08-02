---
title: Exercise real application dependencies in E2E tests
impact: CRITICAL
impactDescription: Preserves the real domain, application, persistence, and authentication flow
tags: nestjs, e2e, dependency-injection, authentication
---

## Exercise real application dependencies in E2E tests

**Impact: CRITICAL (preserves the real domain, application, persistence, and authentication flow)**

### Rule

Resolve setup providers from the production application container and exercise public HTTP endpoints
with a real client. Prepare users and records through production repository or service capabilities,
then perform the real login or authentication flow instead of assigning a token or mocking the
application service under test.

Use project-defined DI tokens and capabilities such as `USER_REPOSITORY` and `PASSWORD_HASHER` in
examples. The rule is independent of the ORM, HTTP client library, test runner, and package manager.

### Why it matters

- Real providers verify module wiring, persistence, hashing, validation, authorization, and response
  serialization together.
- Real authentication proves that credentials travel through the same endpoint, guards, and token
  handling used by consumers.
- Mocking domain or application services can make a test pass while the production dependency graph
  is broken.
- Capability-based provider access keeps the setup portable across database and repository
  implementations.

### Exceptions and limits

- A double is acceptable only when the user requests it or when an external boundary is
  nondeterministic, destructive, expensive, or unavailable.
- Replace only that external adapter. Keep the controller or endpoint, guards, application logic,
  persistence, and other local flow real when those are part of the behavior under test.
- Report the substituted boundary, the reason for substitution, and the real flow that remains
  covered. If no boundary was substituted, report that explicitly.
- Use an isolated test resource when the real provider requires one; do not bypass provider
  invariants merely to shorten setup.

### Examples

**Incorrect (mocks internal logic and skips authentication):**

```typescript
const userService = app.get(UserService);
jest.spyOn(userService, 'create').mockResolvedValue({ id: 'user-1' });

const response = await httpClient.get('/users/user-1', {
  headers: { authorization: 'Bearer already-issued-token' },
});
```

**Correct (uses production providers and the real login endpoint):**

```typescript
const userRepository = app.get<UserRepository>(USER_REPOSITORY);
const passwordHasher = app.get<PasswordHasher>(PASSWORD_HASHER);
const credentials = {
  email: 'e2e-user@example.test',
  password: 'test-password',
};

const passwordHash = await passwordHasher.hash(credentials.password);
const user = await userRepository.create({
  email: credentials.email,
  passwordHash,
});

const loginResponse = await httpClient.post('/auth/login', {
  body: credentials,
});
const accessToken = loginResponse.body.accessToken;

const response = await httpClient.get(`/users/${user.id}`, {
  headers: { authorization: `Bearer ${accessToken}` },
});
```

The client and response shape are illustrative. Use the project-defined client and public login
contract, but preserve the provider resolution and HTTP authentication sequence.

### Related cards

- [Replicate the production bootstrap in E2E tests](./test-e2e-replicate-production-bootstrap.md)
- [Own shared E2E context and lifecycle in the orchestrator](./test-e2e-own-shared-context-lifecycle.md)
- [Assert explicit public contracts in E2E tests](./test-e2e-assert-public-contracts.md)
- [Use repositories for Drizzle persistence access](./arch-use-repository-pattern.md)

### References

- [NestJS unit testing](https://docs.nestjs.com/fundamentals/unit-testing)
- [NestJS custom providers](https://docs.nestjs.com/fundamentals/custom-providers)
- [NestJS authentication](https://docs.nestjs.com/security/authentication)
