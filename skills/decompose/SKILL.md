---
name: decompose
description: Decompose a requirement, feature, or work item into small, independently executable and verifiable tasks, establish an execution-ready to-do list, and make sequencing and parallelism explicit. Use this whenever the user asks to break work down, plan implementation, create a roadmap, identify dependencies, decide what can run in parallel, track progress, or produce a task graph, even if they do not explicitly ask for a planner.
argument-hint: "requirement, feature, or work item to decompose and plan for execution"
metadata:
  version: 1.4.4
  author: xbhel
  depends-on:
    - analyze
---

# Execution Planner

## Goal

Turn a requirement or work item into an execution-ready plan with small, independently verifiable tasks, explicit dependencies, checkpoints, a trackable to-do list, and a Mermaid task graph.

## When to Use

Use this skill when:

- the user wants a requirement or task split into smaller steps before execution
- the work needs a clear sequence, dependency map, or parallelization plan
- progress must be tracked through a to-do list during execution
- the user asks for a task graph, execution plan, or step-by-step delivery plan

Do not use this skill to replace requirement clarification, design, or implementation. Use it to plan and track that work.

## Context

- Read [references/task-shapes.md](references/task-shapes.md) for task sizing, dependency, and checkpoint rules.
- Read [references/output-template.md](references/output-template.md) for the required output format.

## Core Principles

- MUST keep each task small enough to implement and verify independently.
- MUST assign each task a broad `Type` that reflects its primary task category.
- MUST give each task one clear verification path and at least one checkpoint.
- MUST assign each task to an explicit execution wave such as `W1`, `W2`, or `W3`.
- MUST state whether each task is `parallel` or `sequential`.
- MUST add `depends-on` for every sequential task that relies on another task's output, decision, or stable interface.
- MUST keep the text task list, the trackable to-do list, and the Mermaid graph consistent with each other.
- MUST prefer clarified requirements and confirmed constraints over inference.
- MUST mark uncertainty explicitly when dependencies, owners, or verification paths are inferred rather than confirmed.
- NEVER merge multiple unrelated behaviors into a single task item.
- NEVER label tasks as parallel when they contend on the same file, contract, migration, or unstable shared seam without noting the coordination risk.

## Workflow

### Step 1. Confirm the planning baseline

Resolve the goal, boundary, and granularity from requirements. If the requirement is not ready to decompose safely, use `/analyze` skill first.

### Step 2. Slice the work into candidate tasks

Break the work into the smallest useful units that still have a clear goal and a clear verification path.

For every candidate task:

- assign a stable task ID
- write a short action-oriented title
- assign a meaningful task `Type`
- state the concrete outcome the task produces

If a task cannot be validated independently, split it further.

### Step 3. Resolve sequencing and parallelism

Determine whether each task is independent or depends on others.

- Mark **parallel** if it has no dependency on outputs, decisions, or stable interfaces.
- Mark **sequential** if execution order is required due to dependencies (e.g., artifacts, contracts, migrations, blockers, decisions).
- Assign a **wave ID**; tasks in the same wave execute in parallel.
- Use separate waves for dependent tasks unless a milestone-based grouping is clearer.
- Use `depends-on: Txx` to explicitly define dependencies.
- Group tasks into the same wave only when they share the same stable dependency baseline.


### Step 4. Shape each task for execution

Use the task shapes from [references/task-shapes.md](references/task-shapes.md).

For every task, keep the steps short, include only the minimum actionable work, and add one verification path plus one checkpoint.

### Step 5. Build the tracking artifacts

Prepare these together so they stay aligned:

- execution wave summary
- task list
- checkpoint list
- Mermaid task graph
- trackable to-do list

Build the to-do list with one item per task, sequential IDs, concise titles, and statuses limited to `not-started`, `in-progress`, or `completed`.

### Step 6. Validate the plan before returning it

Before finalizing, verify that:

- every task has a single clear outcome
- every task has a broad but meaningful `Type`
- every task has an independent verification path
- every task belongs to an explicit execution wave
- every sequential task has explicit dependencies
- every task's steps stay lightweight and do not over-specify downstream implementation details
- checkpoints appear after meaningful milestones
- the Mermaid graph matches the task list exactly
- the to-do list is stable enough to track later without renumbering or reinterpretation

## Output

Output the plan using the exact section structure defined in [references/output-template.md](references/output-template.md).

## Error Handling

- If the work is too large for one pass, decompose it into higher-level tasks first, then refine only the next executable slice.
- If dependencies cannot be confirmed from evidence, mark them as inferred and explain the risk.
- If no independent verification path exists for a task, split the task further or mark it as requiring explicit human checkpoint approval.
- Always output the to-do list as plain text that can be tracked later in another tool or workflow.
