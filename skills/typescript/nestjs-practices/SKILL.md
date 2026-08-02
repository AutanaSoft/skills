---
name: nestjs-practices
description: >
  Apply NestJS practices for modules, services, repositories, dependency injection, configuration,
  bootstrap, logging and errors, external contracts, data integration, standalone application
  contexts, and real HTTP E2E tests. Trigger when creating, writing, reviewing, or refactoring
  NestJS E2E tests, including FastifyAdapter or test bootstrap, real providers, fixtures, HTTP
  authentication, shared lifecycle, payload variants, and public response assertions. Also use for
  NestJS configuration, architecture, observability, integrations, Drizzle, and standalone-context
  work. Do not use for generic TypeScript tests or E2E tests for non-NestJS applications.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.3.0'
---

# NestJS Practices

Apply the smallest relevant set of NestJS decision cards. The cards own the normative guidance,
examples, exceptions, and sources; this entry point only activates the catalog and routes the work.

## Activation Contract

- Load this skill for NestJS modules, services, repositories, dependency injection, configuration,
  bootstrap, logging and errors, external contracts, data integration, standalone application
  contexts, or real HTTP E2E tests.
- For E2E work, activate it when creating, writing, reviewing, or refactoring tests involving
  `FastifyAdapter`, test bootstrap, fixtures, HTTP authentication, shared lifecycle, payloads, or
  public response assertions.
- Do not activate it for generic TypeScript tests or E2E tests for applications that do not use
  NestJS.

## Hard Rules

- Load the card that owns each decision; do not copy a card's full rule, examples, exceptions, or
  sources into this entry point.
- Inspect the target project's existing bootstrap, runner discovery, configuration, and commands
  before choosing a structure. Preserve established conventions unless the requested change requires
  a migration.
- Keep adapters, ORMs, clients, runners, and package-manager commands project-dependent. For E2E,
  preserve real HTTP flows and real application providers unless a documented external-boundary
  exception applies.
- Keep credentials, tokens, and other secrets out of logs, reports, and generated examples.

## Workflow

1. Identify the NestJS concern and load only the matching cards in the decision map.
2. For E2E work, inspect the production root module and bootstrap, including the adapter, global
   pipes, prefix, and request or correlation ID behavior when present.
3. Inspect runner discovery and configuration, then inspect the project-defined commands before
   choosing a one-file suite or an orchestrator with sub-suites.
4. Apply the cards using the project's existing names, providers, runner, HTTP client, and commands.
5. When project commands exist, verify both the target file and the full E2E suite. Run the relevant
   repository checks for other NestJS changes.
6. Produce the Output Contract below without exposing secrets.

## Rule Categories by Priority

| Priority                                          | Prefix      | Use for                                                                                                                  |
| ------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| Critical runtime and contract risk                | `test-e2e-` | Production-like HTTP bootstrap, real dependencies, lifecycle, suite composition, payloads, and public response contracts |
| Critical boundary and integration risk            | `api-`      | External service input and output contracts                                                                              |
| High configuration and framework integration risk | `config-`   | Configuration placement, validation, registration, injection, environment access, and secrets                            |
| High application design risk                      | `arch-`     | Coordinators, service boundaries, repositories, and standalone contexts                                                  |
| High diagnostics risk                             | `error-`    | Structured logging and safe caught-error handling                                                                        |
| High NestJS data integration risk                 | `nestjs-`   | Drizzle database module wiring and lifecycle                                                                             |

## Decision Map

Load the first matching card for the decision. Each physical reference card appears once in this
map.

| Concern                                       | Card                                                                                                            |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| E2E bootstrap and production parity           | [Replicate the production bootstrap in E2E tests](references/test-e2e-replicate-production-bootstrap.md)        |
| E2E dependencies and HTTP authentication      | [Exercise real application dependencies in E2E tests](references/test-e2e-use-real-dependencies.md)             |
| E2E context, cleanup, and singleton ownership | [Own shared E2E context and lifecycle in the orchestrator](references/test-e2e-own-shared-context-lifecycle.md) |
| E2E suite size and discovery                  | [Organize E2E suites by flow and discovery rules](references/test-e2e-organize-suites-by-size.md)               |
| E2E canonical and invalid payloads            | [Derive invalid E2E payloads from canonical valid constants](references/test-e2e-derive-invalid-payloads.md)    |
| E2E public response and error contracts       | [Assert explicit public contracts in E2E tests](references/test-e2e-assert-public-contracts.md)                 |
| Configuration file placement                  | [Place configuration files under src/config](references/config-place-files-under-src-config.md)                 |
| Configuration factories and namespaces        | [Use namespaced registerAs factories](references/config-use-namespaced-register-as-factories.md)                |
| Environment validation                        | [Validate environment with Zod](references/config-validate-environment-with-zod.md)                             |
| AppModule configuration wiring                | [Register configuration in AppModule](references/config-register-configuration-in-app-module.md)                |
| Configuration consumer injection              | [Inject namespaced configuration](references/config-inject-namespaced-configuration.md)                         |
| Direct environment access                     | [Prevent direct environment access](references/config-prevent-direct-environment-access.md)                     |
| Secret handling                               | [Avoid hardcoded secrets](references/config-avoid-hardcoded-secrets.md)                                         |
| Cross-module workflows                        | [Use flow coordinators for cross-module workflows](references/arch-use-flow-coordinators.md)                    |
| Service responsibility                        | [Keep services focused on one domain](references/arch-service-repository-responsibility.md)                     |
| Drizzle persistence access                    | [Use repositories for Drizzle persistence access](references/arch-use-repository-pattern.md)                    |
| Non-HTTP NestJS processes                     | [Use a standalone NestJS application context](references/arch-use-standalone-application.md)                    |
| Structured logging                            | [Use structured runtime logging](references/error-use-structured-logging.md)                                    |
| Caught error narrowing                        | [Handle caught errors as unknown](references/error-handle-unknown-catches.md)                                   |
| External service boundaries                   | [Validate external service contracts](references/api-use-external-service-contracts.md)                         |
| Drizzle database module integration           | [Provide Drizzle through a NestJS database module](references/nestjs-use-drizzle-database-module.md)            |

## Output Contract

Report all of the following:

- Cards applied.
- Files created or modified.
- Real HTTP flows and real providers exercised for E2E work.
- Canonical constants or factories reused.
- Invalid variants and local mutations used, including the property changed for each case.
- Substituted external boundaries and the justification for each, or an explicit statement that none
  were substituted.
- Commands executed and their results, including the target file and full E2E suite when available.
