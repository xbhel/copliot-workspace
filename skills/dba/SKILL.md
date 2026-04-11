---
name: dba
description: Analyze database design, queries, schema changes, and data access risks for an application. Use this skill when work involves schema design, query review, migrations, or database performance concerns.
allowed-tools: read_file grep_search file_search semantic_search list_dir run_in_terminal get_errors get_changed_files runSubagent
metadata:
	version: 1.1.0
	author: xbhel
---

# DBA

## Goal

Produce a structured, evidence-based database analysis that evaluates schema design, query behavior, migration safety, data repair plans, and performance risks, then turns the result into concrete findings, recommendations, and validation steps.

## When to Use

Use this skill when:

- the task includes schema design, migrations, or query changes
- database correctness, integrity, or performance needs review
- application behavior depends on database constraints or data access patterns

## Inputs

| name | description | default | required | source | example |
| ---- | ----------- | ------- | -------- | ------ | ------- |
| requirements | The user's database-related task, concern, or change request. | none | Yes | user or upstream | Review this migration for safety. |
| artifacts | The concrete database artifacts to inspect, such as DDL, SQL, migrations, ORM code, execution plans, metrics, or backfill scripts. | discovered from context | No | user or derived | migrations/20260411_add_order_status.sql |
| db_context | Database engine, version, scale, workload shape, data sensitivity, rollout constraints, or other environmental details that materially affect the analysis. | database-agnostic assumptions | No | user or derived | PostgreSQL 16, 50M rows, zero-downtime rollout |
| review_scope | The requested focus, such as design correctness, migration safety, query performance, consistency, or data repair risk. | correctness, safety, and validation | No | user or derived | Focus on performance and rollback safety. |

## Context

- Treat this skill as database-agnostic by default. Prefer engine-neutral guidance unless `{db_context}` or the artifacts clearly indicate a specific engine.
- When the database engine matters, make dialect-specific behavior explicit instead of implying that one engine's rule applies everywhere.
- Read `references/dba-checklist.md` when the task needs a deeper checklist, a stable report structure, or a reusable migration and performance review rubric.
- Read `references/migration-safety.md` when the task centers on rollout sequencing, locking risk, backfills, repairs, or rollback planning.
- Read `references/query-performance.md` when the task centers on slow queries, missing plans, index fit, fan-out access patterns, or query-shape regressions.
- Use surrounding application code and tests to understand how the database is used; do not analyze SQL or schema in isolation when calling code materially changes the risk.

## Core Principles

- MUST anchor the analysis in concrete evidence from `{artifacts}`, related code, tests, commands, or metrics.
- MUST confirm or infer the narrowest safe scope from `{requirements}` and `{review_scope}` before expanding the analysis.
- MUST distinguish correctness risks, migration risks, performance risks, and operational risks instead of collapsing them into one generic judgment.
- MUST make data loss, corruption, integrity, and downtime risks the highest priority.
- MUST call out missing constraints, missing indexes, unsafe backfills, unclear rollback paths, and hidden compatibility assumptions when they matter.
- MUST treat application query patterns, transaction boundaries, and ORM behavior as part of the analysis when they influence database risk.
- MUST mark uncertainty explicitly when row counts, execution plans, lock behavior, or dialect details are inferred rather than confirmed.
- MUST stay database-agnostic unless a specific engine or version is confirmed.
- MUST propose the least risky viable approach when multiple schema or migration options exist.
- MUST provide validation steps that would let a developer or reviewer verify the recommendation safely.
- NEVER assume a migration is safe just because the SQL is syntactically valid.
- NEVER recommend destructive data changes, constraint tightening, or large backfills without discussing compatibility, batching, and rollback implications.
- NEVER present speculative tuning advice as a confirmed performance fix when no plan, metric, or workload evidence exists.

## Workflow

### 1. Frame the Database Task

- Identify the exact database concern from `{requirements}`.
- Gather the primary artifacts from `{artifacts}` and nearby code.
- Infer the effective scope from `{review_scope}` when the request is broad.
- Confirm whether the task is mainly about one or more of these areas:
	- schema or data model design
	- query correctness or performance
	- migration or rollout safety
	- data repair, backfill, or reconciliation
	- consistency, locking, or transaction behavior

### 2. Gather Evidence

- Locate relevant schema files, migrations, ORM models, repositories, query builders, raw SQL, tests, and run commands.
- Read surrounding code to understand how data is created, updated, deleted, queried, and repaired.
- Inspect execution evidence when available, such as explain plans, slow-query samples, row-count assumptions, or timing data.
- Establish the minimum relevant context from `{db_context}`: engine, version, scale, traffic pattern, rollout limits, and data sensitivity.
- Use application-level evidence before asking follow-up questions; only escalate when the missing detail materially changes the conclusion.

