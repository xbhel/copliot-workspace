---
name: develop-features
description: Drive end-to-end feature development from user requirements through design, implementation, testing, quality review, documentation,and final delivery.
metadata:
  version: 1.0.0
  author: xbhel
---

## Goal

Provide a structured approach to developing new features. Instead of jumping straight into coding, this process emphasizes clarifying user requirements, understanding the codebase, designing the solution, implementing the code, testing, and validating quality—resulting in well-designed features that integrate seamlessly with the existing codebase, meet user needs, and are maintainable in the long term.

## Inputs

|name|description|required|source|
|---|---|---|---|
|requirements|A clear description of the feature, which may include the problem, expected behavior, inputs/outputs, key constraints, and examples.|Yes|user|

## Core Principles

Building new features is not just about writing code. You MUST:

- Ask clarifying questions until the requirements are unambiguous.
- Prefer listing all questions at once instead of asking them one by one.
- Understand the codebase before making changes.
- Design with existing architecture and patterns in mind.
- Confirm the design with the user before implementation.
- Implement only what the feature requires—avoid over-engineering and unrelated changes.
- Prefer test-first development when practical; do not treat tests as a post-implementation task.
- Review the code for quality, readability, and maintainability.

## Workflow

### Phase 1: Clarify Requirements

Ask follow-up questions as needed until the requirements are clear and unambiguous. Clarify the following when relevant:

- **Problem and capability:** identify the problem to solve or the capability to add, including scope, users, and context.
- **Expected behavior and outcome:** clarify the desired behavior, success criteria, and concrete examples when available.
- **Inputs and outputs:** identify required inputs, expected outputs, formats, validation rules, and interfaces when applicable.
- **Constraints and edge cases:** clarify constraints, failure cases, invalid input handling, performance needs, and compatibility concerns when relevant.
- **Examples and usage:** gather example scenarios, use cases, or reference behaviors when they help remove ambiguity.

Example: 

```
User: Implement a Python calculator.

You: To clarify the requirements:
  1. Interface: CLI (interactive or one-off arguments) or GUI?
  2. Operations: Basic math (+, -, *, /) or advanced (powers, roots)?
  3. Error Handling: How to handle division by zero or invalid inputs?
```

Summarize the clarified requirements and **confirm them with the user** before moving on.

### Phase 2: Analyze the Codebase

Analyze the existing codebase to understand relevant code, patterns, and workflows. Focus on the following areas:

- **Structure & Responsibilities:** Identify layout, key services, modules, and utilities. Pinpoint files and components affected by or interacting with the new feature.
- **Architectural Patterns:** Identify the high-level abstraction and design patterns in use (e.g., layered architecture, command-dispatch, plugin system, MVC).
- **Standards & Conventions:** Review coding standards and established conventions (naming, error handling, formatting, etc.)
- **Reference Implementations:** Find and review similar features or components to ensure consistency and reuse opportunities.
- **Integration & Dependencies:** Map integration points, internal APIs, external dependencies, and data flow related to the feature.
- **Testing & Validation:** Locate existing tests (unit, integration, e2e). Understand test stack, lint, conventions, and how to run them, and use them to infer expected behavior and edge cases.
- **Build & Run (as needed):** Check how the project is built, started, and configured locally (scripts, Docker, Make, envs).

Summarize your findings before moving on.

Example output:

```
**Codebase Analysis:**
- **Modules:** `src/cli.py` (entry), `src/operations/` (logic target), `src/utils/parser.py` (shared).
- **Patterns:** Command-dispatch.
- **Conventions:** Pure functions, type hints, docstrings. Errors raise `ValueError`.
- **Reference:** Adapt `src/operations/converter.py` pattern.
- **Testing:** `pytest` in `tests/`, covering valid/invalid paths. Run via `uv run pytest`.
```

### Phase 3: Validate & Refine Requirements

Validate the clarified requirements against the codebase findings, resolving any remaining uncertainties. Use the codebase analysis first, and ask targeted follow-up questions only for decisions or behaviors that are still unclear. Follow these steps:

