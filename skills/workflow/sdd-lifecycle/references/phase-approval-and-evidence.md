---
title: Respect SDD phase gates, approval, and evidence
impact: HIGH
impactDescription: Prevents implementing from drafts and verifies that work has real evidence
tags: phase, approval, tdd, evidence, verify
---

## Respect SDD phase gates, approval, and evidence

**Impact: HIGH (prevents implementing from drafts and verifies that work has real evidence)**

Each SDD phase has dependencies and expected evidence. Implementing from unapproved artifacts breaks
the work contract.

### Phase Guidance

| Phase   | Primary Artifact                        | Lifecycle Guidance                                                        |
| ------- | --------------------------------------- | ------------------------------------------------------------------------- |
| Idea    | `*.idea.md`                             | Usually `draft`; archive or supersede after PRD/spec approval.            |
| PRD     | `*.prd.md`                              | Product intent and criteria; avoid technical test details.                |
| Spec    | `*.component-spec.md`, `*.page-spec.md` | Observable behavior and verifiable criteria.                              |
| Design  | `design.md`                             | Technical decisions, architecture, testing strategy, and validation plan. |
| Tasks   | `tasks.md`                              | Executable checklist; must reflect design and test capability.            |
| Apply   | `apply-progress.md`                     | Implementation evidence; Strict TDD requires RED/GREEN/REFACTOR evidence. |
| Verify  | `verify-report.md`                      | Verification evidence and PASS/FAIL/WARNING findings.                     |
| Archive | `archive-report.md`                     | Final synchronization and closure.                                        |

### Implementation Approval Gate

Before writing code in an Apply phase:

1. Read the current PRD, spec, design, and tasks.
2. Check the lifecycle status of each required artifact.
3. If any required artifact is `draft` or `reviewed`, do not implement yet.
4. Ask the user for explicit approval.
5. After explicit approval, update source artifacts to `approved` when appropriate, append
   `Change Log`, and mark tasks/apply-progress as `in_progress`.

Do not treat recommendations, assumptions, or generated drafts as approved contracts. Implementation
can proceed only from `approved` artifacts or from an explicit user statement such as
`approved for implementation`.

### Strict TDD Cycle Evidence

When Strict TDD is active or the workspace has tests, `apply-progress` must include:

```md
## TDD Cycle Evidence

| Task | RED | GREEN | TRIANGULATE | SAFETY NET | REFACTOR | Commands |
| ---- | --- | ----- | ----------- | ---------- | -------- | -------- |
```

Use this as the official `Strict TDD Cycle Evidence` format.

- Use one row per meaningful task or behavior, not one row for the whole feature.
- `RED` must show the failing test, missing behavior, or expected failure before implementation.
- `GREEN` must show the passing evidence after implementation.
- `TRIANGULATE` must show at least one additional example, edge case, or behavior that prevents
  overfitting.
- `SAFETY NET` must identify existing tests, validations, or checks that protected previously
  working behavior.
- `REFACTOR` must state what changed after tests were green, or explicitly say no refactor was
  needed.
- `Commands` must list the exact commands run and their results.

Verification must fail or block if required tests were run but this evidence is missing, incomplete,
or too coarse to audit.
