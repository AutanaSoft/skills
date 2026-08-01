---
title: Define Drizzle schema contracts in the database module
impact: HIGH
impactDescription: Maintains one owner for tables, relations, and persistence contracts
tags: drizzle, schema, contracts, database
---

## Define Drizzle schema contracts in the database module

**Impact: HIGH (maintains one owner for tables, relations, and persistence contracts)**

Keep tables, relations, migrations, and table-derived persistence contracts in the database module.
Consumers import public schema and types from that owner; application payloads and use-case inputs
remain outside it.

**Incorrect (a consumer defines a persistence table):**

```typescript
// features/users/users.table.ts
export const users = pgTable('users', { id: uuid('id').primaryKey() });
```

**Correct (the database module owns table-derived contracts):**

```typescript
// database/contracts/users.ts
export const userSelectSchema = createSelectSchema(users);
export type UserSelectRecord = z.infer<typeof userSelectSchema>;
```

Reference: [Drizzle ORM: Schema declaration](https://orm.drizzle.team/docs/sql-schema-declaration)
