# Anatomy of a Skill

A skill packages focused instructions for an AI agent. It requires `SKILL.md` and can add resources
only when they improve execution, maintenance, or evaluation. See the
[Agent Skills specification](https://agentskills.io/specification) for the general format; this
document explains the repository's conceptual model.

## Canonical Structure

```text
<skill-name>/
├── SKILL.md          # Required: discovery metadata, workflow, and navigation
├── references/       # Optional: rule cards and extended guidance
├── scripts/          # Optional: deterministic task helpers
├── assets/           # Optional: files used in generated output
└── evals/            # Optional: triggering and behavioral evaluation cases
```

The directory name matches `name`. Reference internal resources with relative paths so the skill
remains portable.

Every optional directory must have a clear execution or maintenance purpose. Do not add empty
directories or supporting files merely to make the package appear complete.

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

The `description` is an activation contract, not a catalog summary. It must provide enough
information for an agent to decide whether the skill applies without reading the rest of the
package.

A strong description:

- states the work the skill owns;
- includes concrete positive triggers;
- includes material exclusions when they prevent likely false activation;
- uses task and domain terminology that may appear in user requests;
- remains understandable when the skill is distributed independently.

Keep activation and scope self-contained. Do not require or name another skill unless the package
explicitly declares that dependency and the runtime guarantees its availability. Express excluded
work in terms of the task boundary rather than redirecting to another skill.

## Progressive Disclosure

1. **Discovery:** the agent evaluates `name` and `description` to decide whether the skill applies.
2. **Activation:** the agent reads `SKILL.md` for the task-specific workflow, constraints, and
   navigation.
3. **Execution:** the agent reads only the relevant `references/` files, uses `assets/`, or runs
   `scripts/`.
4. **Evaluation:** maintainers use `evals/` to verify triggering and task behavior without adding
   evaluation instructions to the task-time context.

Keep `SKILL.md` concise. Put detailed rules, examples, exceptions, and edge cases in `references/`
rather than duplicating them in the entry point.

`SKILL.md` should help the agent answer three questions:

1. Does this skill own the current task?
2. Which workflow or decision category applies?
3. Which resource should be loaded next?

It should not attempt to reproduce every rule contained in the package.

## Self-Contained Activation

A skill must be discoverable and understandable in isolation.

The activation contract may exclude adjacent concerns, but it must not assume that another package
is installed, enabled, accepted by the maintainer, or available under a particular name.

**Avoid:**

```text
Use another-skill instead for end-to-end testing.
```

**Prefer:**

```text
Do not use this skill for end-to-end test design, test-runner orchestration, fixtures, or temporary
test infrastructure.
```

Cross-skill composition may be documented only when the repository and runtime define it as an
explicit dependency model. Incidental co-location in the same repository is not sufficient evidence
of availability.

## Reference Ownership

Assign one normative owner to each decision.

The owning reference card contains the authoritative:

- rule;
- rationale;
- application criteria;
- exceptions and limits;
- examples;
- external sources.

Related cards may explain where their responsibility ends and link to the owning card, but they must
not restate, fork, or subtly alter its guidance.

For example, one card may own configuration construction while another owns typed injection. The
injection card may require a validated configuration contract and link to the construction card, but
it should not define a second construction or validation policy.

A single normative owner reduces:

- contradictory guidance;
- partial updates;
- duplicated examples;
- inconsistent exceptions;
- uncertainty about which card an evaluation should target.

## Card Cohesion and Splitting

A reference card may contain multiple instructions when they form one cohesive decision.

Keep related instructions together when they share the same:

- activation context;
- architectural or operational boundary;
- impact;
- failure mode;
- evaluation criteria.

Split guidance into separate cards when the rules can activate, fail, change, or be evaluated
independently.

Do not force every sentence into its own card. Atomicity means one coherent decision boundary, not
one isolated statement.

For example, a configuration card may cohesively define:

```text
defaults
→ defined overrides
→ transformations
→ derived values
→ final validation
→ framework registration
```

when those steps jointly define one construction boundary.

Secret handling, consumer injection, and dynamic-module registration may still require separate
cards because their activation criteria and failure modes differ.

## Merging and Replacing Cards

When merging, renaming, or replacing reference cards, inventory the valid behavior owned by every
source card before editing.

For each source requirement, decide explicitly whether it will be:

- preserved in the new normative owner;
- moved to another card;
- replaced by a documented decision;
- removed intentionally.

Do not lose accepted behavior merely because an example or explanation was simplified.

A consolidation is incomplete when it preserves the broad topic but silently drops a meaningful
contract such as:

- an exported API;
- an ownership boundary;
- a validation step;
- a required output;
- an exception;
- a consumer pattern.

After restructuring cards:

1. remove or archive obsolete files according to repository policy;
2. update all incoming links;
3. update `SKILL.md`;
4. update the skill README;
5. update affected evaluations;
6. search for stale filenames and duplicated guidance.

## Reference Cards

Reference cards contain task-time normative guidance.

A card should represent one cohesive rule or decision and include the structure required by the
[Reference Card Template](./reference-card-template.md).

Cards should:

- use accepted frontmatter fields and impact values;
- match the frontmatter title and visible heading;
- provide focused incorrect and correct examples when examples improve the decision;
- label fenced code blocks with the correct language;
- cite authoritative HTTPS sources;
- link to related cards instead of duplicating their rules.

Examples must implement the written rule accurately. They must not introduce stronger runtime,
security, compatibility, or architectural behavior than the rule requires.

When an example intentionally demonstrates only part of a broader policy, state that limitation
explicitly.

## Scripts

Use `scripts/` for deterministic helpers that improve execution.

Scripts should:

- have documented inputs and outputs;
- fail clearly and safely;
- avoid hidden network, filesystem, or environment assumptions;
- preserve the target project's established tools when appropriate;
- be reusable rather than tailored to one evaluation prompt;
- avoid embedding normative guidance that belongs in a reference card.

A script supports a decision or workflow; it does not replace the written contract.

## Assets

Use `assets/` for files copied, transformed, or included in generated output.

Examples include:

- templates;
- diagrams;
- starter files;
- schemas;
- configuration fragments;
- static media.

Do not place explanatory documentation in `assets/`. Guidance belongs in `SKILL.md` or
`references/`.

## Evaluations

Use `evals/` to verify that a skill produces the intended activation and task behavior.

Evaluation files are maintenance resources. They are not normally loaded during task execution.

### Triggering Evaluations

Triggering evaluations verify whether the skill activates for the correct requests.

Include:

- representative positive queries;
- realistic negative queries;
- boundary cases likely to cause false positives or false negatives.

Re-run triggering evaluations whenever any of the following changes:

- `name`;
- `description`;
- activation boundaries;
- material exclusions;
- skill scope.

Triggering cases should evaluate the skill independently. They must not assume that another skill is
installed to receive an excluded request.

### Behavioral Evaluations

Behavioral evaluations verify observable decisions and outputs after activation.

Use them to check matters such as:

- required workflow steps;
- ownership boundaries;
- preserved public patterns;
- required files or output sections;
- prohibited behavior;
- relevant exceptions.

Assertions should test decisions and outcomes rather than exact prose. A response may use different
wording and still satisfy the skill contract.

Re-run behavioral evaluations whenever rules, examples, workflow, ownership, output expectations, or
reference structure change.

When merging cards, add or update evaluations that protect behavior inherited from every source
card.

## README Responsibility

A skill README is an inventory and maintenance aid, not a task-time rule source.

Use it to document:

- package structure;
- active reference cards;
- domain or prefix inventories;
- maintenance conventions;
- evaluation resources;
- contributor-oriented notes.

Do not place normative rules only in README. An agent that activates the skill may never read it.

Keep README, `SKILL.md`, and the physical file tree synchronized. When a card is added, removed,
renamed, or merged, update the inventory in the same change.

## Quality Boundaries

- Write actionable instructions and explicit triggers.
- Keep activation and exclusions self-contained.
- Keep `SKILL.md` focused on workflow and navigation.
- Assign one normative owner to each decision.
- Keep cohesive rules together and independently activated rules separate.
- Link related cards instead of repeating their guidance.
- Preserve accepted behavior when merging or replacing cards.
- Keep scripts deterministic and document required inputs and outputs.
- Ensure examples do not impose behavior stronger than the written rule.
- Use a skill README for inventory and maintenance conventions, not task-time rules.
- Add evaluations when they materially protect triggering or behavior.
- Keep credentials, tokens, personal data, and other secrets out of examples, logs, reports, and
  evaluation fixtures.

## Validation

A structurally valid skill is not necessarily ready for delivery. Formatting, links, repository
policies, and behavior may still fail independently.

Before delivery:

1. Run the focused validator for the modified skill.
2. Run repository formatting checks.
3. Run the complete repository validation command.
4. Run relevant triggering evaluations.
5. Run relevant behavioral evaluations.
6. Search for stale filenames, broken links, duplicated ownership, and unintended scope changes.
7. Inspect the complete diff.

When a validation step cannot be executed, report:

- the exact command not run;
- why it was blocked;
- which behavior remains unverified.

Do not describe evaluation definitions as passing results unless they were actually executed.

Repository-specific commands and required authoring workflows belong in `AGENTS.md`, the relevant
template, or another operational guide. This document defines the conceptual validation model.

## Authoring Templates

- [Skill Template](./skill-template.md) defines the operational contract for `SKILL.md`.
- [Reference Card Template](./reference-card-template.md) defines one rule card in `references/`.

Use the templates together with this document:

- this document defines package anatomy and ownership principles;
- the skill template defines the entry-point shape;
- the reference-card template defines detailed normative cards;
- repository instructions define the required editing and validation workflow.
