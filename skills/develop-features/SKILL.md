---
name: develop-features
description: Guide the full feature development lifecycle — from requirements analysis through design, implementation, testing, and documentation.
metadata:
  version: 1.0.0
  author: xbhel
  tags: [development, feature, planning, code generation, testing, documentation]
  aliases: [dev-feature]
---

## Goal

Take `{feature_request}` from raw requirements to a working, tested, and documented implementation by systematically analyzing requirements, designing a solution, implementing code, writing tests, and summarizing the outcome.

## Inputs

| name | description | default | required | source | example |
| ---- | ----------- | ------- | -------- | ------ | ------- |
| feature_request | A description of the feature to develop, including its purpose, expected behavior, and any known constraints. | | Yes | user | Add JWT-based authentication to the REST API. |
| codebase_context | Relevant information about the existing codebase, such as architecture, conventions, key modules, or tech stack. If not provided, it will be derived by exploring the project during workflow step 2. | | No | user or derived | Spring Boot 3, Maven, layered architecture with controller/service/repository. |
| constraints | Any non-functional requirements, time limits, compatibility requirements, or explicit restrictions. | | No | user | Must remain backward-compatible with existing session-based auth. |

## Context

Feature development follows an iterative, confirm-before-code approach:

- Requirements and design are always confirmed with the user before implementation begins.
- Clarifying questions are asked until the feature requirements are unambiguous.
- Implementation, tests, and documentation are produced together as a single deliverable.

## Core Principles

- **Understand before implementing:** Never start coding until requirements are fully clear and the design is confirmed.
- **Follow existing conventions:** Prefer the project's established patterns, naming conventions, and code style over personal preferences.
- **Test alongside code:** Write unit and integration tests as part of implementation — not as an afterthought.
- **Minimal, focused changes:** Implement only what is required by the feature. Avoid refactoring unrelated code.
- **Document decisions:** Record key design choices, trade-offs, and usage instructions so future contributors understand the intent.

## Workflow

1. **Analyze requirements:** Review `{feature_request}` and `{constraints}` to identify:
   - What the feature must do and what it must not do.
   - Expected inputs, outputs, and user-facing behavior.
   - Edge cases and error scenarios.

2. **Analyze the codebase:** Use `{codebase_context}` or explore the project to identify:
   - Relevant modules, classes, functions, and entry points.
   - Existing coding standards, patterns, and guidelines to follow.
   - Integration points where the new feature will connect to existing code.

3. **Clarify requirements (ask-loop):** Ask targeted questions to resolve any ambiguity. Repeat until requirements are fully clear:
   - Propose your current understanding and ask the user to confirm or correct it.
   - Identify and resolve open questions about behavior, edge cases, or constraints.
   - Update the working requirements based on user responses before proceeding.

4. **Design the solution:** Define the architecture and components needed:
   - List the components to create or modify and their responsibilities.
   - Describe how components interact with each other and with the existing codebase.
   - Identify the data structures, algorithms, and APIs involved.

5. **Plan the implementation:** Produce a concrete, trackable plan:
   - Break the implementation into an ordered to-do list of steps.
   - Flag any steps with significant risk or uncertainty.

6. **Confirm with the user:** Present the design and implementation plan for approval:
   - Summarize the proposed solution clearly.
   - Highlight trade-offs or alternatives considered.
   - Incorporate any user feedback and adjust the plan before proceeding.

7. **Implement the feature:** Write clean, maintainable code following project conventions:
   - Execute the implementation plan step by step.
   - Track progress against the to-do list and report completion of each step.

8. **Write tests:** Add unit and integration tests covering:
   - Happy path and core functionality.
   - Edge cases and error scenarios identified in step 1.
   - Integration with existing components.

9. **Review and iterate:** Present the implementation to the user for feedback:
   - Walk through key code sections and test results.
   - Apply requested changes and re-review until the feature is satisfactory.

10. **Document the feature:** Produce concise documentation covering:
    - Usage instructions and examples.
    - Public API or interface description.
    - Key design decisions and trade-offs made during development.

## Output

- Implemented feature code following project conventions.
- Unit and integration tests covering the feature's behavior and edge cases.
- A brief summary including:
  - What was built and how it works.
  - Key design decisions and trade-offs.
  - Usage instructions or API documentation.
  - Any known limitations or follow-up items.

## Error Handling

- If `{feature_request}` is too vague to proceed, ask clarifying questions before doing any analysis or design work.
- If a design conflict or technical blocker arises during implementation, stop and report the issue to the user rather than guessing a resolution.
- If existing code lacks clear conventions, derive a reasonable approach from surrounding code and confirm with the user before applying it broadly.
- If a test cannot be written for a section of code (e.g., due to missing test infrastructure), document the gap and the reason clearly.
