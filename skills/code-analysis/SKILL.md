---
name: code-analysis
description: Analyze an existing codebase, or a specific area within a codebase, to build a clear, evidence-based understanding of how it works, how its parts interact, and how it can be changed or extended safely. Use this skill before implementation, debugging, refactoring, design, estimation, or review.
metadata:
  version: 1.0.1
  author: xbhel
---

## Goal

Produce a structured, evidence-based analysis of a target codebase area, including how it works, how it interacts with surrounding code, and what constraints, extension points, gaps, or risks are relevant, with sufficient detail to support design, implementation, debugging, refactoring, estimation, and review.

## When to Use

Use this skill when:

- you need working context before implementation, debugging, refactoring, or review
- behavior must be traced across files, modules, or execution paths
- interfaces, dependencies, conventions, or extension points must be mapped
- tests, run context, or likely risks need to be identified for the target area

## Core Principles

- **Evidence first:** Every finding should point to concrete evidence (file, symbol, test, or command).
- **Stay in scope:** Analyze only what the task needs.
- **Observe before prescribing:** Describe current behavior before suggesting changes.
- **Treat gaps as findings:** Missing tests, unclear seams, and undocumented constraints matter.
- **Mark uncertainty when needed:** Use `[confirmed]` and `[inferred]` where the distinction matters.

## Workflow

1. Locate relevant files, modules, entry points, components, and tests within the target scope.
2. Trace control flow, data flow, state changes, and side effects through the implementation.
3. Identify architectural patterns, abstractions, interfaces, dependencies, and runtime assumptions.
4. Review similar implementations for consistency, divergence, and reuse opportunities.
5. Examine tests, build scripts, and run commands to infer expected behavior and edge cases.
6. Summarize findings, inferences, ambiguities, and gaps using the checklist below.

### Analysis Checklist

| Area | What to capture |
| --- | --- |
| Scope                     | Relevant files, modules, entry points, boundaries, and what is context only.                       |
| Responsibilities          | Primary responsibilities and ownership boundaries of relevant modules and components.              |
| Behavior                  | Key execution paths, control flow, data flow, state changes, side effects, and failure behavior.   |
| Architecture              | Dominant patterns, abstractions, module relationships, and separation of concerns.                 |
| Conventions               | Naming, organization, validation, error handling, and local standards.                             |
| Interfaces                | Public APIs, internal contracts, extension points, and integrations.                               |
| Dependencies              | Libraries, shared modules, services, data stores, config, and runtime assumptions.                 |
| Reference Implementations | Similar implementations worth reusing, matching, or using as behavioral references.                |
| Tests and Validation      | Test layout, frameworks, useful commands, expected behavior, and coverage signals.                 |
| Build and Run Context     | Build scripts and run commands relevant to the target area.                                        |
| Gaps and Constraints      | Missing tests, unclear ownership, ambiguity, hidden coupling, and limits.                          |

## Output

Output a comprehensive analysis that captures the relevant checklist areas with concrete evidence. 

## Examples

```text
User: Codebase Analysis (focus: auth token refresh flow)

You:

Summary:
- `HttpClient.request()` retries once after a `401` by calling `refresh_access_token()` and replaying the original request. [confirmed]

Scope:
- Included: `src/auth/refresh.py`, `src/http/client.py`, `tests/auth/test_refresh.py`
- Context only: `src/auth/errors.py`

Behavior:
- `client.py` detects `401`, delegates token rotation to `refresh.py`, then replays the request with updated credentials. [confirmed]
- Concurrent refresh handling is not obvious from the current implementation. [inferred]

Architecture:
- `refresh.py` owns token rotation and persistence
- `client.py` owns retry orchestration and request replay [confirmed]

Conventions:
- Domain-specific auth errors come from `src/auth/errors.py`
- Token storage stays in `refresh.py`, not `client.py` [confirmed]

Reference Implementation:
- `src/payments/session_refresh.py` is the closest retry-then-refresh flow [confirmed]

Tests and Validation:
- Covers successful refresh and expired refresh token handling
- Missing an explicit test for concurrent refresh attempts [confirmed]
- Relevant command: `uv run pytest tests/auth/test_refresh.py` [confirmed]

Gaps and Risks:
- Retry count is hard-coded in `client.py`, so changing refresh behavior may affect all `401` handling paths.
```
