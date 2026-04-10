# Review Checklist

Read this file when needed for:

- a more detailed code review checklist
- a stable PR review output template

## Quick Checklist

Before producing the final review, check these dimensions:

- Check requirement coverage against known requirements, acceptance criteria, and design constraints.
- Check correctness for logic bugs, missing guards, boundary issues, and regression risks.
- Check data and state handling for consistency issues, duplicate writes, concurrency risks, and idempotency gaps.
- Check error handling for exceptions, timeouts, nulls, rollback behavior, and user-visible failures.
- Check interface compatibility for callers, return values, events, schemas, and config.
- Check test coverage for the happy path, edge cases, and failure modes.
- Check whether lint, build, and tests passed or whether evidence is missing.
- Check design alignment against the existing architecture and complexity expectations.
- Check maintainability for naming, readability, duplication, coupling, and comments.

## High-Risk Review Prompts

Increase review depth for these change types:

- authentication, authorization, permissions, tenant isolation
- money, billing, inventory, order state
- deletion, migration, batch processing, retry logic, compensation logic
- cache behavior, consistency, concurrency, queues, async jobs
- API contracts, database schema, event formats
- feature flags, rollout paths, rollback paths

## Validation Expectations

Prefer recording these statuses:

- `Lint`: pass / fail / not run
- `Tests`: pass / fail / not run
- `Build`: pass / fail / not run

If validation did not run, state why. For example:

- static review only
- missing local dependencies
- current environment cannot execute the commands
- user did not ask for validation and the repository has no stable commands

## Review Discipline

- MUST keep findings evidence-based.
- MUST keep the review scoped to the requested change.
- MUST report validation gaps explicitly.
- MUST separate confirmed issues from inferred risks.
- NEVER treat stylistic preference as a blocking issue.
- NEVER hide uncertainty.
- NEVER claim validation passed without command evidence.

## PR Review Template

```text
Review Findings:

Critical:
- <impact>. Evidence: <file:line / symbol / command>. [confirmed|inferred]

Major:
- <impact>. Evidence: <file:line / symbol / command>. [confirmed|inferred]

Minor:
- <impact>. Evidence: <file:line / symbol / command>. [confirmed|inferred]

Open Questions / Assumptions:
- <only if it affects confidence>

Validation:
- Lint: <pass|fail|not run> (<optional detail>)
- Tests: <pass|fail|not run> (<optional detail>)
- Build: <pass|fail|not run> (<optional detail>)

Verdict:
- <pass|pass with notes|re-review required>
```
