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
- Understand the codebase before making changes.
- Design with existing architecture and patterns in mind.
- Confirm the design with the user before implementation.
- Implement only what the feature requires—avoid over-engineering and unrelated changes.
- Write tests alongside your code, not as an afterthought.
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

You: I need a few details to make sure I build the right calculator:
  1. Interface and interaction: Should this be a command-line tool (CLI) or a GUI? 
    - If CLI, should it be interactive (like a prompt) or run once with an input (e.g., `python calc.py "2 + 2"`)?
  2. Supported operation: What operations should it support?
    - Just basic math (+, -, *, /) or also things like powers, square roots, etc.?
  3. Error handling and edge cases: How should it handle cases like division by zero or invalid input?
  ...
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
Here's what I found after analyzing the codebase:

1. Relevant modules and files:
   - `src/operations/` for math modules, `src/cli.py` as entry point, `src/utils/parser.py` for shared parsing.
   - New calculator logic fits in `src/operations/`.
2. Architectural patterns:
   - Command-dispatch: CLI parses input → dispatches to an operation module → returns formatted output.
3. Coding standards and conventions:
   - Pure functions with type hints and docstrings; errors raised as `ValueError`.
4. Reference implementations:
   - `src/operations/converter.py` — similar parse-dispatch-return pattern; can adapt for calculator.
5. Integration points and dependencies:
   - Register a new subcommand in `src/cli.py`; reuse `tokenize()` from `src/utils/parser.py`.
6. Testing setup and coverage:
   - `tests/` with `pytest`, one `test_<module>.py` per module, parametrized cases covering 
     valid/invalid inputs and boundary values.
7. Build and run:
   - `uv run python -m src.cli` to run; `uv run pytest` to test.
   ...
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

After completing this phase, the requirements should be fully clarified and enriched with codebase insights, ready for design and implementation. 

Before proceeding, MUST confirm the refined requirements with the user, including relevant codebase context such as files, test stack, patterns, and other insights.

### Phase 4: Design the Solution

Design the solution based on the refined requirements and codebase context, focusing on these aspects:

- **Architecture & Components:** Define the high-level architecture, key components, design patterns, abstractions.
- **Data Flow & Interfaces:** Map data flow, inputs/outputs, and interfaces, indicating related functions or files.
- **Error Handling & Edge Cases:** Design handling of errors and edge cases.
- **Implementation Steps:** Break the design into an to-do list for execution and tracking. Each item should be small enough to implement and validate independently.
- **Testing Strategy:** Plan how to test the feature, including unit, integration, and edge cases.
- **Validation Strategy:** Define how to validate the feature against requirements, including success criteria and metrics.
- **Documentation Plan:** Outline required documentation (code comments, user guides, API docs) and assign responsibility.
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
- Confirm the chosen approach with the user before implementation

## Phase 5: Implementation

Implement the feature according to the design, You MUST:

- Follow the design, chosen approach, and implementation steps
- Apply the relevant context and patterns identified in Phases 2 and 3
- Write clean, maintainable code that follows existing standards and conventions
- Implement tests alongside the code, covering relevant cases and edge cases
- Document the code and any necessary user-facing documentation.

## Phase 6: Quality Review & Iteration

After implementation, review the code for quality, readability, and maintainability. You MUST:

- Review only the changes related to the feature unless the user clearly requests a broader review.
- Ensure the code meets the requirements and design
- Check for adherence to coding standards and conventions
- Verify that tests are comprehensive and passing
- Verify that lints and checks are passing
- Review documentation for clarity and completeness

If issues are found, iterate on the implementation until they are resolved and the feature is ready for delivery. Follow an `implement and test -> review` loop until the feature meets the requirements and quality bar.

#### Out-of-Scope Issues

Report any potential issues outside the current implementation **only if confidence is ≥ 80**, and ask for clarification if needed. Focus on issues that truly matter: quality over quantity.

**Confidence Scoring**

Rate each potential issue on a scale from 0-100:

- **0:** Not confident at all. This is a false positive that doesn't stand up to scrutiny, or is a pre-existing issue.
- **25:** Somewhat confident. This might be a real issue, but may also be a false positive. If stylistic, it wasn't explicitly called out in project guidelines.
- **50:** Moderately confident. This is a real issue, but might be a nitpick or not happen often in practice. Not very important relative to the rest of the changes.
- **75:** Highly confident. Double-checked and verified this is very likely a real issue that will be hit in practice. The existing approach is insufficient. Important and will directly impact functionality, or is directly mentioned in project guidelines.
- **100:** Absolutely certain. Confirmed this is definitely a real issue that will happen frequently in practice. The evidence directly confirms this.
