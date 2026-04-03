---
name: requirement-analysis
description: Analyze the user’s requirements, clarify ambiguities, validate them against the codebase, and produce a refined specification ready for design and implementation.
metadata:
  version: 1.0.0
  author: xbhel
---

# Requirement Analysis

## Goal

Turn raw, incomplete, or ambiguous requirements into a refined, codebase-informed specification that is ready for design and implementation.

## When to Use

Use this skill when:

- a feature, bug, or change request is incomplete or ambiguous
- requirements need clarification or validation before design or implementation
- alignment with the existing codebase (architecture, patterns, constraints) is required
- you need to produce a specification ready for design and implementation

## Inputs

| name | description | required | source |
|---|---|---|---|
| requirements | The user's description of the feature, change, or problem to solve. It may be incomplete, unclear, or ambiguous. | Yes | user or upstream |

## Core Principles

- MUST ask clarifying questions until the requirements are unambiguous.
- ALWAYS batch clarifying questions into a single prompt; never ask one at a time.
- MUST use codebase evidence to resolve ambiguities before escalating to the user.
- MUST surface assumptions and risks explicitly; do not absorb them silently.

## Workflow

### Phase 1: Clarify Requirements

Ask follow-up questions as needed until the requirements are clear and unambiguous. Infer what you can, and clarify only what is genuinely unclear or affects implementation. Cover these areas when relevant:

- **Problem and scope:** the problem to solve, affected users, context, and what is in or out of scope.
- **Expected behavior:** desired behavior, success criteria, and concrete examples when helpful.
- **Inputs and outputs:** required inputs, expected outputs, formats, validation rules, and interface or contract details.
- **Constraints:** performance, compatibility, security, policy requirements.
- **Edge cases and failure modes:** invalid inputs, boundary conditions, graceful degradation.
- **Examples and usage:** representative scenarios, use cases, or reference behavior when they help remove ambiguity.

Example:

```text
User: Implement a Python calculator.

You: Before proceeding, I have a few clarifying questions:
  1. Should this be a CLI tool or a GUI application?
  2. Which operations should it support: basic math (+, -, *, /) only, or also powers and roots?
  3. How should it handle division by zero and invalid input?
```

Once the requirements are clarified, summarize them concisely and **confirm the summary with the user** before moving on.

### Phase 2: Analyze the Codebase

Invoke the `/code-analysis` to analyze code relevant to the requirements, including existing patterns and workflows. Use the findings to identify:

- relevant modules, files, and interfaces
- required conventions and patterns
- affected integration points
- gaps in existing tests or behavior
- similar features or components to guide consistency and reuse

Example:

```text
You: To implement the calculator, I analyzed the codebase and found:

- **Modules:** `src/cli.py` (entry), `src/operations/` (logic target), `src/utils/parser.py` (shared)
- **Patterns:** command dispatch
- **Conventions:** pure functions, type hints, docstrings; errors raise `ValueError`
- **Reference:** adapt the pattern used in `src/operations/converter.py`
- **Testing:** `pytest` in `tests/`, covering valid and invalid paths; run with `uv run pytest`
```

### Phase 3: Validate and Refine Requirements

Cross-reference the requirements against the codebase analysis. Use code evidence first, and ask follow-up questions only when the evidence is insufficient.

1. Validate alignment with the existing architecture, data flow, and ownership boundaries.
2. Identify gaps, conflicts, and missing behaviors.
3. Refine edge cases and failure modes based on system constraints.
4. Surface assumptions, risks, and any remaining open questions.
5. Propose simpler, better-aligned alternatives when requirements conflict with the codebase or the approach is overly complex.
6. Consolidate the refined spec, list all items needing user feedback, including open questions, assumptions, trade-offs, and alternative approaches, and wait for the user’s answers before proceeding.

Example:

```text
You: Pending Clarifications:
1. Parser: `src/utils/parser.py` only handles space-separated tokens. Should `2+2` be supported, or rejected with a clear error?
2. Division by zero: should it be handled and shown as a user-facing error, or allowed to propagate as an exception?

User:
1. Yes, support compact expressions like `2+2`.
2. Handle division by zero and show a clear user-facing error message.
```

After this phase, the requirements should be fully clarified and grounded in codebase context, ready for design and implementation.

### Phase 4: Output

Produce the final refined requirements as an implementation-ready specification. Consolidate all clarified requirements, validation results, and codebase insights from the previous phases into a single structured output.

Include, when relevant:

1. Problem, scope, and confirmed goals.
2. Confirmed behavior and success criteria
3. Inputs, outputs, and interface or contract details
4. Constraints and non-functional requirements
5. Edge cases and failure modes
6. Relevant codebase context, including modules, files, interfaces, patterns, and workflows
7. Affected integration points
8. Assumptions, risks, and trade-offs

Ensure the output is well organized, internally consistent, and detailed enough to be used directly for design and implementation.

Example output:

```text
Problem, scope, and confirmed goals:
- Add a calculator feature to the CLI for basic arithmetic operations.
- Keep the change within the existing CLI workflow.
- Do not add a GUI or advanced math functions.

Confirmed behavior and success criteria:
- Support addition, subtraction, multiplication, and division.
- Support compact expressions like `2+2`.
- Return correct results for valid expressions.
- Show clear user-facing error messages for invalid input and division by zero.

Inputs, outputs, and interface or contract details:
- Input: CLI arguments or interactive text input.
- Output: computed result or user-facing error message.

Constraints and non-functional requirements:
- Must reuse the existing CLI entry point.
- Must follow current error-handling conventions.

Edge cases and failure modes:
- Division by zero should be handled and shown as a user-facing error.
- Invalid expressions should return clear error messages.
- Missing operands should return clear error messages.

Relevant codebase context:
- `src/cli.py`: CLI entry
- `src/utils/parser.py`: input parsing
- `src/operations/`: operation implementations
- Existing pattern: command dispatch with pure helper functions

Affected integration points:
- CLI argument parsing
- operation dispatch
- test coverage in `tests/`

Assumptions, risks, and trade-offs:
- Supporting compact expressions like `2+2` may require parser changes and could affect existing parsing behavior.
- Favor clear user-facing error messages over exposing raw exceptions.
```

## Output

A structured, implementation-ready specification covering all clarified requirements, codebase context, and validation results.

## Error Handling

- **Long tasks:** If a task takes too long, split it into subagents to run steps in parallel, then combine results. Common in codebase analysis.
