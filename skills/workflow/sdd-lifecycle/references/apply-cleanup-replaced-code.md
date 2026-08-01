---
title: Clean obsolete code when replacing behavior
impact: HIGH
impactDescription:
  Prevents technical debt, duplicated UI, and dead code paths after applying changes
tags: apply, cleanup, replacement, dead-code, verify
---

## Clean obsolete code when replacing behavior

**Impact: HIGH (prevents technical debt, duplicated UI, and dead code paths after applying
changes)**

When an implementation replaces existing behavior, UI, data flows, components, or layouts, the work
is not complete if it only adds the new implementation. Replaced code must be removed or
consolidated.

This rule exists because agents tend to build on top of previous code without removing what became
obsolete. That creates screens with duplicated logic, dead imports, unused helpers, and old sections
that remain alive or hidden.

### Rule

If a change replaces an existing implementation:

1. Identify which previous code is superseded by the change.
2. Remove replaced markup, components, helpers, imports, and wiring.
3. Consolidate duplicated mapping/transformation logic into a single source of truth.
4. Update tests, stories, fixtures, or references that point to obsolete structures.
5. Verify that old and new versions are not rendered for the same concept.
6. Do not hide replaced code with CSS, temporary flags, or conditionals without explicit
   justification.

Replaced code must be **removed, not hidden**.

### Apply Checklist

- [ ] Existing components or sections replaced by the new implementation were identified.
- [ ] Unused imports were removed.
- [ ] Obsolete helpers/local state/mappers were removed.
- [ ] Old markup replaced by new components was removed.
- [ ] Duplicated logic was consolidated.
- [ ] Affected references, tests, or stories were updated.

### Verify Checklist

- [ ] The screen does not render old and new UI for the same concept.
- [ ] There are no obvious dead imports related to the replacement.
- [ ] There are no obsolete helpers or mappers related to the replacement.
- [ ] The change does not leave old code hidden with CSS or temporary conditionals.
- [ ] `apply-progress` documents which code was replaced or removed.

**Incorrect:**

```tsx
export function DashboardPage() {
  return (
    <>
      <LegacyMetrics />
      <NewMetrics />
      <LegacyTable className="hidden" />
      <DataTable data={data} config={config} />
    </>
  );
}
```

**Correct:**

```tsx
export function DashboardPage() {
  return (
    <>
      <NewMetrics />
      <DataTable data={data} config={config} />
    </>
  );
}
```
