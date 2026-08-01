---
title: Use transactions for coordinated Drizzle writes
impact: HIGH
impactDescription: Prevents partial writes by sharing one transaction client across the workflow
tags: drizzle, transactions, consistency, repositories
---

## Use transactions for coordinated Drizzle writes

**Impact: HIGH (prevents partial writes by sharing one transaction client across the workflow)**

Open a transaction at the workflow coordinator and pass its `tx` client to every participating data
access operation, including reads that determine later writes. Do not open independent or nested
transactions in repositories; keep unrelated slow external I/O outside the transaction.

**Incorrect (related writes use the default client):**

```typescript
await usersRepository.create(user);
await profilesRepository.create(profile);
```

**Correct (the workflow shares one transaction):**

```typescript
await db.transaction(async (tx) => {
  await usersRepository.create(user, tx);
  await profilesRepository.create(profile, tx);
});
```

Reference: [Drizzle ORM: Transactions](https://orm.drizzle.team/docs/transactions)
