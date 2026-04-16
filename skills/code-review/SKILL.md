---
name: code-review
description: Review code changes for correctness, regressions, requirement coverage, test quality, design alignment, and delivery risk. Use this skill when asked to review a pull request, diff, commit, patch, or implementation and produce prioritized findings with concrete evidence and a clear verdict.
allowed-tools: read_file grep_search file_search semantic_search list_dir run_in_terminal get_terminal_output get_errors get_changed_files search_subagent runSubagent vscode_listCodeUsages fetch_webpage
metadata:
  version: 1.1.0
  author: xbhel
---

# Code Review

## Goal

Produce an evidence-based review of a change, prioritizing correctness, regressions, requirement gaps, design drift, and validation gaps over style feedback.

## When to Use

- The user asks for a code review, PR review, patch review, commit review, or diff review.
- A change must be evaluated before merge or handoff.
- The task is to find bugs, regressions, requirement gaps, test gaps, or risky design choices.

## Inputs

| name | description | default | required | source | example |
| ---- | ----------- | ------- | -------- | ------ | ------- |
| changes | The code under review: pull request, diff, commit range, changed files, or branch comparison. | current working change | Yes | user or derived | PR #42 |
| requirements | Confirmed requirements, acceptance criteria, expected behavior, or approved design constraints for the change. | none | No | user or upstream | "Add retry on 429 responses and keep retry logic in `http/client.py`." |
| review_scope | Boundaries for the review, such as files, modules, risks, or whether style feedback is wanted. | correctness, tests, lint, and design alignment | No | user or derived | "Focus on auth refresh flow." |

## Context

- The actual diff is the primary review artifact when it is available.
- Surrounding code, related tests, and validation commands provide the minimum context needed to verify behavior.
- Review requests may arrive without complete requirements or design context, so some intent may need to be inferred from code.
- Unrelated local changes may exist in the workspace and should be treated as out of scope.
- [review-checklist.md](./references/review-checklist.md) contains a reusable checklist and PR review template for deeper or more standardized reviews.

## Core Principles

- MUST present findings before summaries.
- MUST prioritize correctness, security, regressions, requirement gaps, data loss, concurrency issues, and missing validation before style feedback.
- MUST review the actual diff when it is available.
- MUST read surrounding code when needed to verify behavior.
- MUST treat code review as a validation task, not an editing task, unless the user explicitly asks for fixes.
- MUST stay tightly scoped to the requested review target, even when unrelated local changes exist.
- MUST infer cautiously from code when requirements are missing and MUST state uncertainty explicitly.
- MUST support every finding with concrete evidence such as a file, symbol, code path, test, or command result.
- MUST review behavior, not just syntax, by tracing execution paths and side effects through the touched code.
- MUST distinguish confirmed facts from inference whenever the distinction affects confidence.
- MUST treat missing tests as findings when the change introduces unverified behavior or risk.
- MUST treat missing lint or build validation as review findings when important behavior remains unverified.
- MUST label pre-existing issues as pre-existing and MUST NOT block the reviewed change on them unless they materially affect it.
- MUST keep the review proportional to the change.
- MUST mark the review as partial when validation could not run.
- NEVER lead with compliments, generic summaries, or stylistic commentary.
- NEVER invent requirements, expected behavior, or design intent without evidence.
- NEVER inflate the report with speculative, low-confidence, or low-value nits.

## Workflow

### 1. Frame the Review

- Identify the exact review target: PR, diff, commit range, files, or local changes.
- Confirm the intended scope from `{review_scope}` and `{requirements}` when available.
- Infer the narrowest safe scope from repository state and user context when the target is ambiguous.

### 2. Gather Context

- Read the changed files and the nearby code needed to understand execution paths.
- Review related tests, fixtures, and build or validation commands relevant to the touched area.
- Look for reference implementations or existing patterns that the change should match.
- Use surrounding code to recover missing requirements when possible.

### 3. Check Requirement Coverage

- Verify that the change satisfies the known requirements and acceptance criteria from `{requirements}`.
- Flag missing behavior, partial implementations, and scope drift.
- Report ambiguous behavior as a risk when evidence is insufficient.
- Do not invent a requirement to make the review sound complete.

### 4. Check Correctness and Regression Risk

