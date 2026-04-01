## Goal

Open a pull request from a source branch to a target branch, using a repository template when available and adding reviewers or assignees when needed.

## Inputs

|name|description|default|required|source|
|---|---|---|---|---|
|source|Source branch for the pull request|current branch|No|user or derived|
|target|Target branch for the pull request|`dev`|No|user or default|
|reviewers|Reviewers to request|current user|No|user or derived|
|assignees|Assignees to add|current user|No|user or derived|

## Context

### PR Title

`<type>(<scope>)#<workitem>: <short_description>`

Derived from the source branch name, user input, or `git log --oneline {target}..{source}`:

- `type`: `feat` | `fix` | `chore` | `docs` | `style` | `refactor` | `perf` | `test` | `build` | `ci` | `revert` | `release`
- `scope`: _(optional)_ area affected, e.g. `auth`, `ui`, `api`
- `workitem`: _(optional)_ work item or issue number
- `short_description`: concise summary from commits or user input

### PR Body Template

```markdown
## Summary
<brief summary>
- type: <type>
- workitem: #<workitem>
- <what changed>

## Validation
- <tests or checks run>

## Risks
- <known risks or follow-up items>
```

### MCP Servers

| Platform    | Server          |
| ----------- | --------------- |
| Azure DevOps| microsoft/azure-devops-mcp |
| GitHub      | io.github.github/github-mcp-server |

### CLI

ALWAYS use `uv run python -m scripts.pull_request --help` to see available options before executing.

Example:

```bash
uv run python -m scripts.pull_request \
    --title "Add new feature for testing" \
    --description "This PR adds a new feature." \
    --source feat/278052-add-e2e-tracking \
    --target dev \
    --reviewers hex2 allen\
    --assignees allen \
    --workitems 2798156 \
    --is-draft \
    --is-auto-complete \
    --cwd "C:/workspace/project/3368-E2ETrackingSystem"
```

## Core Principles

- MUST strictly follow the PR title and body format for consistency and traceability.

## Workflow

1. **Resolve Inputs**: Determine `{source}`, `{target}`, `{reviewers}`, and `{assignees}` from the request and context.
2. **Generate Title**: Run `git log --oneline {target}..{source}` and format per [PR Title](#pr-title).
3. **Select Template**: Look for a PR template in `.github/`; prompt user if multiple exist. Fall back to [PR Body Template](#pr-body-template).
4. **Build Body**: Populate the template with commit context and user inputs.
5. **Create PR**: Use the [MCP server](#mcp-servers) for the detected platform; fall back to [CLI](#cli) if unavailable.
6. **Assign**: Add `{reviewers}` and `{assignees}` after PR creation.

## Output

- PR URL, title, and target branch
- Reviewers and assignees successfully added

## Error Handling

- If the PR is created but reviewer/assignee assignment partially fails, report the PR creation success and the assignment failures separately.
