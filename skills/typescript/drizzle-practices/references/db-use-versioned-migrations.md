---
title: Use reviewed versioned Drizzle migrations
impact: HIGH
impactDescription: Preserves traceability and reviewability for shared database schema changes
tags: drizzle, migrations, schema, safety
---

## Use reviewed versioned Drizzle migrations

**Impact: HIGH (preserves traceability and reviewability for shared database schema changes)**

For shared or production environments, generate versioned migrations, review the generated SQL and
metadata, then apply the migration. Do not use schema push as a substitute for a reviewed migration.
Review destructive changes, nullability, foreign keys, unique indexes, renames, and type changes
especially carefully.

**Incorrect (pushes a shared schema change directly):**

```bash
drizzle-kit push
```

**Correct (generates and reviews a migration):**

```bash
drizzle-kit generate
drizzle-kit migrate
```

Reference: [Drizzle ORM: Migrations](https://orm.drizzle.team/docs/migrations)
