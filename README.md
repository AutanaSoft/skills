# AutanaSoft Skills

[![skills.sh](https://skills.sh/b/AutanaSoft/skills)](https://skills.sh/AutanaSoft/skills)

Skill collection that lets AI agents apply consistent TypeScript, framework, and AutanaSoft workflow
practices. Installable via `npx skills` in any agent that supports the standard.

## Choose an installation mode

Choose one installation mode per project:

| Mode                    | Best for               | How it works                                                                 |
| ----------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| Claude Code marketplace | Managed installations  | Claude Code manages the installed plugin and its updates.                    |
| `skills.sh`             | Editable installations | The CLI copies skill files into the agent directory for you to own and edit. |

Do not install both modes in the same project. They create duplicate copies of the skills.

## Quick path

1. Pick a skill from the table below.
2. Install it: `npx skills add AutanaSoft/skills --skill <name>`.
3. Activate it in the agent with a phrase from its `description` (frontmatter). For example: "write
   a commit" loads `commit-message`.

## Skills

### typescript

| Skill                  | When to use it                                                                    |
| ---------------------- | --------------------------------------------------------------------------------- |
| `ts-general-practices` | Type safety, imports type-only, generics, utility types, unknown data boundaries. |
| `ts-zodv4-practices`   | Zod 4 validation, shared contracts, parse/safeParse, schema composition.          |
| `drizzle-practices`    | Schemas, migrations, transactions, persistence contracts.                         |
| `nestjs-practices`     | Modules, services, repositories, DI, logging, standalone apps.                    |
| `nestjs-e2e-practices` | Real HTTP E2E, Jest orchestration, isolated databases, fixtures, API contracts.   |
| `nextjs-practices`     | App Router, Server Components, route handlers, server actions.                    |

### workflow

| Skill            | When to use it                                                      |
| ---------------- | ------------------------------------------------------------------- |
| `sdd-lifecycle`  | SDD artifact lifecycle (PRD, spec, design, tasks, verify, archive). |
| `pdr-intake`     | Mature ambiguous ideas into minimum PDRs before starting SDD.       |
| `commit-message` | Conventional Commits generated from `git diff`.                     |

## Why these skills exist

These skills turn recurring engineering decisions into concise, reusable instructions: type-safe
boundaries, explicit validation and persistence contracts, framework boundaries, and a documented
workflow from idea to commit. Compose and adapt them to the project instead of treating them as a
replacement for engineering judgment.

## Installation

### Via `npx skills` (recommended)

```bash
npx skills add AutanaSoft/skills --skill <name>
```

### Claude Code marketplace

Claude Code can install the grouped plugins directly from the repository marketplace:

```text
/plugin marketplace add AutanaSoft/skills
/plugin install typescript@autanasoft-skills
/plugin install workflow@autanasoft-skills
```

Detailed installation options and verification steps are available in the
[installation guide](docs/installation.md).

Each skill follows the [Agent Skills](https://agentskills.io/specification) standard:

- `name` (frontmatter) matches the directory name.
- `description` includes triggers so the agent activates it on its own.
- Extended content lives in `references/` and only loads on demand.

Repository layout and authoring guidance are documented in
[repository structure](docs/repository-structure.md).

## License

MIT — see [LICENSE](./LICENSE).
