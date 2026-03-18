# Agents & Skills Guidelines

## Naming Conventions

- Skill: use lowercase, gerund form (verb-ing), and hyphen separation (e.g., creating-pull-request) to clearly express the action or capability provided.
- Agent: use lowercase, hyphen separation, and a role-based suffix (e.g., -assistant, -expert) to explicitly convey the agent’s responsibility and specialization (e.g., email-assistant).

## Content Structure

When authoring a **skill file**, organize the content in the following order:

1. Metadata:
   - `name`
   - `description`
   - `allowed-tools` (optional)
   - `depends-on` (optional)
   - `metadata`:
     - `version`
     - `owner`
     - `mcp-server` (optional)
     - `tags` (optional)
2. `## Goal`
3. `## Inputs`
4. `## Outputs` (optional)
5. `## Context` (optional)
6. `## Core Principles` (optional)
7. `## Workflow` (optional)
8. `## Error Handling` (optional)
9. `## Examples` (optional)

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
- `default`: A default value for the input parameter, if applicable.
- `required`: Whether the input parameter must be provided before execution (Yes/No).
  - `Yes`: The parameter must be provided by the user or inferred before execution.
  - `No`: The parameter is optional and may have a default value or be inferred if not provided.
- `source`: The origin of the input value. Allowed values include:
  - `user`: The value is provided directly by the user.
  - `derived`: The value can be inferred or calculated from other inputs or context.
  - `upstream`: The value is passed down from an upstream agent or skill in the workflow.
  - `default`: The value is a predefined default that can be used if no other source provides it.
  - combinations of the above (e.g., `user or derived`). Use short combinations joined by `or`.
- `allowed values`: A list of permissible values for the input parameter, if applicable.
- `example`: An example value for the input parameter, if applicable.

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

- Input parameters must be referenced using the `{}` syntax within the skill or agent definition.
- Never ask the user for information that can be inferred or obtained through allowed tools or commands.
- Never assume that the user has provided all necessary information. Always check for missing inputs and ask for them explicitly.
