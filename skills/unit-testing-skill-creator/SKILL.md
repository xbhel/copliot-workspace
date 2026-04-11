---
name: unit-testing-skill-creator
description: Create or refine reusable unit-testing skills for a specific language, framework, or repository convention using the layered template in this skill. Use this whenever the user wants to create, adapt, standardize, templatize, or port a testing skill across stacks such as unittest, pytest, JUnit, Mockito, Jest, Vitest, coverage tooling, or project-specific test workflows, even if they only describe the conventions and do not explicitly ask for a skill.
metadata:
  version: 1.1.0
  author: xbhel
  depends-on:
    - code-analysis
---

# Unit Testing Skill Creator

## Goal

Create or refine a complete, reusable unit-testing skill that tells an agent how to add, run, fix, and report on unit tests for a specific language, stack, and project convention.

## When to Use

Use this skill when:

- the user wants a reusable testing skill rather than a one-off test implementation
- an existing testing skill needs to be adapted to another language, framework, or repository standard
- the user describes test conventions, commands, coverage gates, or mocking patterns and those instructions should become a durable skill
- you need to turn structured inputs plus workspace evidence into a ready-to-save `SKILL.md`

Do not use this skill to write or execute tests directly. Use it to author the skill that would guide that testing work.

## Inputs

| name | description | default | required | source | allowed values | example |
| ---- | ----------- | ------- | -------- | ------ | -------------- | ------- |
| language | Target programming language for the generated unit-testing skill. |  | Yes | user or derived | Any programming language with an established test ecosystem | Python |
| env | Runtime environment or version constraints that the generated skill must assume. | ecosystem default | No | user or derived | Versioned runtime, SDK, virtual environment, or container convention | 	venv Python 3.12 |
| testing_stack | Testing stack in comma-separated `key=value` form. Supported keys: `framework`, `assertion`, `mock`, `coverage`, `lint`. Infer missing keys from the ecosystem when possible. | ecosystem default | No | user or derived | Framework-specific tool choices | framework=pytest,assertion=assert,mock=unittest.mock,coverage=coverage |
| build_tool | Package manager, task runner, or build tool used to install dependencies and run tests. | ecosystem default | No | user or derived | Maven, Gradle, uv, npm, pnpm, go, cargo | uv |
| project_layout | Source, test, fixtures, and helper layout the generated skill should assume. | ecosystem default | No | user or derived | Repository-specific layout or mirrored defaults | src/ and tests/unit/ |
| context | Project-specific conventions that do not fit the structured fields above, such as naming patterns, commands, config files, or exception cases. |  | No | user | Repository conventions and special rules | Test file naming: `test_<module>.py`; use `uvx ruff check` for lint |
| domain_context | Optional framework or domain context that changes unit-testing patterns. |  | No | user or derived | Spring, FastAPI, React, Flink, CLI tools, data pipelines | FastAPI |
| coverage_target | Coverage threshold the generated skill should use as its default gate after tests and lint pass. | 80% | No | user or default | Percentage | 85% |
| max_iterations | Iteration cap for the generated skill's run-test-fix-improve loop. | 3 | No | user or default | Positive integer | 4 |
| skill_name | Directory and frontmatter name for the generated skill. Preserve the original name when refining an existing skill. | derived from request | No | user or derived | Valid skill folder name | python-pytest |

## Context

This skill builds unit-testing skills in six layers. Read [references/layers.md](references/layers.md) before drafting or revising the output skill. Every checklist item in that reference must become concrete, target-specific guidance. Do not leave the generated skill full of generic prompts such as "describe the mocking approach" or "insert commands here."

Use the layers as follows:

- Layer 1 defines language-agnostic testing principles that should survive stack changes.
- Layer 2 converts those principles into concrete commands, conventions, and tooling for `{language}`, `{testing_stack}`, `{build_tool}`, and `{project_layout}`.
- Layer 3 applies only when `{domain_context}` materially changes how unit tests should be written.
- Layer 4 defines the execution loop the generated skill should follow once invoked on a real codebase.
- Layer 5 defines the reporting structure the generated skill must require at the end of the run.
- Layer 6 defines how the generated skill should handle blockers, defects, and mismatched conventions.

Use [references/examples.md](references/examples.md) when you need a concrete example of how structured inputs map into a finished testing skill. Treat the examples as shape guidance, not copy-paste text.

## Core Principles

