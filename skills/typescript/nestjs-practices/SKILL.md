---
name: nestjs-practices
description:
  'Trigger: NestJS configuration work. Apply configuration placement, validation, wiring, injection,
  environment access, and secret-handling practices.'
license: MIT
metadata:
  author: AutanaSoft
  version: '0.2.0'
---

# NestJS Practices

Apply focused NestJS configuration rules. Load only the cards that match the change; the cards own
the normative guidance and examples.

## Activation Contract

- Load this skill when adding, reviewing, or refactoring NestJS configuration, environment
  validation, `ConfigModule` wiring, or configuration injection.

## Hard Rules

- Keep each rule decision in its corresponding reference card; do not combine unrelated
  configuration decisions in a change or a card.
- Preserve established configuration namespaces unless the change explicitly requires a migration.

## Decision Gates

| Change concern            | Load this card                                              |
| ------------------------- | ----------------------------------------------------------- |
| File location or name     | `references/config-place-files-under-src-config.md`         |
| Factory or namespace      | `references/config-use-namespaced-register-as-factories.md` |
| Environment validation    | `references/config-validate-environment-with-zod.md`        |
| Root module wiring        | `references/config-register-configuration-in-app-module.md` |
| Consumer injection        | `references/config-inject-namespaced-configuration.md`      |
| Direct environment access | `references/config-prevent-direct-environment-access.md`    |
| Secrets                   | `references/config-avoid-hardcoded-secrets.md`              |

## Execution Steps

1. Inspect existing namespaces and their consumers before changing configuration.
2. Apply the relevant cards in the table without introducing a separate workflow card.
3. Run the repository lint and formatting commands that apply to the changed application.

## Output Contract

Report the cards applied, the configuration files changed, and the lint or formatting result.

## References

- `references/config-place-files-under-src-config.md`
- `references/config-use-namespaced-register-as-factories.md`
- `references/config-validate-environment-with-zod.md`
- `references/config-register-configuration-in-app-module.md`
- `references/config-inject-namespaced-configuration.md`
- `references/config-prevent-direct-environment-access.md`
- `references/config-avoid-hardcoded-secrets.md`
