---
name: '{{SKILL_NAME}}'
description: '{{DESCRIPTION}}'
# MANAGE_SKILLS_LICENSE_BEGIN
license: '{{LICENSE}}'
# MANAGE_SKILLS_LICENSE_END
# MANAGE_SKILLS_ALLOWED_TOOLS_BEGIN
allowed-tools: '{{ALLOWED_TOOLS}}'
# MANAGE_SKILLS_ALLOWED_TOOLS_END
# MANAGE_SKILLS_METADATA_BEGIN
metadata:
  author: '{{AUTHOR}}'
  version: '{{VERSION}}'
# MANAGE_SKILLS_METADATA_END
# MANAGE_SKILLS_COMPATIBILITY_BEGIN
compatibility: '{{COMPATIBILITY}}'
# MANAGE_SKILLS_COMPATIBILITY_END
---

# {{SKILL_TITLE}}

{{OVERVIEW}}

## When to Apply

Use this skill when:

- {{TRIGGER_1}}
- {{TRIGGER_2}}

<!-- MANAGE_SKILLS_CATEGORIES_BEGIN -->

## Rule Categories by Priority

| Priority | Category       | Impact   | Prefix          |
| -------- | -------------- | -------- | --------------- |
| 1        | {{CATEGORY_1}} | CRITICAL | `{{PREFIX_1}}-` |
| 2        | {{CATEGORY_2}} | HIGH     | `{{PREFIX_2}}-` |

## Quick Reference

### 1. {{CATEGORY_1}} (CRITICAL)

- `{{PREFIX_1}}-{{SLUG_1}}` - {{RULE_DESCRIPTION_1}}
- `{{PREFIX_1}}-{{SLUG_2}}` - {{RULE_DESCRIPTION_2}}

### 2. {{CATEGORY_2}} (HIGH)

- `{{PREFIX_2}}-{{SLUG_3}}` - {{RULE_DESCRIPTION_3}}
- `{{PREFIX_2}}-{{SLUG_4}}` - {{RULE_DESCRIPTION_4}}

<!-- MANAGE_SKILLS_CATEGORIES_END -->

<!-- MANAGE_SKILLS_REFERENCES_BEGIN -->

## How to Use

Identify the applicable category and read only the relevant reference cards:

```text
references/{{PREFIX_1}}-{{SLUG_1}}.md
references/{{PREFIX_2}}-{{SLUG_3}}.md
```

<!-- MANAGE_SKILLS_REFERENCES_END -->
