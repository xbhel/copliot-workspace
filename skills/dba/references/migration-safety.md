# Migration Safety

Read this file when needed for:

- a deeper migration safety review
- staged rollout guidance for schema changes, backfills, and repair jobs
- a stable checklist for compatibility, locking, and rollback analysis

## Migration Framing

Before reviewing details, identify these basics:

- the database engine and version, or mark them unknown
- whether the change is online, maintenance-window only, or unclear
- the affected tables, expected row counts, write frequency, and critical read paths
- whether old and new application versions must coexist during rollout
- whether the change is additive, tightening, destructive, or a repair operation

## Safety Checklist

Before producing the final result, check these dimensions:

- [ ] Compatibility between old and new application versions during partial rollout.
- [ ] Whether the migration order is safe for readers, writers, background jobs, and replicas.
- [ ] Whether any DDL can rewrite a table, block writes, or hold long-lived locks.
- [ ] Whether index creation strategy is safe for the expected traffic and engine behavior.
- [ ] Whether backfills or repairs are batched, resumable, throttled, and observable.
- [ ] Whether retries are safe and whether repeated execution is idempotent when needed.
- [ ] Whether rollback is realistic, documented, and cheaper than forward repair.
- [ ] Whether data verification exists before constraint tightening, column removal, or cleanup.
- [ ] Whether cleanup steps depend on assumptions that may fail in production.

## Recommended Rollout Patterns

Prefer patterns like these when they fit the change:

1. Additive first: add new nullable columns, tables, or indexes before switching reads or writes.
2. Dual compatibility: keep old and new application versions working during the rollout window.
3. Backfill separately: decouple schema change from large data movement when possible.
4. Tighten later: add `NOT NULL`, stronger constraints, or destructive cleanup only after validation.
5. Clean up last: remove obsolete columns, indexes, triggers, or compatibility code in a later step.

## High-Risk Signals

Increase review depth when you see these patterns:

- one-step migrations that both change schema and backfill large volumes of data
- destructive DDL without a compatibility window
- type conversions on hot tables without engine-specific lock analysis
- updates or deletes without batching, ordering, or progress markers
- backfills that derive values from mutable business state without snapshot rules
- repair scripts that assume single execution or exclusive access
- rollback plans that are described only as "restore backup" without realistic timing

## Validation Expectations

Prefer explicitly recording these checks:

- `Compatibility Check`: pass / fail / not run
- `Migration Rehearsal`: pass / fail / not run
- `Data Verification`: pass / fail / not run
- `Rollback Rehearsal`: pass / fail / not run
- `Observability Readiness`: pass / fail / not run

Useful validation examples:

- rehearse on production-like row counts or a staging copy
- verify old and new application versions both work during the rollout window
- run row-count, null-check, and uniqueness verification queries before tightening constraints
- confirm monitoring or logs exist for migration progress, retries, and failures

## Migration Review Template

```text
Migration Safety Review:

Summary:
- <what is changing and the overall rollout risk>

Context:
- Engine and Version: <value> or <unknown>
- Affected Artifacts: <migration files, scripts, code paths>
- Rollout Assumptions: <compatibility window, maintenance window, traffic assumptions>

Findings:

Critical:
- <impact>. Evidence: <file / statement / code path>. [confirmed|inferred]

Major:
- <impact>. Evidence: <file / statement / code path>. [confirmed|inferred]

Minor:
- <impact>. Evidence: <file / statement / code path>. [confirmed|inferred]

Recommended Rollout:
- <ordered rollout or safer alternative>

Validation:
- Compatibility Check: <pass|fail|not run> (<optional detail>)
- Migration Rehearsal: <pass|fail|not run> (<optional detail>)
- Data Verification: <pass|fail|not run> (<optional detail>)
- Rollback Rehearsal: <pass|fail|not run> (<optional detail>)
- Observability Readiness: <pass|fail|not run> (<optional detail>)

Open Questions / Assumptions:
- <only if confidence depends on them>
```

## Review Discipline

- MUST prefer staged rollout advice over one-shot destructive changes when the safer path is viable.
- MUST surface engine-specific lock or rewrite risk when the DDL behavior depends on the engine.
- MUST highlight when rollback is unrealistic and a forward-fix plan is the real recovery path.
- MUST separate confirmed operational risk from general caution.
- NEVER assume maintenance-window exclusivity unless the artifacts or user explicitly confirm it.
- NEVER treat unbounded backfills or repairs as safe by default.
