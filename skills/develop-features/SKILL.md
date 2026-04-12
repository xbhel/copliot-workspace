---
name: develop-features
description: Orchestrate end-to-end feature delivery by composing requirement analysis, architecture design, execution planning, TDD implementation, code review, and final handoff. Use this skill when delivering a non-trivial feature from raw request through validated completion.
metadata:
  version: 1.1.1
  author: xbhel
  depends-on:
    - requirement-analysis
    - architecture-design
    - execution-planner
    - test-driven-development
    - code-review
---

# Develop Features

## Goal

Provide a structured approach to developing new features. Instead of jumping straight into coding, this process emphasizes clarifying user requirements, understanding the codebase, designing the solution, implementing the code, testing, and validating quality, resulting in well-designed features that integrate seamlessly with the existing codebase, meet user needs, and are maintainable in the long term.

## When to Use

Use this skill when:

- the goal is to deliver a non-trivial feature end to end, from raw or partially defined requirements through implementation, validation, and final handoff
- the work requires requirement refinement, solution design, execution planning, TDD implementation, and quality review to stay in one coordinated workflow
- the task benefits from explicit user checkpoints between requirements, design, implementation, and review instead of jumping straight into a single edit

Do not use this skill when a single specialist skill is sufficient for the task.

## Inputs

| name | description | required | source |
| --- | --- | --- | --- |
| requirements | The user's description of the feature, change, or problem to solve. It may be incomplete, unclear, or ambiguous. | Yes | user |

## Context

- This skill is an orchestrator. Delegate each phase to the appropriate specialist skill instead of repeating that skill's full workflow here.
- Outputs from earlier phases become required inputs for later phases.
- Keep the workflow proportional to the change. If a single specialized skill is enough, say so directly.

## Core Principles

- MUST clarify and confirm requirements before design, and confirm the chosen design before implementation.
- MUST ground design and implementation in the existing codebase, patterns, constraints, and confirmed requirements.
- MUST create a TDD-first implementation plan before coding begins.
- MUST implement in small validated slices, using parallel implementation agents only for independent items that do not contend on the same unstable seam.
- MUST review the code for quality, readability, and maintainability.
- MUST keep the scope tight to the approved feature and carry forward confirmed assumptions, risks, and constraints across phases.
- NEVER silently absorb unresolved decisions that materially affect design or implementation.
- NEVER restate an entire delegated skill inline when a concise handoff to that skill is enough.

## Workflow

### Phase 1: Clarify Requirements

Use `/requirement-analysis` to clarify, validate, and refine the requirements until they are ready for design.

Before moving forward:

- resolve or explicitly carry forward any open questions
- confirm the refined requirements with the user
- capture the affected files, patterns, tests, and constraints that later phases must respect

### Phase 2: Design the Solution

Once the refined requirements are confirmed, use `/architecture-design` to produce the implementation-ready design.

Launch three parallel design subagents with different focuses:

- Minimal Changes: minimal changes, maximum reuse, lowest migration cost
- Clean Architecture: clean boundaries, maintainability, and stronger architecture
- Pragmatic Balance: pragmatic balance between delivery speed, safety, and future flexibility

Then compare the three approaches, evaluate the trade-offs, recommend one option, and confirm the chosen approach with the user before implementation.

### Phase 3: Plan the Implementation

After the design is approved, use `/execution-planner` to convert the confirmed scope into an execution-ready plan.

The plan should stay TDD-first and include the execution slices, dependencies, checkpoints, trackable to-do list, and task graph needed to drive implementation safely.

### Phase 4: Implement with TDD

Execute the plan through `/test-driven-development`, following its failing-test-first workflow for each implementation slice.

When Phase 3 marks items as parallel, run multiple implementation subagents in parallel, one per independent item or small cluster within the same wave.

During implementation, you MUST:

- assign each subagent a stable slice boundary from the approved plan
- keep parallel subagents off the same unstable file, contract, migration, or shared seam unless the plan explicitly calls for coordination
- require each subagent to complete its own red-green-refactor loop before merging results
- synchronize at the end of each wave, resolve conflicts, and run shared validation before starting the next dependent wave
- keep execution aligned with the approved requirements, design, plan, and existing patterns
- run broader validation at meaningful checkpoints, not only the most recent test
- update code comments or docs only when they clarify non-obvious behavior

### Phase 5: Quality Review and Iteration

When the implementation is functionally complete, use `/code-review` on the resulting change set.

Scope the review to:

- the implemented diff
- the confirmed requirements
- the approved design constraints
- the expected tests, lint checks, and validation steps

Treat `Critical` and `Major` review findings as blocking.

If review findings require changes, return to the TDD loop for the affected slice, re-run the relevant validation, and repeat review until the blocking findings are resolved.

Report out-of-scope issues only when confidence is high enough that they materially matter.

After the review loop is complete, produce the final delivery summary using the output structure below.

## Output

A structured final delivery summary that synthesizes the outputs of the delegated skills and includes:

- current status of the feature
- refined requirements baseline
- approved design summary
- implementation outcome and changed surfaces
- validation results, including tests, lint, and review verdict
- remaining risks, follow-up items, or open decisions
- documentation and usage notes relevant to users or maintainers

## Error Handling

- Stop before design when requirement-critical questions remain unresolved.
- Present the lower-risk option and wait for approval when the design conflicts with the codebase or is over-engineered for the task.
- Refine or rescope the plan before coding when `execution-planner` cannot produce independently verifiable tasks.
- Create the smallest safe test seam first, or get explicit approval, when `test-driven-development` cannot start cleanly.
- Reslice the work or serialize that seam when parallel implementation slices begin to conflict.
- Do not present the feature as complete while blocking `code-review` findings remain unresolved, unless the user explicitly accepts them.
- Split long-running delegated phases into subagents where appropriate, then recombine their outputs before continuing.
