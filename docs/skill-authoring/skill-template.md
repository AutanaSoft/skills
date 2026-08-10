# SKILL.md Template

Use this template as the structural foundation for creating or modifying a `SKILL.md` file. Remove
optional fields and conditional sections that do not apply. For skill construction rules, see
[Skill Anatomy](./skill-anatomy.md).

## Skeleton

````markdown
---
name: <skill-name>
description: <what the skill does and when to use it>
license: <optional license identifier or relative path>
metadata:
  author: <optional author>
  version: <optional version>
---

# <Skill Name>

<One paragraph describing the skill's purpose, scope, and organization.>

## When to Apply

Use this skill when:

- <Concrete trigger>
- <Concrete trigger>

<!-- Include categories and the quick reference only when the skill organizes
rules or decisions by category. -->

## Rule Categories by Priority

| Priority | Category   | Impact   | Prefix      |
| -------- | ---------- | -------- | ----------- |
| 1        | <Category> | CRITICAL | `<prefix>-` |
| 2        | <Category> | HIGH     | `<prefix>-` |

## Quick Reference

### 1. <Category> (CRITICAL)

- `<prefix>-<slug>` - <Brief rule or decision description>
- `<prefix>-<slug>` - <Brief rule or decision description>

### 2. <Category> (HIGH)

- `<prefix>-<slug>` - <Brief rule or decision description>
- `<prefix>-<slug>` - <Brief rule or decision description>

<!-- Include How to Use only when the skill has reference cards in references/. -->

## How to Use

Identify the applicable category and read only the relevant reference cards:

```text
references/<prefix>-<rule-or-decision>.md
references/<prefix>-<another-rule-or-decision>.md
```
````
