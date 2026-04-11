---
name: requirement-analysis
description: Analyze the user’s requirements, clarify ambiguities, validate them against the codebase, and produce a refined specification ready for design and implementation. Use this skill before design or implementation when requirements are incomplete, ambiguous, or need codebase validation.
metadata:
  version: 1.0.0
  author: xbhel
  depends-on: 
    - code-analysis
---

# Requirement Analysis

## Goal

Turn raw, incomplete, or ambiguous requirements into a refined, codebase-informed specification that is clear, evidence-based, and ready for design and implementation.

## When to Use

Use this skill when:

- a feature, bug, or change request is incomplete or ambiguous
- requirements must be clarified or validated before design or implementation
- you need a codebase-informed specification that is ready to hand off for design or implementation

## Inputs

| name | description | required | source |
|---|---|---|---|
| requirements | The user's description of the feature, change, or problem to solve. It may be incomplete, unclear, or ambiguous. | Yes | user or upstream |

## Core Principles

- MUST ask clarifying questions until the requirements are unambiguous.
- ALWAYS batch clarifying questions into a single prompt; never ask one at a time.
- MUST use codebase evidence to resolve ambiguities before escalating to the user.
- MUST produce a requirements specification, not an architecture proposal.
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

Use the `code-analysis` skill to explore only the codebase areas affected by the clarified requirements and gather relevant evidence. Keep the analysis targeted; avoid broad or exhaustive reviews. Launch 2–3 `code-analysis` agents in parallel, each focusing on a different aspect (e.g., similar features, architecture, UI patterns).

### Phase 3: Validate and Refine Requirements

Cross-reference the clarified requirements against the codebase analysis. Use code evidence first, and ask follow-up questions only when the evidence is insufficient.

Follow these steps:

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

After this phase, the requirements should be fully clarified, evidence-backed, and grounded in the relevant codebase context, ready for design and implementation.

### Phase 4: Produce Specification

Produce the final refined requirements as a requirements specification, not an architecture proposal. Consolidate the clarified requirements, validation results, and codebase findings from the previous phases into one structured output, including:

1. Problem, scope, and confirmed goals.
2. Confirmed behavior and acceptance criteria.
3. Inputs, outputs, rules, validation, and interface expectations.
4. Constraints and non-functional requirements.
5. Edge cases and failure modes.
6. Relevant codebase findings that shape the requirements, including modules, files, interfaces, patterns, dependencies, tests, and workflows.
7. Affected surfaces, dependencies, and compatibility considerations.
8. Assumptions, risks, trade-offs, and any remaining open questions.

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
- Open questions: none.
```

## Output

A structured requirements specification covering the clarified requirements, relevant codebase evidence, validation results, and any remaining decisions needed before design.

## Error Handling

- **Long tasks:** If a task takes too long, split it into subagents to run steps in parallel, then combine results. Common in codebase analysis.