1. **Validate Against Codebase:** Ensure requirements align with existing modules, architecture, and patterns.
2. **Identify Gaps & Constraints:** Detect missing capabilities, limitations, or conflicts with the current implementation.
3. **Clarify Edge Cases:** Refine edge cases and expected behaviors based on system constraints and existing implementations.
4. **Surface Assumptions & Risks:** Highlight implicit assumptions, potential risks, and trade-offs.
5. **Open Questions:** List any unresolved questions or decisions that need input from stakeholders.
6. **Suggest Alternative Approaches (if needed):** Propose simpler or better-aligned approaches when the current direction is too complex or misaligned.
7. **Consolidate and Confirm:** List all items needing user feedback (open questions, assumptions, trade-offs, or alternative approaches) and wait for answers.

Example output for feedback:

```
**Pending Clarifications:**
1. **Parser:** `src/utils/parser.py` only accepts spaced input like `2 + 2`. Should we add support for `2+2`, or keep the current rule?
2. **Division by Zero:** Should the CLI catch `ValueError` and show a friendly message?
```

After completing this phase, the requirements should be fully clarified and enriched with codebase insights, ready for design and implementation. 

Before proceeding, MUST confirm the refined requirements with the user, including relevant codebase context such as files, test stack, patterns, and other helpful insights.

Example output for refined requirements:

```
**Refined Requirements:**
- **Scope:** Add `+`, `-`, `*`, `/` operations in `src/operations/`, following the `converter.py` pattern.
- **Constraints:** Keep spaced input only. No `parser.py` changes. (Confirmed)
- **Edge Cases:** Raise `ValueError` for division by zero and handle it in the CLI.
- **Testing:** Add tests for valid operations and division-by-zero behavior using `pytest`.
```

### Phase 4: Design the Solution

Design the solution based on the refined requirements and codebase context, focusing on these aspects:

- **Architecture & Components:** Define the high-level architecture, key components, design patterns, abstractions.
- **Data Flow & Interfaces:** Map data flow, inputs/outputs, and interfaces, indicating related functions or files.
- **Error Handling & Edge Cases:** Design handling of errors and edge cases.
- **Testing Strategy:** Plan how to test the feature, including unit, integration, and edge cases.
- **Validation Strategy:** Define how to validate the feature against requirements, including success criteria and metrics.
- **Documentation Plan:** Outline required documentation (code comments, user guides, API docs).
- **Review & Feedback:** Plan design-level reviews, feedback loops, and iterative improvements.

**Design Multiple Approaches**

Consider alternatives with different focuses:

- Minimal Changes: Smallest changes with maximum reuse.
- Clean Architecture: Prioritize maintainability and elegant abstractions.
- Pragmatic Balance: Balance speed and quality.

You MUST:

- Review all approaches and evaluate trade-offs
- Form an opinion on which approach best fits this task
- Present a comparison with recommendations
- **Confirm the chosen approach with the user** before implementation

Example output:

```
**Design Options:**

**A. Minimal Changes**
- Add `src/operations/math.py` with `add`, `subtract`, `multiply`, `divide`.
- Add a `calc` subcommand in `src/cli.py`.
- *Pros:* Small change, matches current patterns.
- *Cons:* Harder to extend for advanced math.

**B. Clean Architecture**
- Replace parser logic with AST-based parsing.
- Add a calculator service or plugin layer.
- *Pros:* Easier to extend later.
- *Cons:* Too much change for current scope.

**C. Pragmatic Balance (Recommended)**
- Add `src/operations/math.py` now.
- Keep the current parser, but isolate command handling so later parser changes stay local.
- *Pros:* Good balance of speed, clarity, and future flexibility.
- *Cons:* Slightly more setup than the minimal approach.

*Recommendation:* Approach C. Proceed?
```

### Phase 5: Plan the Implementation

After the user confirms the chosen approach, create a TDD-first to-do list for execution and tracking. Make each step map to a clear behavior and a concrete code change, and keep it small enough to implement and validate independently.

Example output:

```
**Implementation Plan for Approach C:**
1. Add failing tests for math operations and division-by-zero behavior.
2. Implement `src/operations/math.py` until those tests pass.
3. Add a failing CLI test for the `calc` command flow and error handling.
4. Update `src/cli.py` until the CLI tests pass.
5. Refactor the touched code, then update docs and usage examples.

**Checkpoints:**
- After step 2, run the math tests and verify they pass.
- After step 4, run the CLI tests and verify the command flow matches existing patterns.
```

