# Portable Authoring Contract

Use this fallback when the host does not provide stricter skill-development rules. It contains only
the decisions required to create and modify a portable skill safely.

## Package Contract

Every skill requires `SKILL.md`. Optional resources belong in `agents/`, `references/`, `scripts/`,
`assets/`, and test or evaluation directories only when they serve a concrete purpose. Use relative
internal paths. Do not create empty directories, unresolved template tokens, or auxiliary files by
default.

Apply progressive disclosure:

1. Discovery reads `name` and `description`.
2. Activation reads `SKILL.md` for selection, workflow, constraints, and navigation.
3. Execution loads only relevant references or assets and runs necessary scripts.
4. Evaluation remains outside normal execution context.

## Activation and Metadata

Use only these supported top-level `SKILL.md` frontmatter fields:

| Field           | Required | Portable contract                                                   |
| --------------- | -------- | ------------------------------------------------------------------- |
| `name`          | Yes      | Lowercase kebab-case, at most 64 characters, matching the directory |
| `description`   | Yes      | Non-empty activation contract, at most 1024 characters              |
| `license`       | No       | SPDX identifier or relative license path                            |
| `allowed-tools` | No       | Environment-supported tool restrictions                             |
| `metadata`      | No       | Maintainer metadata such as author or version                       |
| `compatibility` | No       | Environment requirements, at most 500 characters                    |

The description states the work performed and concrete positive triggers. Add exclusions only when
they prevent likely false activation. Keep it understandable outside its source repository.

When `agents/openai.yaml` exists, use quoted strings under `interface`:

```yaml
interface:
  display_name: 'Human-readable name'
  short_description: 'A concise summary between 25 and 64 characters'
  default_prompt: 'Use $skill-name to perform a representative task.'
```

The default prompt explicitly names `$<skill-name>`. Regenerating this file must not modify any
other artifact.

## Creation

Define capability, scope, triggers, exclusions, inputs, outputs, and concrete requests before naming
the skill. Search for an equivalent package first. Choose a short verb-led name and use the bundled
initializer with complete metadata. Customize the generated workflow before delivery.

Add scripts only for deterministic repeated work, assets only for files consumed by outputs, and
tests or evals only for meaningful protection. A README is optional maintainer inventory, never the
sole owner of execution rules.

## Modification

Inventory the existing package, incoming links, registrations, tests, and behavior before editing.
Treat existing content as intentional. Preserve accepted behavior unless the request explicitly
changes it.

For merges, renames, replacements, or retirement, classify every affected requirement as preserved,
moved, superseded with rationale, or intentionally removed. Update links, navigation, metadata, and
evaluations coherently. Search for stale names and duplicated normative rules.

## Reference Cards

Create cards only when detailed rules, exceptions, or examples would make `SKILL.md` dense. Each
card owns one cohesive decision and uses `assets/reference-card-template.md`.

Require:

- A title matching the visible H2 heading
- Impact of `CRITICAL`, `HIGH`, `MEDIUM-HIGH`, `MEDIUM`, or `LOW-MEDIUM`
- A meaningful impact description and necessary lowercase kebab-case tags
- Focused `Incorrect` and `Correct` examples with declared code languages
- An authoritative HTTPS reference when one exists, or an explicit internal-policy justification
- Links to related owners instead of duplicated rules

## Validation

Run the bundled validator and all affected scripts or tests. Confirm directory/name agreement,
frontmatter fields, metadata coherence, reference-card structure, absence of unresolved template
tokens, and preservation of unrelated files. Then run host checks when available and report omitted
checks honestly.
