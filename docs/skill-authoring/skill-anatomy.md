# Anatomy of a Skill

A skill packages focused instructions for an AI agent. It requires `SKILL.md` and can add resources
only when they improve execution. See the
[Agent Skills specification](https://agentskills.io/specification) for the general format; this
document explains the repository's conceptual model.

## Canonical Structure

```text
<skill-name>/
├── SKILL.md          # Required: discovery metadata and instructions
├── references/       # Optional: rule cards and extended guidance
├── scripts/          # Optional: deterministic task helpers
└── assets/           # Optional: files used in generated output
```

The directory name matches `name`. Reference resources with relative paths so the skill remains
portable.

## Frontmatter Contract

The repository validator accepts these top-level `SKILL.md` fields:

| Field           | Required | Contract                                                                                             |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Kebab-case and at most 64 characters; repository convention requires it to equal the directory name. |
| `description`   | Yes      | A string of at most 1024 characters that states what the skill does and when to use it.              |
| `license`       | No       | A short license identifier or relative license path.                                                 |
| `allowed-tools` | No       | Tool restriction metadata when the runtime supports it.                                              |
| `metadata`      | No       | Additional metadata such as `author` or `version`.                                                   |
| `compatibility` | No       | A runtime or dependency requirement, at most 500 characters.                                         |

Do not add unsupported top-level fields. The validator is the repository contract.

## Progressive Disclosure

1. **Discovery:** the agent evaluates `name` and `description` to decide whether the skill applies.
2. **Activation:** the agent reads `SKILL.md` for the task-specific workflow and navigation.
3. **Execution:** the agent reads relevant `references/` files, uses `assets/`, or runs `scripts/`.

Keep `SKILL.md` concise. Put detailed rules, examples, and edge cases in `references/` rather than
duplicating them in the entry point.

## Quality Boundaries

- Write actionable instructions and explicit triggers.
- Keep scripts deterministic and document required inputs and outputs.
- Keep rules in reference cards; link related cards instead of repeating their guidance.
- Use a skill README for inventory and maintenance conventions, not task-time rules.

## Authoring Templates

- [Skill Template](./skill-template.md) defines the operational contract for `SKILL.md`.
- [Reference Card Template](./reference-card-template.md) defines one rule card in `references/`.
