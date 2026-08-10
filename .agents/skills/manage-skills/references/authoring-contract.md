---
title: Portable Authoring Contract
impact: CRITICAL
impactDescription: Prevents standalone skill authoring from diverging from the canonical contract.
tags: skill-authoring, portability
---

## Portable Authoring Contract

This file is the standalone operational transposition of the canonical Skill Development Guide. The
guide remains the single normative owner in its repository; this copy exists only so the distributed
skill can apply the same decisions without host files. Host rules may add stricter checks but must
not weaken portable safety or create a runtime dependency.

### Quick Path

1. Read applicable host instructions.
2. For updates, inventory the complete package, links, registrations, evals, and current behavior.
3. Define capability, scope, triggers, exclusions, inputs, outputs, constraints, and realistic uses.
4. Search for an equivalent skill; create only when no equivalent exists.
5. Start `SKILL.md` from `assets/skill-template.md`; explicitly choose every optional field and
   conditional section.
6. Add reference cards, scripts, assets, README, metadata, or evals only for a concrete purpose.
7. Validate portable behavior, then applicable host checks, and report omissions exactly.

### Package and Disclosure

Every package requires `SKILL.md`. Optional `agents/`, `references/`, `scripts/`, `assets/`,
`evals/`, and `README.md` exist only when useful. Directory and `name` match; internal paths are
relative. Never ship placeholders, unresolved markers, empty directories, or auxiliary files added
for completeness.

Progressive disclosure has four levels: discovery reads `name` and `description`; activation reads
`SKILL.md`; execution loads only relevant references, assets, or scripts; maintainers run evals
outside normal execution context.

### Activation and Frontmatter

The activation contract states what work belongs, concrete positive triggers, and exclusions that
prevent likely false activation. It remains understandable when distributed alone. Do not redirect
to another skill unless an explicit dependency model guarantees it; express exclusions as task
boundaries.

Use only these top-level fields:

| Field           | Required | Contract                                                              |
| --------------- | -------- | --------------------------------------------------------------------- |
| `name`          | Yes      | Kebab-case, at most 64 characters, matching the directory             |
| `description`   | Yes      | String, at most 1024 characters, describing capability and activation |
| `license`       | No       | Short identifier or relative license path                             |
| `allowed-tools` | No       | Environment-supported tool restrictions                               |
| `metadata`      | No       | Mapping such as `author` or `version`                                 |
| `compatibility` | No       | Environment or dependency requirement, at most 500 characters         |

Remove inapplicable optional fields. `agents/openai.yaml` is also optional: create it only when the
user requests it or the host requires it. When present, `interface` contains string values
`display_name`, `short_description` (25-64 characters), and `default_prompt`, which mentions
`$<skill-name>`. Metadata generation owns only that file.

### Build `SKILL.md`

Use `assets/skill-template.md` as the structural skeleton. Keep activation, scope, selection,
general workflow, input constraints, and navigation here, without duplicating detailed normative
owners.

`When to Apply` is required. Include categories, priorities, exact heading
`Rule Categories by Priority`, and `Quick Reference` only when rules or decisions are categorized.
Quick-reference entries use `` `<prefix>-<slug>` - <brief description> ``. Include exact heading
`How to Use` only when `references/` exists; it explains how to select and load only relevant cards,
not inventory maintenance. Remove every conditional section that has no decided purpose.

### Reference Cards

Use cards only when detailed rules, examples, exceptions, or edge cases would make `SKILL.md` dense.
Each card owns one cohesive decision. Split independently activated, failing, changing, or evaluated
decisions; related cards link to the owner instead of restating it.

Create cards from `assets/reference-card-template.md`. Preserve exact markers `Incorrect`,
`Correct`, and `Reference`, and include supporting subsections only when required. Every card
requires:

- `title` exactly matching its only visible H2 heading;
- impact `CRITICAL`, `HIGH`, `MEDIUM-HIGH`, `MEDIUM`, or `LOW-MEDIUM`;
- a meaningful `impactDescription` and necessary, unique, lowercase kebab-case tags;
- specific Incorrect and Correct examples addressing the same written decision;
- a declared language on every code block;
- an authoritative HTTPS source when applicable, or an explicit internal-policy justification when
  no external authority applies.

Examples implement the written rule precisely and must not add stricter security, compatibility,
runtime, or architecture behavior. State limitations when an example covers only part of a policy.

### Optional Resource Boundaries

- Scripts are deterministic, reusable helpers with documented inputs and outputs, clear safe
  failure, no hidden environment/network assumptions, and respect for target tooling. They support
  rather than own normative decisions.
- Assets are files copied, transformed, or included in output. Explanatory documentation belongs in
  `SKILL.md` or references.
- README is optional inventory and maintenance guidance for structure, cards, prefixes, conventions,
  evals, and contributors. It never solely owns execution rules and stays synchronized with the
  tree.
- Evals protect meaningful activation or behavior. Activation cases include positive, negative, and
  edge requests; behavior assertions verify observable contract rather than exact wording. Rerun
  them after relevant activation, workflow, ownership, output, example, or structure changes.
- Keep credentials, tokens, personal data, and secrets out of examples, logs, reports, and test
  data.

### Modify, Merge, or Retire

Before editing, inventory all affected files, valid behavior, incoming links, registrations, and
evals; treat differences as intentional. Classify every requirement as preserved, moved, superseded
with a documented rationale, or intentionally removed with a rationale. Do not lose APIs, ownership
boundaries, validation, required outputs, exceptions, or consumption patterns while simplifying.

After restructuring, handle obsolete files under host policy; update links, relative paths, Quick
Reference, How to Use, metadata, README, and evals; then search for stale names, broken links, and
duplicated rules. Never initialize over an existing skill. Update scripts must preserve unrelated
and intentional content; use narrow, atomic writes with rollback on failure.

### Validation and Delivery

Run `scripts/quick_validate.py` first. It deterministically checks supported and duplicate fields,
scalar types and lengths, exact technical headings, every card, tags, code fences, references,
optional OpenAI metadata, and residual markers. Run affected scripts and tests in temporary
directories and prove standalone execution. Then run host formatting, linting, validators, links,
evals, registries, complete diff, and repository-wide checks when available.

Manual review remains mandatory for semantics the validator cannot prove:

- capability, scope, trigger, and exclusion quality;
- useful selection, workflow, input constraints, and navigation;
- whether categories, references, scripts, assets, README, metadata, and evals are justified;
- single normative ownership and cohesive card boundaries;
- rule/rationale/example agreement, authority quality, and internal-source justification;
- preservation of intended behavior, links, inventory, secrets policy, and complete diff scope.

Report every omitted command, reason, and unverified behavior. Never report an eval definition as a
passing execution.

**Incorrect (depends on unavailable host policy or weakens the canonical contract):**

```text
Load host-only authoring instructions and skip portable validation when they are unavailable.
```

**Correct (uses the bundled transposition and treats host rules as stricter overlays):**

```text
Load this package-relative contract, run portable validation, then apply available host checks.
```

Reference: Internal policy transposed from the canonical Skill Development Guide; no external
authority owns these repository-specific authoring decisions.
