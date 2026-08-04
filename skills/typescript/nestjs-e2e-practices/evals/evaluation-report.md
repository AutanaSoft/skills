# Behavioral Evaluation Report

The initial evaluation compared three representative prompts with `nestjs-e2e-practices` against a
baseline that did not load an E2E skill. Independent agents produced each answer without modifying
the repository.

## Results

| Evaluation                               | With skill | Baseline  | Material difference                                                                                              |
| ---------------------------------------- | ---------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| Auth and users structure                 | 6/6        | 2/6       | The skill produced one discovered main orchestrator, explicit feature registration, and global ownership         |
| Forgot-password email boundary           | 5/5        | 4/5       | Both isolated the transport; only the skill explicitly reported that deliverability remains outside E2E coverage |
| Duplicate discovery, fixtures, contracts | 6/6        | 4/6       | The skill added global lifecycle ownership and explicit sensitive-field assertions                               |
| **Total**                                | **17/17**  | **10/17** | The skill improved orchestration, ownership, and security evidence                                               |

## Findings

- The structure evaluation discriminates strongly: the baseline created independently discovered
  auth and users specs, each with its own application lifecycle. The skill created one
  Jest-discovered main entry point and imported non-discovered feature suites.
- The external-boundary rule is partly available from general NestJS knowledge, so its strongest
  discriminators are explicit residual scope and centralized boundary ownership.
- The repair evaluation confirms that the skill connects Jest discovery, fixture isolation, public
  contracts, sensitive-field absence, and application ownership instead of treating them separately.
- A post-implementation review found that the first draft described the ownership model but omitted
  the complete recommended file tree from the executable card. The orchestration card now includes
  the canonical `support/`, `fixtures/`, feature orchestrator, context, and endpoint-suite layout.
- No repository files were modified by evaluation agents.

## Limitations

- The task runner did not expose token or wall-clock metrics, so timing and token comparisons were
  not recorded.
- A benchmark viewer was not generated because the evaluation runs returned conversational outputs
  rather than persisted run directories in the `skill-creator` workspace schema.
- Triggering queries are prepared separately and still require human review before optimization.
