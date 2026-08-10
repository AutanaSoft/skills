# Skill Development Guide

A skill is a package of specific instructions that enables an AI agent to recognize a task and
execute it consistently. This guide is the repository's conceptual and operational authority for
creating, modifying, merging, or retiring skills. It is intended for the people who design and
maintain those packages.

Every skill requires `SKILL.md`. Other resources are optional and are added only when they improve
execution, maintenance, or evaluation. A simple skill may consist solely of `SKILL.md`.

The [Agent Skills specification](https://agentskills.io/specification) defines the general format.
The [repository README](../../README.md) introduces the collection, and the
[repository structure](../repository-structure.md) documents its organization and validation points.
This guide defines how to make authoring decisions. The canonical templates are structural
skeletons, not sources of additional rules.

## Quick Path

To create or modify a skill:

1. Consult the README and repository documentation applicable to the scope of the change.
2. When modifying a skill, first inventory its `SKILL.md`, `references/`, scripts, assets, README,
   evals, links, and current behavior.
3. Define or confirm the capability, scope, triggers, and exclusions.
4. Choose a kebab-case name and a directory with the same name.
5. Create or adjust `SKILL.md` from the [skill template](./skill-template.md), then remove fields
   and conditional sections that do not apply.
6. Design the selection, general workflow, input constraints, and navigation the agent needs.
7. Decide whether the domain requires categories and reference cards; do not add them by default.
8. Add scripts, assets, a README, or evals only for a concrete purpose.
9. Update navigation, links, the README, and evals when the inventory or behavior changes.
10. Validate structure, formatting, links, activation, behavior, and the complete diff.
11. Accurately report any validation step you did not run.

## Package Anatomy

```text
<skill-name>/
├── SKILL.md          # Required: discovery metadata, workflow, and navigation
├── references/       # Optional: cohesive rule or decision cards
├── scripts/          # Optional: deterministic task helpers
├── assets/           # Optional: files used in generated output
├── evals/            # Optional: triggering and behavioral evaluation cases
└── README.md          # Optional: maintainer inventory and conventions
```

The directory name matches `name`. Use relative paths for internal resources so the skill remains
portable. Do not add categories, empty directories, or auxiliary files merely to make the package
look complete.

The structure applies progressive disclosure:

1. **Discovery:** the agent evaluates `name` and `description`.
2. **Activation:** it reads `SKILL.md` to learn the workflow, constraints, and navigation.
3. **Execution:** it loads only the relevant cards, uses assets, or runs scripts.
4. **Evaluation:** maintainers use `evals/` without adding those instructions to the normal
   execution context.

## Design Scope and Activation

Before writing instructions, define a concrete capability: what outcome the skill produces, which
tasks belong to it, and which do not. Use task and domain terms that may appear in real requests.

The `description` is the activation contract, not a catalog summary. It must:

- state what work belongs to the skill;
- include concrete positive triggers;
- include exclusions when they prevent a likely false activation;
- remain understandable when the package is distributed independently.

Keep activation and scope self-contained. Do not require or mention another skill unless the package
declares that dependency and the environment guarantees its availability. Express exclusions as task
boundaries, not circumstantial redirects.

**Avoid:**

```text
Use another-skill instead for end-to-end testing.
```

**Prefer:**

```text
Do not use this skill for end-to-end test design, test-runner orchestration, fixtures, or temporary
test infrastructure.
```

The presence of two skills in the same repository does not prove that both are installed. Document
composition only when an explicit dependency model exists.

## Build `SKILL.md`

Start from the [skill template](./skill-template.md). Keep only fields and sections that serve a
real purpose. `SKILL.md` contains activation, scope, selection, general workflow, input constraints,
and navigation. When `references/` exists, it discovers and directs the agent to the relevant rules
without duplicating their normative details.

It must make it possible to answer:

1. Does this task belong to the skill?
2. Which workflow or decision category applies?
3. Which resource should be loaded next?

### Frontmatter

The repository validator accepts these top-level fields:

| Field           | Required | Contract                                                                                 |
| --------------- | -------- | ---------------------------------------------------------------------------------------- |
| `name`          | Yes      | Kebab-case, no more than 64 characters, and matching the directory.                      |
| `description`   | Yes      | A string of no more than 1024 characters stating what the skill does and when to use it. |
| `license`       | No       | A short identifier or relative path to the license.                                      |
| `allowed-tools` | No       | Tool restrictions when supported by the environment.                                     |
| `metadata`      | No       | Additional metadata such as `author` or `version`.                                       |
| `compatibility` | No       | An environment or dependency requirement, no more than 500 characters.                   |

Do not add unsupported fields. Remove optional fields that do not apply: the validator is the
repository contract.

### Conditional Sections

Include categories, priorities, and `Rule Categories by Priority` only when the skill organizes
rules or decisions by category. In that case, use `Quick Reference` as a concise index with the
identifier first:

```text
`<prefix>-<slug>` - <brief description>
```

Include `How to Use` only when `references/` exists. It must explain how to identify and load only
the relevant cards. The inventory and maintenance workflow belong in the README, not in
`How to Use`.

Use the exact technical headings `When to Apply`, `Rule Categories by Priority`, `Quick Reference`,
and `How to Use` when their corresponding sections apply.

Remove every conditional section without a purpose. Concision does not mean omitting necessary
decisions; it means avoiding explanations, examples, and detailed rules that already have another
owner.

## Decide Whether to Create Reference Cards

Use `references/` when detailed rules, examples, exceptions, or edge cases would prevent `SKILL.md`
from remaining a concise entry point. Do not create cards for a simple skill that can express its
entire workflow and instructions in `SKILL.md`. When `references/` exists, the cards own the
detailed normative rules and conventions; `SKILL.md` makes them discoverable, supports their
selection, and loads only the relevant ones.

The canonical term is **reference card**. Each card owns one cohesive rule or decision. It may group
related variants when they share an activation context, architectural or operational boundary,
impact, failure mode, and evaluation criterion.

Split content when its rules can be activated, fail, change, or be evaluated independently. Do not
turn every sentence into a card: atomicity defines a decision boundary, not an isolated statement.

For example, a configuration decision may cohesively cover:

```text
defaults
→ defined overrides
→ transformations
→ derived values
→ final validation
→ framework registration
```

Secret handling or injection into consumers may require separate cards because their triggers and
failures differ.

### Single Normative Ownership

Assign one normative owner to each decision. The owning card contains the rule, its rationale,
application criteria, exceptions, boundaries, examples, and sources. Related cards may define the
limits of their responsibility and link to the owner, but they must not restate or alter its
guidance.

Single ownership prevents contradictions, partial updates, duplicated examples, inconsistent
exceptions, and ambiguity about which card should evaluate a case.

## Build a Reference Card

Create each card from the [reference card template](./reference-card-template.md). Use the exact
technical markers `Incorrect`, `Correct`, and `Reference`.

Every card satisfies this contract:

- `title` exactly matches the visible H2 heading;
- `impact` uses one of these exact values: `CRITICAL`, `HIGH`, `MEDIUM-HIGH`, `MEDIUM`, or
  `LOW-MEDIUM`;
- `impactDescription` explains the consequence, scope, or rationale;
- tags are only those that are necessary, non-redundant, lowercase, and kebab-case;
- it contains specific `Incorrect` and `Correct` examples focused on the same rule or decision;
- every code block declares its language;
- it cites at least one authoritative HTTPS source when an applicable external authority exists;
- it links related cards instead of duplicating their rules.

A purely internal policy may explicitly justify in `Reference` why no external source applies. Never
invent a link to satisfy the format mechanically.

Examples must implement the written rule precisely and cover the same decision from both sides. They
must not impose security, compatibility, runtime, or architectural behavior stricter than the rule.
If an example demonstrates only part of a broader policy, state that limitation.

## Optional Resources and Boundaries

### Scripts

Use `scripts/` for deterministic utilities that improve execution. They must document inputs and
outputs, fail clearly and safely, avoid hidden assumptions about the network, file system, or
environment, respect the target project's tools, and remain reusable beyond an evaluation prompt.

A script supports a workflow or decision; it does not replace the written contract or contain
normative rules that belong in a card.

### Assets

Use `assets/` for files copied, transformed, or included in output: templates, diagrams, starter
files, schemas, configuration, or static media. Explanatory documentation belongs in `SKILL.md` or
`references/`.

### README

The README is an inventory and maintenance aid, not a source of execution rules. It may document
structure, active cards, domains or prefixes, conventions, evals, and contributor notes.

Do not place normative rules only there: the agent may not read it. Keep the README, `SKILL.md`, and
physical tree synchronized when the inventory changes.

### Evals

Use `evals/` when they provide meaningful protection for activation or behavior. They are
maintenance resources and are not normally loaded during execution.

Activation evaluations include realistic positive, negative, and edge-case queries. Rerun them when
`name`, `description`, triggers, exclusions, or scope change. They evaluate the skill independently,
without assuming that another skill will receive excluded requests.

Behavior evaluations verify observable decisions and outcomes: required steps, ownership, public
patterns, outputs, prohibitions, and exceptions. Their assertions verify the contract, not exact
wording. Rerun them when rules, examples, workflow, ownership, output, or reference structure
change.

Keep credentials, tokens, personal data, and secrets out of examples, logs, reports, and test data.

## Modify, Merge, or Retire Content

Before editing an existing skill, inventory the valid behavior of every affected file, its incoming
links, and its evals. Treat the current structure as intentional until proven otherwise.

When merging, renaming, replacing, or retiring cards, classify every source requirement as:

- preserved in the new normative owner;
- moved to another owner;
- superseded by a documented decision;
- intentionally removed with a rationale.

Do not lose accepted behavior because an example or explanation is simplified. Preserving the
general topic is insufficient if an exported API, ownership boundary, validation, required output,
exception, or consumption pattern disappears.

After restructuring:

1. Remove or archive obsolete files according to repository policy.
2. Update incoming links, relative paths, `Quick Reference`, and `How to Use`.
3. Update `SKILL.md` and the README, if present.
4. Add or update evals that protect inherited behavior.
5. Search for obsolete names, broken links, and duplicated rules.

## Validation and Delivery Checklist

A structurally valid skill is not necessarily ready. Before delivery, verify:

- [ ] Applicable repository instructions were read and followed.
- [ ] `name`, directory, frontmatter, and conditional sections satisfy their contract.
- [ ] Capability, scope, triggers, and exclusions are explicit and self-contained.
- [ ] `SKILL.md` contains selection, general workflow, input constraints, and navigation without
      duplicating normative details.
- [ ] Every rule has a single owner and every card preserves one cohesive decision.
- [ ] Categories, `Rule Categories by Priority`, `Quick Reference`, and `How to Use` exist only when
      applicable.
- [ ] Cards satisfy the impact, tag, example, code-language, and source requirements.
- [ ] Scripts, assets, the README, and evals have a purpose and respect their boundaries.
- [ ] The structure and skill-specific validator pass.
- [ ] Repository-wide formatting and validation pass.
- [ ] Links and obsolete filenames were checked.
- [ ] Relevant activation and behavior evaluations pass.
- [ ] The complete diff preserves the intended scope and behavior.

When you cannot run a validation, report the exact omitted command, the reason, and the behavior
left unverified. Do not present eval definitions as successful results when they were not run.

Concrete commands belong in the repository instructions. This guide defines what must be tested; it
does not replace those commands.

## Templates and Documentation Authority

- This guide owns all conceptual and operational authoring rules.
- The [skill template](./skill-template.md) is the canonical structural skeleton for `SKILL.md`.
- The [reference card template](./reference-card-template.md) is the canonical structural skeleton
  for `references/`.
- The README and repository documentation own organization, maintenance, and validation conventions.

Instructions directed at an agent govern how that agent works within the repository; they do not
replace documented repository conventions or the authoring contract defined here.

Use the templates to start the structure and this guide to decide what to keep, complete, or remove.
A difference between a skeleton and this guide does not create a second policy: the rule resides
here, while the template represents only its minimum form.
