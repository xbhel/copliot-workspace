## Goal

Create a new working branch from the correct base branch using the shared branch naming convention.

## Inputs

|name|description|default|required|source|allowed_values|
|---|---|---|---|---|---|
|base|Base branch to branch from.|`dev`|No|user or default||
|type|The type of change being made.|`feat`|No|user or derived|`feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `revert`, `release`|
|workitem|The work item number this change belongs to.|Inferred from context or auto-generated 7-digit random number|No|user or derived||

## Context

**Branch Name Format:** `{type}/{workitem}_<descriptive_name>`.

- `type`: inferred from context or user input. Common values:
  - `feat`: new features or significant changes
  - `fix`: bug fixes or minor improvements
  - `chore`: maintenance or non-functional changes
  - `docs`: documentation only
  - `style`: formatting/style changes
  - `refactor`: code restructuring without behavior change
  - `perf`: performance improvements
  - `test`: adding or updating tests
  - `build`: changes to build process or dependencies
  - `ci`: CI/CD pipeline changes
  - `revert`: reverting a previous commit
  - `release`: changes related to versioning or releases
- `descriptive_name`: concise, hyphen-separated summary of the change (max 20 characters), derived from the work item or user input.

Example: `feat/1234578_add-user-auth`

## Workflow

1. Resolve `{base}`, `{type}`, `{workitem}`, and `<descriptive_name>` from the request and current context.
2. Fetch the latest `origin/{base}`.
3. Normalize `<descriptive_name>` to a concise, hyphen-separated slug (max 20 characters).
4. Create the branch using the format defined in `Context` from `{base}` and switch to it.

## Output

- Created branch name.
- Base branch used.

## Error Handling

- MUST stop and ask whether to reuse the branch or create a different name if the branch already exists.
- MUST stop and report the failure if `{base}` cannot be fetched or does not exist on origin.
