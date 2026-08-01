---
title: Language Policy
impact: LOW
impactDescription: Neutral professional output keeps the commit log reviewable across contributors
tags: style, language, english, neutral
---

## Language Policy

**Impact: LOW (Neutral professional output keeps the commit log reviewable across contributors)**

Commit messages are technical artifacts read by tools and humans across teams and time zones.
Default to neutral and professional English. Honor an explicit other-language request. Never inject
regional slang, dialect-specific grammar, or voseo unless the user explicitly asks.

**Incorrect (Spanish commit with regional slang and no scope):**

```text
chore: dale, acomodamos un toque el header del dashboard, che
```

**Correct (neutral English, with a Conventional Commit scope):**

```text
chore(ui): align dashboard header typography
```

**Incorrect (Spanish with voseo in a commit message):**

```text
fix(auth): arreglá el bug del refresh token expirado
```

**Correct (neutral professional English, no regional grammar):**

```text
fix(auth): reject expired refresh tokens
```

**Correct (Spanish, neutral and professional, when the user explicitly asks for Spanish):**

```text
feat(sessions): implementar rotación de tokens de refresco

Añadir seguimiento de la familia de tokens e invalidar los tokens de refresco previos al rotar.
```

Reference: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
