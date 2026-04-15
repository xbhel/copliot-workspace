# Agents Guidelines

## Content Structure

When authoring a skill, organize the content in the following order:

1. Metadata: Defined at the top of the file.
2. Goal: Clear statement of the skill’s purpose and expected outcome.
3. When to Use: Guidance on scenarios where this skill is applicable.
4. Inputs (optional): Table of input parameters following the defined Input Schema below.
5. Context (optional): Background, conventions, or assumptions that inform execution.
6. Core Principles (optional): Constraints and rules that must be followed.
7. Workflow (optional): Step-by-step execution process to achieve its goal.
8. Output (optional): Expected output format and structure.
9. Error Handling (optional): Rules for handling errors and exceptions.
10. Examples (optional): Sample inputs and expected outputs demonstrating usage.

Always use `Must` to denote required behavior and `Never` to denote prohibited or anti-pattern behavior in `Core Principles`.

## Input Schema

When a skill or agent defines an `Inputs` section, it must use the following schema:

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

## User Interaction

Users typically invoke an **agent** or **skill** by name. If input parameters are required:

- Collect values through an appropriate interface (e.g., form, command line, API request).
- Prefer using `ask_questions` to gather or confirm input values unless another interface is better suited for the context.
- Present both:
  - **Missing values** that require user input.
  - **Inferred or pre-collected values**, allowing the user to review and confirm them before execution.

## Core Principles

- Never ask for info that can be inferred or fetched via tools.
- Never assume completeness—check for missing inputs and request them explicitly.
- Must begin each interaction by passively applying the `/rewrite` skill to the user’s request, without requiring explicit instruction.
