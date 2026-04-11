---
name: code-simplifier
description: Simplify and refine existing code for clarity, consistency, and maintainability without changing behavior. Use whenever the user asks to simplify, clean up, refactor for readability, reduce nesting or duplication, remove dead code, polish a recent change, or make code easier to review or maintain, especially in the code they just edited, even if they do not explicitly ask for refactoring.
---

## Goal

Make existing code easier to read, review, and maintain while preserving exact behavior.

## When to Use

Use this skill when the user wants to simplify or clean up existing code, especially when they ask to:

- reduce complexity or nesting
- remove duplication or dead code
- improve readability, naming, or structure
- make recent changes easier to review and maintain

Default to the recently modified or directly relevant code unless the user asks for a broader refactor.

## Core Principles

### Preserve behavior

- Never change what the code does—only how it is expressed. 
- All original features, inputs, outputs, side effects, and behaviors must remain intact.
- If a simplification might change behavior, do not make it.

### Follow local conventions

- Match the surrounding codebase style, naming, abstractions, and architecture.
- Prefer consistency with nearby code over introducing a new pattern.

### Optimize for clarity

- Prefer readable, explicit code over clever or compact code.
- Replacing overly complex expressions with clearer structures
- Using clear, descriptive naming for variables and functions
- Grouping related logic together
- Reduce cognitive load, not just line count.
- Keep control flow and data flow easy to follow.
- Do not trade readability for micro-optimizations.

### Keep scope tight

- Start with the changed diff or directly relevant code before considering broader cleanup.
- Refactor only the code that is relevant to the request.
- Do not clean up unrelated areas unless explicitly asked.
- Do not rewrite tests unless the user asks or the simplification directly requires a test adjustment.
- Do not touch config, build, or infrastructure files unless they are directly relevant to the requested simplification.

## Simplification Heuristics

- Flatten avoidable nesting with guard clauses or early returns.
- Remove redundant logic, dead code, unused variables, and repeated comments.
- Remove unused imports when they are part of the touched code.
- Replace dense expressions with clearer intermediate steps when that improves readability.
- Inline trivial abstractions that add indirection without value.
- Extract a helper only when it gives repeated logic or a clear single responsibility a better home.
- Avoid renames unless they materially improve clarity and are clearly behavior-safe.
- Keep comments minimal and only when they explain non-obvious intent or decisions.
- Keep error handling direct, visible, and consistent with local patterns.
- Avoid refactors that save lines but make debugging or extension harder.

## Workflow

1. Identify the changed diff or directly relevant code.
2. Find the main sources of complexity, duplication, or confusion.
3. Apply the smallest useful refactor that improves clarity.
4. Re-check that behavior, interfaces, and touched-file scope remain unchanged.
5. Summarize only the simplifications that materially improve understanding.

## Output

- Produce code that is simpler, clearer, and easier to maintain.
- Keep explanations brief and focused on meaningful changes.
- Call out any behavior-sensitive assumption if complete certainty is not possible.