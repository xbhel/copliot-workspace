# DBA Checklist

Read this file when needed for:

- a deeper database review checklist
- a stable output template for schema, query, migration, or repair analysis
- a reusable risk rubric for database-heavy changes

## Quick Checklist

Before producing the final result, check these dimensions:

- [ ] Scope clarity: which tables, queries, migrations, code paths, and operational assumptions are in scope.
- [ ] Data correctness: keys, uniqueness, nullability, referential integrity, defaults, checks, and invariant enforcement.
- [ ] Query behavior: predicates, joins, ordering, pagination, batching, aggregation, and idempotency expectations.
- [ ] Index alignment: whether indexes match actual read and write paths, not just theoretical access.
- [ ] Migration safety: backward compatibility, sequencing, lock risk, rollout order, rollback path, and observability.
- [ ] Backfill or repair safety: batching, resumability, retry behavior, deduplication, auditability, and rerun safety.
- [ ] Concurrency and consistency: transaction boundaries, isolation assumptions, duplicate-write protection, and race-condition exposure.
- [ ] Performance evidence: explain plans, row-count assumptions, slow-query evidence, hot paths, and likely regressions.
- [ ] Validation coverage: tests, dry runs, staged rehearsal, data verification queries, and rollback rehearsal.

## High-Risk Database Prompts

Increase review depth for these change types:

- table rewrites, column type changes, constraint tightening, or large deletes
- backfills, repair jobs, reconciliation scripts, deduplication, or replay logic
- new uniqueness rules, foreign keys, cascading deletes, or partition changes
- high-volume writes, fan-out reads, hot counters, or ledger-like correctness
- pagination or ordering changes on large tables
- migration sequences that assume zero traffic, one-shot execution, or manual intervention

## Migration and Repair Safety Expectations

Prefer explicitly recording these checks:

- `Compatibility`: safe for mixed old and new application versions / not safe / unknown
- `Rollback`: clear rollback path / forward-fix only / unknown
- `Lock Risk`: low / medium / high / unknown
- `Backfill Strategy`: none / batched / online / blocking / unknown
- `Observability`: metrics or logs present / partial / missing

If the evidence is missing, say so directly. For example:

- static review only; no production-like row count evidence
- no explain plan or timing data was provided
- migration framework or engine version is unknown
- rollback relies on manual repair steps that were not documented

## Review Discipline

- MUST keep findings evidence-based and tied to specific schema, queries, migrations, or code paths.
- MUST prioritize data loss, corruption, integrity drift, and downtime risk over style or cosmetic issues.
- MUST separate confirmed problems from inferred risks.
- MUST explain when a recommendation depends on the database engine, version, or workload shape.
- MUST prefer safer staged rollout strategies over single-shot destructive changes.
- NEVER treat syntactically valid SQL as proof of safe production behavior.
- NEVER hide missing rollback, batching, or observability assumptions.
- NEVER claim a performance improvement is confirmed without plan or metric evidence.

## Database Review Template

```text
Database Analysis:

Summary:
- <what was reviewed and the overall risk shape>

Scope and Context:
- Artifacts: <files, queries, migrations, code paths>
- Database Context: <engine, version, scale, workload> or <unknown>
- Assumptions: <only the assumptions that affect conclusions>

Findings:

Critical:
- <impact>. Evidence: <file / query / plan / symbol>. [confirmed|inferred]

Major:
- <impact>. Evidence: <file / query / plan / symbol>. [confirmed|inferred]

Minor:
- <impact>. Evidence: <file / query / plan / symbol>. [confirmed|inferred]

Recommendations:
- <schema, query, migration, or repair action>

Validation:
- Explain or Metrics: <pass|fail|not run> (<optional detail>)
- Tests or Rehearsal: <pass|fail|not run> (<optional detail>)
- Rollback Check: <pass|fail|not run> (<optional detail>)

Open Questions / Assumptions:
- <only if confidence depends on them>
```
