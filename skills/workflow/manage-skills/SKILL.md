---
name: manage-skills
description: >-
  Create, update, restructure, rename, merge, or retire portable agent skills. Use when changing a
  skill's activation contract, SKILL.md, reference cards, scripts, assets, tests, discovery
  metadata, or package navigation. Includes standalone templates, initialization, OpenAI metadata
  generation, validation, and update rules. Do not use for installing third-party skills or
  unrelated agent configuration.
license: Apache-2.0
metadata:
  author: AutanaSoft
  version: '1.1.0'
---

# Manage Skills

Create and modify skills using only resources shipped in this package. Treat host documentation and
validators as optional, stricter overlays; absence of host tooling must never block the portable
workflow.

## When to Apply

Use this skill when:

- Creating a skill package in any writable destination
- Updating an existing skill's behavior, activation, structure, metadata, or resources
- Adding or changing reference cards, scripts, assets, README files, or evaluations
- Renaming, merging, replacing, or retiring skill content
- Synchronizing host navigation or registries after a skill inventory change

## Resolve Resources

Resolve every portable resource relative to this `SKILL.md` directory, never from the current
working directory:

```text
scripts/init_skill.py
scripts/generate_openai_yaml.py
scripts/quick_validate.py
assets/skill-template.md
assets/reference-card-template.md
references/authoring-contract.md
```

Read `references/authoring-contract.md` before creating or modifying a skill. Read the
reference-card section only when detailed rules justify cards. Host instructions may override the
fallback contract for work inside that host, but they cannot remove portable safety guarantees or
create an external runtime dependency for this skill.

## Workflow

### 1. Discover and select

- Extract the outcome, positive triggers, exclusions, users, inputs, outputs, constraints, and
  realistic requests.
- Search the target inventory for an equivalent skill before creating one.
- Choose `create` only when no equivalent exists. Otherwise choose `update` and explain the match.
- Read applicable host instructions when present. Do not assume a repository layout or package
  manager.

### 2. Inventory before update

Inspect the complete existing package before editing: `SKILL.md`, `agents/`, references, scripts,
assets, README, tests or evals, links, registrations, metadata, and current behavior. Treat every
existing difference as intentional unless evidence or the request says otherwise.

Classify affected behavior as preserved, moved, superseded with rationale, or intentionally removed.
Update incoming links and evaluations when behavior or paths change. Never rerun initialization over
an existing destination.

### 3. Create deterministically

Choose a short verb-led kebab-case name. Run:

```bash
python <skill-root>/scripts/init_skill.py <name> \
  --path <parent-directory> \
  --description <activation-contract> \
  --display-name <display-name> \
  --short-description <25-to-64-character-summary> \
  --default-prompt <prompt-containing-$name> \
  --overview <concise-purpose>
```

The initializer creates only `SKILL.md` and `agents/openai.yaml`. It rejects an existing destination
and leaves no placeholders or empty optional directories. Customize the generated workflow, then add
only resources justified by the capability. Use `assets/reference-card-template.md` when a card is
needed; do not copy the fallback contract into the target skill.

### 4. Update metadata explicitly

Preserve `agents/openai.yaml` when it remains coherent. Regenerate it only when missing, requested,
or stale relative to `SKILL.md`:

```bash
python <skill-root>/scripts/generate_openai_yaml.py <target-skill> \
  --display-name <display-name> \
  --short-description <25-to-64-character-summary> \
  --default-prompt <prompt-containing-$name>
```

The generator owns only `agents/openai.yaml`; it must not rewrite `SKILL.md` or other intentional
files.

### 5. Apply progressive disclosure

- Keep activation, scope, selection, general workflow, input constraints, and navigation in
  `SKILL.md`.
- Assign every normative decision one owner. Link instead of duplicating details.
- Add reference cards only for independently selectable rules, exceptions, or examples that would
  make `SKILL.md` dense.
- Add scripts for deterministic repeated work, assets for output inputs, and tests or evals for
  meaningful behavior protection.
- Do not create placeholders, empty directories, or auxiliary documentation without a concrete
  execution or maintenance purpose.

### 6. Validate portable behavior

Always run the bundled validator first:

```bash
python <skill-root>/scripts/quick_validate.py <target-skill>
```

Run affected scripts and tests in temporary directories. Verify creation, metadata regeneration,
valid and invalid packages, and execution with no host documentation or validators available.

After portable checks pass, discover and run applicable host formatters, linters, validators, tests,
registry checks, and diff checks. Host checks are additional evidence, not prerequisites for
portable operation. Report exact omitted commands and resulting uncertainty.

### 7. Synchronize host metadata

When inventory or paths change, inspect the host for registries, marketplace manifests, skill
tables, incoming links, and evaluations. Update only owners proven applicable. Search for obsolete
names, stale paths, broken links, and duplicated rules after renames, merges, or retirement.

## Output Contract

Return:

- `status`: `created`, `updated`, `blocked`, or `failed`
- `executive_summary`: concise outcome and key design choice
- `artifacts`: created, changed, removed, and registered paths
- `next_recommended`: the most useful next action, or `none`
- `risks`: unresolved risks and omitted validations, or `none`
- `skill_resolution`: selected `create` or `update`, resolved skill name and path, and equivalence
  evidence