### Phase 6: Implementation

Implement the feature according to the design, You MUST:

- Follow the design, chosen approach, and implementation steps
- Apply the relevant context and patterns identified in Phases 2 and 3
- Write or update tests first when practical, then implement until the tests pass
- Write clean, maintainable code that follows existing standards and conventions
- Keep tests focused on the required behavior and edge cases, and refactor after the test suite is green
- Document the code with clear, accurate, and concise doc-strings and inline comments.

### Phase 7: Quality Review & Iteration

After implementation, review the code for quality, readability, and maintainability. You MUST:

- Review only the changes related to the feature unless the user clearly requests a broader review.
- Ensure the code meets the requirements and design
- Check for adherence to coding standards and conventions
- Verify that tests are comprehensive and passing
- Verify that lints and checks are passing
- Review documentation for clarity and completeness

Iterate in a `test → implement → refactor → review` loop until all issues are resolved and the feature meets requirements and quality standards.

#### Out-of-Scope Issues

Report any potential issues outside the current implementation **only if confidence is ≥ 80**, and ask for clarification if needed. Focus on issues that truly matter: quality over quantity.

**Confidence Scoring**

Rate each potential issue on a scale from 0-100:

- **0:** Not confident at all. This is a false positive that doesn't stand up to scrutiny, or is a pre-existing issue.
- **25:** Somewhat confident. This might be a real issue, but may also be a false positive. If stylistic, it wasn't explicitly called out in project guidelines.
- **50:** Moderately confident. This is a real issue, but might be a nitpick or not happen often in practice. Not very important relative to the rest of the changes.
- **75:** Highly confident. Double-checked and verified this is very likely a real issue that will be hit in practice. The existing approach is insufficient. Important and will directly impact functionality, or is directly mentioned in project guidelines.
- **100:** Absolutely certain. Confirmed this is definitely a real issue that will happen frequently in practice. The evidence directly confirms this.

Example output:

```
**Quality Review:**
- Requirements: Met.
- Tests: Passed (`pytest`).
- Lint: Passed (`ruff`).

**Out-of-Scope Issues:**
- **Confidence 85:** The CLI still shows raw stack traces for unhandled `ValueError`.
  *Suggestion:* Add a friendly top-level error message. Should I include that change?
```

### Phase 8: Documentation

Document what was built, how it works, how to use it, including:

- A short feature overview and expected behavior
- Key design decisions and trade-offs
- Changed files and components
- Usage instructions and examples
- Public API or interface
- Any relevant context for future maintainers or users
- Suggested next steps or improvements

Example output:

```
**Feature Complete:** Calculator CLI

**What was built:**
- Math operations for `+`, `-`, `*`, `/`
- A `calc` command integrated into the existing CLI flow
- Division-by-zero handling with a user-friendly error path

**Key decisions:**
- Kept the existing parser unchanged
- Used a small math module instead of a larger calculator abstraction
- Isolated command handling so future parser changes stay local

**Files modified:**
- `src/operations/math.py`
- `src/cli.py`
- `tests/test_math.py`

**Usage / Interface:**
- `calc "10 / 2"` returns `5`
- Supported operators: `+`, `-`, `*`, `/`

**Maintainer notes:**
- Add new operators in `src/operations/math.py`
- Keep CLI parsing and user-facing error handling in `src/cli.py`

**Suggested next steps:**
- Add more CLI input validation
- Add more operator coverage if scope expands
- Update README examples if CLI behavior changes
```

## Output

A clear and concise final delivery summary including:

- Feature outcome and current status.
- What was built and how it works.
- Key design decisions and trade-offs.
- Changed files and components.
- Tests, validation, and quality check results.
- Reported issues, risks, or follow-up items.
- Documentation completed.

## Error Handling

- **Long tasks:** If a task takes too long, split it into subagents to run steps in parallel, then combine results. Common in code analysis or design phases.
- **Missing tools:** If required tools or dependencies are missing during implementation, stop, report with context, and request support.
- **Implementation blockers:** If a conflict or technical blocker arises during implementation, stop, report with context, and request guidance.