- MUST author or revise skills, not tests. If the request is actually to write test code, hand off to the appropriate testing skill instead of using this one.
- MUST resolve as much as possible from the user request and workspace context before asking follow-up questions.
- MUST preserve the original skill name when refining an existing skill unless the user explicitly asks to rename it.
- MUST prefer repository conventions over ecosystem defaults when they conflict.
- MUST turn each relevant checklist item from [references/layers.md](references/layers.md) into concrete, operational guidance.
- MUST explain tradeoffs when multiple testing stacks or conventions are plausible instead of silently choosing a surprising option.
- MUST keep the generated skill easy to read and easy to clarify: short sections, explicit labels, compact tables where useful, and no filler.
- MUST ensure every `{variable}` used in the generated skill is defined in its Inputs section or fully resolved into static text.
- NEVER leave unresolved placeholders, vague TODO language, or framework-agnostic filler in the generated skill.
- NEVER overfit the generated skill to one example if the user is asking for a reusable pattern.

## Workflow

### Step 1. Classify the request

Determine whether you are creating a new skill, refining an existing skill, or porting one skill to a new stack. If refining, inspect the current skill first and preserve any parts that are already working.

### Step 2. Resolve inputs from evidence first

Pull what you can from the request, nearby files, existing skills, and repository conventions. Use `/code-analysis` to inspect the workspace for testing patterns and the target stack. Infer sensible defaults for omitted optional inputs. Only ask follow-up questions for decisions that materially change the generated skill.

### Step 3. Present resolved and missing values

Summarize the inputs you resolved, the assumptions you made, and any missing values that still require confirmation. Keep this compact so the user can correct it quickly.

### Step 4. Choose the stack shape

Normalize `{testing_stack}` into concrete tool choices and explain any important defaults.

Typical mapping includes:

- framework
- assertion style
- mocking library or mechanism
- coverage tool
- lint or static-analysis tool

If the stack is partially specified, fill the rest using the target ecosystem's idiomatic defaults.

### Step 5. Compose the generated skill layer by layer

Use [references/layers.md](references/layers.md) as the source checklist and map it into the final skill structure required by [AGENTS.md](../../AGENTS.md):

- Layers 1-3 become most of the generated skill's `## Context` and `## Core Principles`
- Layer 4 becomes the generated skill's `## Workflow`
- Layer 5 becomes the generated skill's `## Output`
- Layer 6 becomes the generated skill's `## Error Handling`
When Layer 3 does not apply, omit it cleanly rather than leaving an empty section.

### Step 6. Make the generated skill operational

For the generated skill to be useful on first use, include concrete details such as:

- directory and naming conventions
- full-suite, focused-test, lint, and coverage commands
- mocking and fixture patterns
- async or concurrency guidance when relevant
- common pitfalls that are specific to the chosen stack
- a clear final reporting format

### Step 7. Validate the draft before returning it

Check the generated skill against this review list:

- frontmatter name matches `{skill_name}`
- description is specific enough to trigger in the right contexts
- the generated skill reads as a standalone document
- no unresolved placeholders remain
- commands, tools, and paths are internally consistent
- the workflow explains when to stop, what to report, and how to react to blockers

### Step 8. Return the skill plus a short decision summary

Provide the finished `SKILL.md` and briefly call out the key assumptions, defaults, or open questions that the user may want to adjust.

## Output

Return a complete, ready-to-save unit-testing skill for `{skill_name}`. The response should contain:

1. A short resolved-input summary covering the chosen language, stack, build tool, layout, domain context, coverage target, and iteration cap.
2. The finished `SKILL.md` content with valid frontmatter and sections ordered per [AGENTS.md](../../AGENTS.md).
3. A brief assumptions or follow-up section only if something important could not be inferred confidently.

The generated skill must stand on its own without requiring the reader to consult this creator skill during normal use.

## Error Handling

- If essential inputs such as `{language}` or the target stack cannot be inferred, ask the smallest set of clarifying questions needed to unblock the draft.
- If the repository conventions conflict with the user's stated preferences, surface the conflict and recommend which one the generated skill should follow.
- If the user asks to refine an existing skill and parts of it are already strong, keep them and replace only the weak or generic sections.
- If a domain-specific extension would materially improve the skill, add it; otherwise omit Layer 3 to keep the result lean.
- If you cannot confidently provide concrete commands, say what evidence is missing instead of inventing commands.

## Examples

See [references/examples.md](references/examples.md) for example input bundles.

Typical prompts that should trigger this skill include:

- "Create a reusable pytest skill for our FastAPI repos. We use Poetry, pytest-mock, coverage, and Ruff."
- "Port this unittest skill to JUnit 5 plus Mockito and keep the same layered structure."
- "Turn our team testing conventions into a skill instead of rewriting the same instructions every sprint."
