## Goal

Define how the execution-planner skill should shape tasks so they are small, independently verifiable, and safe to schedule.

## Task Sizing Rules

A task is small enough only when all of the following are true:

- it produces one primary outcome
- it can be completed without bundling unrelated behavior changes
- it has one clear verification path
- it can be described without the word `and` hiding multiple deliverables

Split the task further when:

- implementation and verification would touch multiple unrelated seams
- the verification path is broad or ambiguous
- the task mixes decision-making with execution
- the task would naturally produce more than one commit-sized change

## Task Categories

Use `Type` for the task's broad category.

Prefer a small, stable set of high-level values. Common values include: `coding`, `infra`, `config`, `data`, `doc`, `design`, `research`, `review`, `release`

## Task Shapes

Use one default task step pattern.

Default structure:

1. prepare or gather the minimal input needed for the task
2. change or produce the target output
3. verify or review the result using one primary validation path
4. checkpoint

Guidance:

- keep the steps outcome-focused rather than encoding a full implementation doctrine
- use the lightest pattern that still makes the task independently actionable and reviewable
- for `coding`, `infra`, `config`, and `data` tasks, verification should usually be a focused command, test, lint run, or observable behavior check
- for `doc`, `design`, `research`, `review`, and `release` tasks, verification should usually be artifact review, checklist completion, sign-off, or explicit human confirmation
- the checkpoint should confirm the task output is stable enough for dependent work to proceed

## Execution Mode Rules

Mark a task as `parallel` only when it does not require:

- another task's code, API, or schema to stabilize first
- a shared decision that is still unresolved
- serialized rollout or migration order
- edits to the same volatile file or module without coordination

Otherwise mark it as `sequential` and add `depends-on`.

Assign every task to an explicit wave such as `W1`, `W2`, or `W3`.

Wave rules:

- tasks in the same wave should be able to start from the same dependency baseline
- tasks in the same wave should usually be parallel with one another
- sequential tasks should usually get their own wave
- if a wave contains only one task, keep the wave anyway so the overall ordering stays obvious

When several tasks can run together, prefer describing them as a parallel wave, for example `W2: T03, T04`.

## Dependency Rules

Use `depends-on` when a task needs:

- a previous design or decision
- a prior interface, fixture, or test seam
- an earlier migration or rollout checkpoint
- a shared utility or contract to exist first

Dependency statements should be concrete:

- Good: `depends-on: T02 because the API contract must be settled first`
- Bad: `depends-on: previous work`

## Checkpoint Rules

Add checkpoints after:

- completion of a task's main verification milestone
- completion of a design or requirement artifact that downstream tasks consume
- completion of a risky integration slice before broader parallel work starts
- completion of a milestone that changes what can run in parallel next

Checkpoint language should confirm a fact, not restate effort:

- Good: `Checkpoint: parser tests pass and the error format matches the existing API contract.`
- Bad: `Checkpoint: parser work done.`

## Verification Rules

Every task must have one primary verification signal.

Prefer, in order:

1. focused automated test or command
2. targeted lint or static check
3. visible behavior or artifact inspection
4. explicit human approval when automation is not realistic
