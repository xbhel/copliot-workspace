# Agents & Skills Guidelines

## Project Structure

The project is organized into the following directories:

- `agents/`: Agents definitions that orchestrate multiple skills to achieve complex tasks.
- `skills/`: Skill definitions and implementations.
- `mcp_servers/`: Mcp server implementations and related resources.
- `scripts/`: Utility scripts for testing, deployment, and maintenance.


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

## User Interaction

Users typically invoke an **agent** or **skill** by name. 

If input parameters are required:

- Collect values through an appropriate interface (e.g., form, command line, API request).
- Prefer using `ask_questions` to gather or confirm input values unless another interface is better suited for the context.
- Present both:
    - **Missing values** that require user input.
    - **Inferred or pre-collected values**, allowing the user to review and confirm them before execution.