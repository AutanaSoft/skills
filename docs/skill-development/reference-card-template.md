# Reference Card Template

Use this structural foundation to create a card file in `references/`. For construction rules, see
the [Skill Development Guide](./skill-development-guide.md).

## Skeleton

````markdown
---
title: <Rule title>
impact: <CRITICAL | HIGH | MEDIUM-HIGH | MEDIUM | LOW-MEDIUM>
impactDescription: <Brief consequence or scope>
tags: <lowercase-kebab-case>, <lowercase-kebab-case>
---

## <Rule title>

<Normative paragraph defining the rule and why it matters.>

**Incorrect (<specific description of how the rule is violated>):**

```<language>
<Code that violates the rule>
```

**Correct (<specific description of how the rule is applied>):**

```<language>
<Code that applies the rule>
```

<!-- Add subsections or supporting examples only when the rule requires them. -->

Reference: [<Official source>](https://example.com)
````
