# Skill Template

Use this template to create or modify `SKILL.md`. For the conceptual model, see
[Skill Anatomy](./skill-anatomy.md).

## Skeleton

```markdown
---
name: <skill-name>
description: <what the skill does and when to use it>
license: <optional license identifier or relative path>
metadata:
  author: <optional author>
  version: <optional version>
compatibility: <optional runtime or dependency requirement>
allowed-tools: <optional runtime-specific tool restriction>
---

# <Skill Name>

<One paragraph describing the skill and its organization.>

## When to Apply

- <Concrete trigger>
- <Concrete trigger>

<!-- Include only when rules have categories. -->

## Rule Categories by Priority

| Priority | Category   | Impact | Prefix      |
| -------- | ---------- | ------ | ----------- |
| 1        | <Category> | HIGH   | `<prefix>-` |

## Quick Reference

- <Brief rule description> - `<prefix>-<slug>`

## How to Use

Read the card that applies to the task: `references/<prefix>-<slug>.md`.

<!-- Include only when a compiled document exists. -->

## Full Compiled Document

Read `AGENTS.md` for the complete guide.
```

Remove optional frontmatter fields and conditional sections that do not apply. The allowed fields
and their validator limits are defined in [Skill Anatomy](./skill-anatomy.md#frontmatter-contract).

## Content Contract

- `description` states both the capability and concrete trigger contexts.
- `name` is kebab-case and matches the skill directory.
- `Quick Reference` is a concise index. Use inline card names by default, such as `prefix-slug`.
- Use Markdown links in `Quick Reference` only when direct navigation adds value; keep one style
  consistent within the section.
- `How to Use` is for the consuming agent: it tells the agent which card to read and where it lives.
- Put normative rules, examples, exceptions, and external sources in reference cards.
- Put inventory and maintenance workflow in the skill README, never in `How to Use`.

## Create or Modify a Skill

1. Read the existing skill before changing it.
2. Confirm its scope and trigger contexts.
3. Put activation and navigation in `SKILL.md`, a single rule in a card, and maintenance details in
   the README.
4. Update the index and any affected relative links.
5. Run the repository validation and inspect the diff.

Create cards with the [Reference Card Template](./reference-card-template.md). Keep `SKILL.md` as
the entry point; do not duplicate card content in it.
