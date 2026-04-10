---
name: architecture-design
description: Design a clear, extensible, and maintainable architecture proposal with explicit boundaries, responsibilities, integration points, and scalability considerations. Use this skill when a change requires architectural decisions, boundary definition, or integration design before implementation.
metadata:
  version: 1.0.1
  author: xbhel
---

# Architecture Design

## Goal

Turn requirements into one concrete, implementation-ready architecture proposal grounded in the available context, with clear structure, ownership boundaries, integration points, and validation considerations.

## When to Use

- The change needs architectural decisions, boundary definitions, or integration design before implementation.
- Responsibilities, ownership, contracts, workflows, or interaction patterns require explicit design choices.

## Core Principles

- MUST understand requirements and relevant context deeply before designing.
- MUST design with the existing architecture, environment, and constraints in mind when they exist.
- MUST prefer reuse of existing components, seams, and conventions before introducing new abstractions.
- MUST ground every design decision in requirements, constraints, or available context evidence.
- MUST define scope before proposing abstractions.
- MUST keep the design proportional to the change.
- MUST make ownership boundaries, contracts, and integration points explicit.
- MUST define where validation, orchestration, state changes, and side effects happen.
- MUST state assumptions, trade-offs, and unresolved decisions explicitly.
- MUST identify conflicting existing patterns or constraints explicitly when present.
- MUST recommend the least risky path when patterns or constraints conflict.
- MUST say directly when the requested architecture is over-engineered for its scope.
- MUST propose a smaller design when the requested architecture is too heavy for the change.
- NEVER invent components or services without a clear responsibility and integration need.
- NEVER silently absorb unresolved product or technical decisions.

## Workflow

### 1. Validate Readiness

- Confirm requirements are sufficiently clear for architectural design.
- Confirm the available context is enough to anchor the proposal.
- List any missing information that would materially affect the design.

### 2. Define Scope and Boundaries

- Define in-scope and out-of-scope work.
- Identify affected components, modules, services, layers, workflows, and external systems.
- Mark stable boundaries that should not change.
- Mark interfaces or contracts that may change and the cost of changing them.
- Capture relevant runtime, deployment, performance, security, and ownership constraints.

### 3. Design the Architecture

- Define the high-level architecture and major abstractions.
- Select the design patterns that fit the context and explain why.
- Define components, services, modules, handlers, adapters, and APIs to add or change.
- Map integration points with existing components, code, storage, events, config, and external systems.
- Define interfaces and contracts between participating parts.
- Trace the data flow and execution path from entry to completion.
- Describe interaction and ownership handoffs where coordination matters.

### 4. Stress the Design

- Identify edge cases: invalid input, missing state, duplicates, ordering, retries, idempotency, concurrency, and partial failure.
- Define error handling at each important boundary.
- Identify operational, performance, maintainability, and migration risks.
- Compare alternatives only when a meaningful design choice exists.

### 5. Define Verification and Delivery

1. Define validation steps and success criteria.
2. Produce a workflow diagram that matches the written design.

## Output

**IMPORTANT:** Every output item below MUST be rendered as its own distinct section in the final response.

Produce one architecture proposal. Every section MUST be concrete and context-specific. Name actual modules, files, APIs, boundaries, systems, or constraints when known. Write decisions, not generic advice.

- **Scope:** Problem being solved, in-scope work, out-of-scope work, and affected boundaries.
- **Architecture**: Recommended structure, major responsibilities, ownership boundaries, and rationale.
- **Design Patterns:** Patterns used or introduced, why they fit, and their trade-offs.
- **Components:** Functions, files, components, modules, services, handlers, or adapters to add or change, with their responsibilities.
- **Interfaces and Contracts:** Input/output schemas, validation rules, invariants, and contracts for functions, classes, APIs, events, or messages exchanged between components.
- **Integration Points:** Affected code paths, services, storage, events, config, or external systems; reuse opportunities; compatibility concerns.
- **Data Flow:** Execution path from entry to completion, including validation, orchestration, side effects, async work, retries, and decision points.
- **Interaction:** Important interaction sequences, coordination points, and ownership handoffs.
- **Edge Cases and Error Handling:** Invalid input, missing state, duplicate requests, concurrency or ordering issues, backward-compatibility concerns, and boundary-specific error handling.
- **Risks and Trade-offs:** Key technical risks, complexity costs, migration concerns, and notable trade-offs.
- **Validation Approach:** How to confirm the architecture is correct, complete, and safe to implement.
- **Architecture Diagram:** Provide a Mermaid diagram that MUST match the written architecture. Adapt the structure to the actual design; do not reuse a default flow when it does not fit.

  Example skeleton only:

  ```mermaid
  flowchart TD
      A[Entry Point] --> B[Validation]
      B --> C[Orchestration]
      C --> D[Domain Logic]
      D --> E[Persistence or Side Effect]
      E --> F[Response or Event]
      C --> G[Error Path]
  ```