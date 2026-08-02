# NestJS Practices

This inventory covers the active atomic decision cards for NestJS architecture and runtime work. The
entry point, `SKILL.md`, handles activation and task-time routing; this file is for catalog review
and maintenance.

## Structure

- `SKILL.md` - Activation and rule index.
- `references/` - Active atomic rule cards.

## Domains and Prefixes

| Prefix      | Domain                                             |
| ----------- | -------------------------------------------------- |
| `test-e2e-` | Real HTTP E2E testing decisions                    |
| `config-`   | Configuration placement, validation, and injection |
| `arch-`     | Application structure and process boundaries       |
| `error-`    | Errors and observability                           |
| `api-`      | External service contracts                         |
| `nestjs-`   | NestJS and Drizzle integration                     |

## E2E Cards

- `references/test-e2e-replicate-production-bootstrap.md` - Replicate the production bootstrap in
  E2E tests
- `references/test-e2e-use-real-dependencies.md` - Exercise real application dependencies in E2E
  tests
- `references/test-e2e-own-shared-context-lifecycle.md` - Own shared E2E context and lifecycle in
  the orchestrator
- `references/test-e2e-organize-suites-by-size.md` - Organize E2E suites by flow and discovery rules
- `references/test-e2e-derive-invalid-payloads.md` - Derive invalid E2E payloads from canonical
  valid constants
- `references/test-e2e-assert-public-contracts.md` - Assert explicit public contracts in E2E tests

## Configuration Cards

- `references/config-place-files-under-src-config.md` - Place configuration files under src/config
- `references/config-use-namespaced-register-as-factories.md` - Use namespaced registerAs factories
- `references/config-validate-environment-with-zod.md` - Validate environment with Zod
- `references/config-register-configuration-in-app-module.md` - Register configuration in AppModule
- `references/config-inject-namespaced-configuration.md` - Inject namespaced configuration
- `references/config-prevent-direct-environment-access.md` - Prevent direct environment access
- `references/config-avoid-hardcoded-secrets.md` - Avoid hardcoded secrets

## Architecture Cards

- `references/arch-use-flow-coordinators.md` - Use flow coordinators for cross-module workflows
- `references/arch-service-repository-responsibility.md` - Keep services focused on one domain
- `references/arch-use-repository-pattern.md` - Use repositories for Drizzle persistence access
- `references/arch-use-standalone-application.md` - Use a standalone NestJS application context

## Errors and Observability Cards

- `references/error-use-structured-logging.md` - Use structured runtime logging
- `references/error-handle-unknown-catches.md` - Handle caught errors as unknown

## External Contract Cards

- `references/api-use-external-service-contracts.md` - Validate external service contracts

## NestJS and Drizzle Integration Cards

- `references/nestjs-use-drizzle-database-module.md` - Provide Drizzle through a NestJS database
  module

## Maintenance

1. Confirm that a proposed rule belongs to NestJS rather than TypeScript, Zod, or Drizzle.
2. Add or update an atomic card in `references/`.
3. Use an accepted impact, at most four tags, focused examples, and an official HTTPS source.
4. Update `SKILL.md` and this inventory when the catalog changes.
