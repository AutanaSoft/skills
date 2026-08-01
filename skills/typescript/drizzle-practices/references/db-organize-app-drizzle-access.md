---
title: Organize Drizzle access in owning server modules
impact: HIGH
impactDescription: Prevents data queries from leaking into UI and framework layers
tags: drizzle, data-access, architecture, server
---

## Organize Drizzle access in owning server modules

**Impact: HIGH (prevents data queries from leaking into UI and framework layers)**

Keep Drizzle queries in server-side modules owned by the feature or domain. Import the database
client and persistence contracts from public package exports. Separate typed read models from
commands that validate authorization and input before writing.

**Incorrect (a UI layer imports internal database modules):**

```typescript
import { db } from '@repo/database/src/client';

export async function renderView() {
  return db.select().from(records);
}
```

**Correct (an owning server module uses a public export):**

```typescript
import { db, records } from '@repo/database';

export async function listRecords() {
  return db.select({ id: records.id, status: records.status }).from(records);
}
```

Reference: [Drizzle ORM: Select](https://orm.drizzle.team/docs/select)
