# Agents & Skills Guidelines

## Content Structure

When authoring a **skill file**, organize the content in the following order:

1. Metadata: Defined at the top of the file.
   - `name`
   - `description`
   - `allowed-tools` (optional)
   - `depends-on` (optional)
   - `metadata`:
     - `version`
     - `author`
     - `mcp-server` (optional)
     - `tags` (optional)
     - `aliases` (optional): alternative invocation names.
2. `## Goal`: Clear statement of the skill’s purpose and expected outcome.
3. `## Inputs`: Table of input parameters following the defined Input Schema below.
4. `## Context` (optional): Background, conventions, or assumptions that inform execution.
5. `## Core Principles` (optional): Constraints and rules that must be followed.
6. `## Workflow` (optional): Step-by-step execution process to achieve its goal.
7. `## Output` (optional): Expected output format and structure.
8. `## Error Handling` (optional): Rules for handling errors and exceptions.
9. `## Examples` (optional): Sample inputs and expected outputs demonstrating usage.

**Agents files** should follow a similar structure but may omit sections that are not relevant to their orchestration role.

Agent guidelines:

- Keep metadata first.
- Prefer including `## Goal`, `## Inputs`, and `## Workflow` sections for clarity.
- Add other sections only when they provide meaningful context or guidance.

## Input Schema

When a skill or agent defines an `##Inputs` section, it must use the following table schema:

| name | description | default | required | source | allowed values | example |
| ---- | ----------- | ------- | -------- | ------ | -------------- | ------- |

Fields:

- `name`: The name of the input parameter, used for referencing within the skill or agent by `{name}`.
- `description`: A brief explanation of the input parameter's purpose.
- `default` (optional): A default value for the input parameter.
- `required`: Whether the input parameter must be provided before execution (Yes/No).
  - `Yes`: The parameter must be provided by the user or inferred before execution.
  - `No`: The parameter is optional and may have a default value or be inferred if not provided.
- `source`: The origin of the input value. Allowed values include:
  - `user`: The value is provided directly by the user.
  - `derived`: The value can be inferred or calculated from other inputs or context.
  - `upstream`: The value is passed down from an upstream agent or skill in the workflow.
  - `default`: The value is a predefined default that can be used if no other source provides it.
  - combinations of the above (e.g., `user or derived`). Use short combinations joined by `or`.
- `allowed values` (optional): A list of permissible values for the input parameter.
- `example` (optional): An example value for the input parameter.

The optional columns may be omitted entirely from the table if they are not applicable to any input parameters.

## User Interaction

Users typically invoke an **agent** or **skill** by name.

If input parameters are required:

- Collect values through an appropriate interface (e.g., form, command line, API request).
- Prefer using `ask_questions` to gather or confirm input values unless another interface is better suited for the context.
- Present both:
  - **Missing values** that require user input.
  - **Inferred or pre-collected values**, allowing the user to review and confirm them before execution.

## Core Principles

- MUST use the correct model for the task, preferring the latest version:
  - GPT for reasoning
  - Gemini for creativity
  - Claude for orchestration and coding
- Reference input parameters with {} in skills/agents.
- Don’t ask for info that can be inferred or fetched via tools.
- Don’t assume completeness—check for missing inputs and request them explicitly.
