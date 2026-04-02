---
name: unit-testing-skill-creator
description: Create or adapt unit testing skills across languages and testing stacks using a layered template.
metadata: 
  version: 1.0.0
  author: xbhel
  tags: [unit testing, test automation, meta-skill, template]
  aliases: [ut-skill-creator]
---

# Unit Testing Skill Creator

## Goal

Create or adapt structured unit testing skills across languages and testing stacks using a layered template.

## When to Use This Skill

Use this skill when:

- the user wants to create a new reusable unit-testing skill rather than directly writing tests
- an existing testing skill needs to be adapted to a new language, framework, or project convention
- you need to generate a complete `SKILL.md` for unit testing from structured inputs and project-specific context

## Inputs

|name| description|default|required|source|allowed values|example|
|-|-|-|-|-|-|-|
|language|Target programming language for generating unit tests.| |Yes|user or derived| |Python|
|env|Runtime environment or version constraints for the target setup, such as `JDK 11` or `venv Python 3.12`.| |No|user or derived| |venv Python 3.12|
|testing_stack|Testing stack in comma-separated `key=value` form. Supported keys: `framework`, `assertion`, `mock`, `coverage`, `lint`. If omitted, infer sensible defaults from the language ecosystem.| ecosystem default |No|user or derived| |framework=pytest,assertion=assert,mock=unittest.mock,coverage=coverage|
|build_tool|Package manager or build tool used to manage dependencies and run tests.| ecosystem default |No|user or derived| |uv|
|project_layout|Source and test directory layout for the project.| ecosystem default |No|user or derived| |src/ and tests/ directories|
|context|Project-specific conventions to embed in the generated skill, such as naming conventions, test/lint/coverage commands, configuration files, or other details not covered by the structured inputs above.| |No|user| |Test file naming: `test_<module>.py`. Run tests: `uv run python -m unittest discover -s Tests/Unit -v`.|
|domain_context|Optional framework or domain context to tailor the generated tests (e.g., Spring, Flink, Vue, FastAPI).| |No|user or derived| |FastAPI|
|coverage_target|Optional coverage threshold enforced post-test pass; used for gating.|80%|No|user or default| |80%|
|max_iterations|Default iteration cap for the generated skill's test-and-fix loop (run tests → fix failures → improve coverage).|3|No|user or default| |3|

## Context

This skill composes six layers into a complete unit testing skill. Each layer is a **checklist of required items** that must be filled with **concrete, target-specific details**, not left as generic prompts. The structure follows the template defined in [references/layers.md](references/layers.md), including:

- **Layer 1: Language-agnostic principles** for test design, coverage, isolation, and readability.
- **Layer 2: Language-specific adapters** for the target framework, assertions, mocks, project layout, and test execution workflow.
- **Layer 3: Optional domain or framework extensions** for context-specific patterns, constraints, and examples such as Spring, Flink, or Vue.
- **Layer 4: Iterative test-and-fix workflow** defining the loop that runs tests, fixes failures, and improves coverage, controlled by `{max_iterations}` and `{coverage_target}`.
- **Layer 5: Output** defining the standardized summary the generated skill must produce after execution.
- **Layer 6: Error handling** defining how the generated skill should respond to failures, blockers, and untestable code.

## Core Principles

- **Skill creator only:** Produce SKILL.md files — never write, execute, or modify test code directly.
- **No generic placeholders:** Replace template items with actual project- and stack-specific guidance.
- **Self-contained output:** The generated skill must stand alone without referring back to this template.
- **Respect project conventions:** Prefer the target project's existing patterns over template defaults.
- **Readable and clarifiable format:** Keep the generated skill easy to read and easy to clarify. Use short sections, clear labels, and scannable lists or tables.

## Workflow

1. **Resolve inputs:** Collect or derive all input values. Infer sensible defaults for unresolved optional inputs from the target `{language}` ecosystem. Present resolved and missing values to the user for confirmation before proceeding.
2. **Compose the skill from the defined layers:** Use [references/layers.md](references/layers.md) as the source template and fill each checklist item with concrete guidance for the target language, stack, and project.
3. **Assemble the skill file:** Compose a complete SKILL.md per AGENTS.md structure. 
    - Map layers to sections: Layers 1–3 → Context and Core Principles; Layer 4 → Workflow; Layer 5 → Output; Layer 6 → Error Handling. 
    - Verify all `{variable}` references are defined in the Inputs table.

## Output

A reusable unit testing skill `<skill_name>/SKILL.md` for the target `{language}` and `{testing_stack}`, structured per AGENTS.md conventions.

## Examples

Refer to [references/examples.md](references/examples.md) for concrete Python and Java example input sets.