- Trace the main execution paths affected by the change.
- Check validation, error handling, boundary conditions, state transitions, side effects, retries, cleanup, and failure behavior.
- Check for these common regression classes:
  - incorrect branching or missing guards
  - stale assumptions about inputs, nullability, or data shape
  - broken compatibility with existing callers or contracts
  - race conditions, duplicate work, ordering bugs, or idempotency gaps
  - security, authorization, or secrets-handling mistakes
  - performance regressions: algorithmic complexity changes, N+1 queries, hot-path inefficiencies, or unnecessary allocations
  - observability or rollback gaps for risky changes

### 5. Check Tests and Validation

- Inspect whether tests cover the happy path, important edge cases, and failure modes introduced by the change.
- Prefer meaningful assertions over superficial execution.
- Run focused validation commands when practical and allowed.
- Confirm lint status in addition to tests and build checks when the project has a lint path.
- Report what remains unverified when lint, tests, or build validation are absent, weak, or not run.
- Do not imply that a change is fully validated when lint, tests, or build checks did not run.

### 6. Check Design Alignment and Maintainability

- Compare the implementation against requirements and existing architectural patterns.
- Flag unnecessary complexity, hidden coupling, ownership drift, and misplaced responsibilities.
- Check whether the change requires documentation updates when it modifies APIs, configuration, schemas, or observable behavior.
- Distinguish maintainability risks from subjective style preferences.
- Do not present personal style preferences as blocking findings.

### 7. Produce the Review

- Report findings in severity order using this priority:
  - `Critical`: bug, regression, security issue, data loss risk, or missing core requirement
  - `Major`: meaningful test gap, design drift, reliability risk, or important maintainability issue
  - `Minor`: small readability, naming, unused, or consistency issue that does not materially affect correctness
- Include the following for each finding:
  - the impact
  - the concrete evidence
  - why it matters in practice
  - whether it is confirmed or inferred when that distinction matters
- Include the following after findings:
  - validation status
  - open questions or assumptions
  - a brief overall verdict: `pass`, `pass with notes`, or `re-review required`

### 8. Re-review After Changes

- Re-check every previously reported `Critical` and `Major` finding after fixes land.
- Confirm whether each finding is resolved, partially resolved, or still open.
- Avoid re-expanding scope unless the fix introduced new behavior worth reviewing.

## Output

MUST produce a concise review with this structure:

1. Findings, ordered by severity, with file references and concrete evidence.
2. Open questions or assumptions, only if they affect confidence in the review.
3. Validation status, including lint, tests, build, commands run, and what was not run.
4. Verdict: `pass`, `pass with notes`, or `re-review required`.

If no findings are discovered, MUST say so explicitly and MUST note any remaining validation gaps or residual risk.

## Error Handling

- If the review target cannot be identified, stop and ask for the minimal missing locator, such as PR number, diff, or file set.
- If the repository state is too incomplete to validate a suspected issue, report it as an unverified risk with the missing evidence.
- If tests or build commands are unavailable, continue with a static review and mark validation as not run.
- If the change is too large for one pass, split the review by subsystem and report the highest-risk areas first.

## Examples

```text
User: Review this auth refresh change.

You:
Critical:
- `refresh_access_token()` writes the new token after replaying queued requests, so concurrent retries can still use stale credentials. This can produce repeated `401` failures under load. Evidence: `src/auth/refresh.py:88`, queue replay starts before `token_store.save()` is called. [confirmed]

Major:
- The new retry path is not covered by a test that exercises two simultaneous `401` responses. The current tests only cover single-request refresh behavior. Evidence: `tests/auth/test_refresh.py`. [confirmed]

Validation:
- Lint: not run
- Tests: not run (reviewed existing tests statically)
- Build: not run

Verdict:
- re-review required
```

```text
User: Review the pagination refactor in list endpoints.

You:
Minor:
- `default_page_size` is defined in both `src/api/config.py:12` and `src/api/pagination.py:5`. The new code reads from `pagination.py`, but two callers in `src/api/users.py` still reference `config.py`. No bug today since both default to 20, but a future change to one will silently diverge. Evidence: `grep -rn default_page_size src/api/`. [confirmed]

Open Questions:
- None.

Validation:
- Lint: pass (`ruff check src/api/`)
- Tests: pass (`pytest tests/api/test_pagination.py`)
- Build: not run

Verdict:
- pass with notes
```
