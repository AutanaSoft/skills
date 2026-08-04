---
name: nestjs-practices
description: >
  Apply NestJS practices for modules, services, repositories, dependency injection, configuration,
  bootstrap, logging and errors, external contracts, data integration, and standalone application
  contexts. Use for NestJS configuration, architecture, observability, integrations, Drizzle, and
  standalone-context work. Use nestjs-e2e-practices instead for end-to-end test design or review.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.4.0'
---

# NestJS Practices

Apply the smallest relevant set of NestJS decision cards. The cards own normative guidance,
examples, exceptions, and sources; this entry point activates the catalog and routes the work.

## Activation Contract

- Load this skill for NestJS modules, services, repositories, dependency injection, configuration,
  bootstrap, logging and errors, external contracts, data integration, or standalone application
  contexts.
- Use `nestjs-e2e-practices` for end-to-end test design, implementation, review, or repair.
- Do not activate it for generic TypeScript work that has no NestJS-specific decision.

## Hard Rules

- Load the card that owns each decision; do not copy a card's full rule, examples, exceptions, or
  sources into this entry point.
- Inspect the target project's architecture and configuration before choosing a structure. Preserve
  established conventions unless the requested change requires a migration.
- Keep adapters, ORMs, clients, and package-manager commands project-dependent.
- Keep credentials, tokens, and other secrets out of logs, reports, and generated examples.

## Workflow

1. Identify the NestJS concern and load only the matching cards in the decision map.
2. Apply the cards using the project's existing names, providers, clients, and commands.
3. Run the relevant repository checks for the NestJS changes.
4. Produce the Output Contract below without exposing secrets.

## Rule Categories by Priority

| Priority                                          | Prefix    | Use for                                                                                       |
| ------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------- |
| Critical boundary and integration risk            | `api-`    | External service input and output contracts                                                   |
| High configuration and framework integration risk | `config-` | Configuration placement, validation, registration, injection, environment access, and secrets |
| High application design risk                      | `arch-`   | Coordinators, service boundaries, repositories, and standalone contexts                       |
| High diagnostics risk                             | `error-`  | Structured logging and safe caught-error handling                                             |
| High NestJS data integration risk                 | `nestjs-` | Drizzle database module wiring and lifecycle                                                  |

## Decision Map

Load the first matching card for the decision. Each physical reference card appears once in this
map.

| Concern                                | Card                                                                                                 |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Configuration file placement           | [Place configuration files under src/config](references/config-place-files-under-src-config.md)      |
| Configuration factories and namespaces | [Use namespaced registerAs factories](references/config-use-namespaced-register-as-factories.md)     |
| Environment validation                 | [Validate environment with Zod](references/config-validate-environment-with-zod.md)                  |
| AppModule configuration wiring         | [Register configuration in AppModule](references/config-register-configuration-in-app-module.md)     |
| Configuration consumer injection       | [Inject namespaced configuration](references/config-inject-namespaced-configuration.md)              |
| Direct environment access              | [Prevent direct environment access](references/config-prevent-direct-environment-access.md)          |
| Secret handling                        | [Avoid hardcoded secrets](references/config-avoid-hardcoded-secrets.md)                              |
| Cross-module workflows                 | [Use flow coordinators for cross-module workflows](references/arch-use-flow-coordinators.md)         |
| Service responsibility                 | [Keep services focused on one domain](references/arch-service-repository-responsibility.md)          |
| Drizzle persistence access             | [Use repositories for Drizzle persistence access](references/arch-use-repository-pattern.md)         |
| Non-HTTP NestJS processes              | [Use a standalone NestJS application context](references/arch-use-standalone-application.md)         |
| Structured logging                     | [Use structured runtime logging](references/error-use-structured-logging.md)                         |
| Caught error narrowing                 | [Handle caught errors as unknown](references/error-handle-unknown-catches.md)                        |
| External service boundaries            | [Validate external service contracts](references/api-use-external-service-contracts.md)              |
| Drizzle database module integration    | [Provide Drizzle through a NestJS database module](references/nestjs-use-drizzle-database-module.md) |

## Output Contract

Report all of the following:

- Cards applied.
- Files created or modified.
- Commands executed and their results.
