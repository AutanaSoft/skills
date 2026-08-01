# Reference Card Template

Use this template for one rule card in a skill's `references/` directory. For the skill entry point,
see [Skill Template](./skill-template.md).

## Skeleton

````markdown
---
title: <Rule Title>
impact: <CRITICAL | HIGH | MEDIUM | LOW>
impactDescription: <Brief consequence or scope>
tags: <lowercase-kebab-case>, <lowercase-kebab-case>
---

## <Rule Title>

**Impact: <CRITICAL | HIGH | MEDIUM | LOW> (<Brief consequence or scope>)**

<Explain the rule and why it matters.>

**Incorrect (<what violates the rule>):**

```typescript
<Code that violates the rule>
```

**Correct (<what applies the rule>):**

```typescript
<Code that applies the rule>
```

Reference: [<Official source>](https://example.com)
````

## Atomicity

A card contains one primary rule or coherent decision. Related variants and alternatives may stay
together when they share the same scope, impact, and application criteria.

Split cards when their triggers, impacts, examples, or application conditions are independent. Link
related cards instead of copying their normative guidance.

## Card Contract

- `title` and the H2 are exactly the same.
- `impact` is `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
- `impactDescription` is present and explains the consequence, scope, or reason.
- Use at most four lowercase kebab-case tags.
- Include one focused `Incorrect` example and one focused `Correct` example for the same rule.
- Declare the language on every code block.
- Include at least one HTTPS reference and prefer official documentation.

## Checklist

- [ ] The card covers one rule or coherent decision.
- [ ] The frontmatter title matches the H2 exactly.
- [ ] The examples demonstrate the same decision.
- [ ] Related guidance is linked rather than duplicated.
