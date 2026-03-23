---
name: develop-features
description: Drive end-to-end feature development from user requirements through design, implementation, testing, quality review, and final documentation.
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

Summarize the clarified requirements and **confirm them with the user** before moving on.
