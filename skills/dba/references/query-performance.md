# Query Performance

Read this file when needed for:

- a deeper query and indexing review
- slow-query, N+1, fan-out, or hot-path analysis
- a stable checklist for plans, predicates, joins, pagination, and validation

## Performance Framing

Before reviewing details, identify these basics:

- the query or query family being analyzed
- the database engine and version, or mark them unknown
- the relevant tables, approximate row counts, and expected cardinality
- the latency or throughput symptom, if one exists
- whether execution evidence exists, such as explain plans, query counts, timing samples, or slow-query logs

## Query Review Checklist

Before producing the final result, check these dimensions:

- [ ] Query shape: predicates, joins, grouping, ordering, pagination, and projection width.
- [ ] Access pattern: point lookup, range scan, batch fetch, fan-out, repeated per-row query, or full-table work.
- [ ] Index fit: whether the existing or proposed indexes match the actual filter, join, and sort keys.
- [ ] Cardinality risk: whether row-count assumptions, selectivity, or skew can invalidate the expected plan.
- [ ] N+1 or chatty access: whether the application issues avoidable repeated queries or round-trips.
- [ ] Write amplification: whether the optimization adds costly indexes, wide updates, or expensive maintenance overhead.
- [ ] Pagination safety: whether ordering is stable and whether offset-based scans become too expensive at scale.
- [ ] Validation evidence: explain plans, timings, query counts, tracing, or staged load checks.

## High-Risk Signals

Increase review depth when you see these patterns:

- repeated per-parent or per-row queries in request handling or background jobs
- queries that sort or aggregate large tables without a matching access path
- offset pagination on large, frequently changing datasets
- wildcard projection or wide-row fetching on hot paths
- filtering on low-selectivity columns without additional narrowing predicates
- index recommendations that improve one read path while sharply increasing write cost
- performance claims made without explain-plan, query-count, or latency evidence

## Review Discipline

- MUST distinguish confirmed performance evidence from inferred risk when no plan or metrics are available.
- MUST evaluate indexes against real predicates, joins, and ordering requirements.
- MUST consider application query count and round-trip patterns, not only individual SQL text.
- MUST discuss write-side trade-offs when recommending new indexes or materialized access paths.
- MUST highlight when pagination or ordering behavior can become unstable or expensive at scale.
- NEVER present a speculative index recommendation as a proven fix without validation guidance.
- NEVER ignore N+1 or fan-out query patterns simply because each individual query appears simple.

## Validation Expectations

Prefer explicitly recording these checks:

- `Explain Plan`: pass / fail / not run
- `Query Count Check`: pass / fail / not run
- `Latency Check`: pass / fail / not run
- `Index Impact Review`: pass / fail / not run

Useful validation examples:

- capture explain or explain analyze for representative parameter values
- measure request-level query counts before and after the change
- compare p95 or p99 latency on representative datasets
- verify index usage against the actual filter, join, and sort shape

## Query Review Template

```text
Query Performance Review:

Summary:
- <what query path was reviewed and the overall performance risk>

Context:
- Engine and Version: <value> or <unknown>
- Affected Queries or Code Paths: <queries, repositories, handlers>
- Evidence Available: <plans, timings, query counts> or <static review only>

Findings:

Critical:
- <impact>. Evidence: <query / plan / file / symbol>. [confirmed|inferred]

Major:
- <impact>. Evidence: <query / plan / file / symbol>. [confirmed|inferred]

Minor:
- <impact>. Evidence: <query / plan / file / symbol>. [confirmed|inferred]

Recommendations:
- <query-shape, indexing, batching, caching, or pagination action>

Validation:
- Explain Plan: <pass|fail|not run> (<optional detail>)
- Query Count Check: <pass|fail|not run> (<optional detail>)
- Latency Check: <pass|fail|not run> (<optional detail>)
- Index Impact Review: <pass|fail|not run> (<optional detail>)

Open Questions / Assumptions:
- <only if confidence depends on them>
```