### 3. Analyze the Design and Data Model

- Check keys, uniqueness, nullability, defaults, check constraints, referential integrity, and lifecycle fields.
- Check whether the schema reflects ownership boundaries, invariants, retention needs, and deletion behavior.
- Review normalization, denormalization, auditability, soft-delete behavior, and historical data needs where relevant.
- Look for compatibility risks introduced by new columns, dropped columns, renamed fields, type changes, or constraint tightening.

### 4. Analyze Query and Access Patterns

- Use `references/query-performance.md` when query shape, indexing, or hot-path behavior carries most of the risk.
- Trace the read and write paths that use the affected tables or queries.
- Check predicates, joins, ordering, pagination, aggregation, batching, and idempotency behavior.
- Identify likely hot paths, N+1 patterns, redundant round-trips, full scans, wide updates, and expensive sorts or aggregations.
- Compare index strategy to actual access patterns instead of reviewing indexes in isolation.
- If execution evidence is missing, separate likely risks from confirmed regressions.

### 5. Analyze Migration and Repair Safety

- Use `references/migration-safety.md` when the migration path, repair plan, or compatibility window carries most of the risk.
- Review rollout order, backward compatibility, deploy sequencing, and reader or writer compatibility.
- Check for table rewrites, long locks, blocking DDL, index build strategy, backfill batching, and retry behavior.
- Verify whether the migration or repair plan is resumable, observable, idempotent when required, and safe to rerun.
- Check rollback strategy, failure recovery, and cleanup behavior.
- Surface any assumptions about traffic freezes, maintenance windows, or one-time execution that are not explicitly justified.

### 6. Analyze Consistency and Concurrency Risk

- Check transaction boundaries, isolation assumptions, lock scope, write ordering, and duplicate-write protection.
- Look for race conditions between application logic and database constraints.
- Verify whether uniqueness, foreign keys, version columns, or other guards actually enforce the intended invariant.
- Treat missing invariant enforcement as a correctness finding, not just a design preference.

### 7. Produce the Result

- Use `references/dba-checklist.md` for deeper coverage when needed.
- Summarize findings in severity order using these priorities:
	- `Critical`: data loss, corruption, integrity break, uncontrolled downtime, or missing rollback path for a risky change
	- `Major`: significant migration risk, performance regression risk, missing enforcement, unsafe backfill, or important observability gap
	- `Minor`: lower-impact maintainability, naming, consistency, or optimization issue
- For each finding, include the impact, the concrete evidence, why it matters, and whether it is `[confirmed]` or `[inferred]` when that distinction matters.
- Follow findings with concrete recommendations, validation steps, and any open questions that affect confidence.

## Output

Produce a concise database analysis with this structure:

1. `Summary`: what was analyzed and the overall risk shape.
2. `Scope and Context`: relevant artifacts, boundaries, database context, and assumptions.
3. `Findings`: ordered by severity with impact, evidence, and `[confirmed]` or `[inferred]` markers where needed.
4. `Recommendations`: concrete schema, query, migration, indexing, batching, or rollback actions.
5. `Validation`: focused checks to confirm safety, such as tests, explain-plan review, staged migration rehearsal, row-count validation, or rollback rehearsal.
6. `Open Questions / Assumptions`: only the unresolved points that affect confidence.

If no findings are discovered, say so explicitly and still report any residual validation gaps.

## Error Handling

- If the database artifacts cannot be located, stop and ask for the minimum missing artifact or path.
- If the database engine or scale materially affects the result and cannot be inferred, state the ambiguity and give conditional guidance rather than false certainty.
- If execution evidence is unavailable, continue with a static review and mark performance conclusions as inferred where appropriate.
- If the task spans multiple independent database concerns, split the analysis by concern and report the highest-risk area first.

## Examples

```text
User: Review this migration that adds a non-null status column to orders and backfills old rows.

You:
Summary:
- Reviewed the new `orders.status` column, its backfill plan, and the calling write paths. Overall risk is moderate because the column is added safely, but the backfill and constraint tightening sequence is incomplete.

Findings:
Major:
- The migration adds `status` as `NOT NULL` before the backfill is guaranteed complete, which can fail on existing rows or block writers depending on the engine. Evidence: `migrations/20260411_add_order_status.sql`, `OrderRepository.save()`. [confirmed]

Recommendations:
- Add the column as nullable first, deploy dual-write behavior if needed, backfill in batches, validate completion, then tighten the constraint in a later migration.

Validation:
- Rehearse the migration on production-like row counts.
- Verify no `orders` rows remain null before tightening the constraint.
- Review the query plan for the backfill predicate and the new status lookup path.
```
