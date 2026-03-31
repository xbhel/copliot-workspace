## Goal

Open a pull request from a source branch to a target branch, using a repository template when available and adding reviewers or assignees when needed.

## Inputs

|name|description|default|required|source|
|---|---|---|---|---|
|source|Source branch for the pull request.|current branch|No|user or derived|
|target|Target branch for the pull request.|`dev`|No|user or default|
|reviewers|Reviewers to request on the pull request.|current user|No|user or derived|
|assignees|Assignees to add to the pull request.||current user|user or derived|

## Context

### PR Title Format

`<type>(<scope>)#<workitem>: <short_description>`

Fields are derived from the source branch name, user input, or commits in `target..source`:

- `type`: The type of changes, such as `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `revert`, `release`.
- `scope`: optional, area of the codebase affected (e.g., auth, ui, api, config).
- `workitem`: optional, reference to a work item or issue number.
- `short_description`: concise summary derived from the commits or user input.

### PR Body Template

```markdown
## Summary
<brief summary of the change>

- type: <type>
- workitem: #<workitem>
- <what changed>

## Validation
- <tests or checks run>

## Risks
- <known risks or follow-up items>
```

## Core Principles

- MUST strictly follow the PR title and body format for consistency and traceability.

## Workflow

1. **Resolve Inputs**: Determine `{source}`, `{target}`, `{reviewers}`, and `{assignees}` from the request and context.
2. **Generate Title**: Use `git log --oneline {target}..{source}` to derive the PR title per the `Context` format.
3. **Select Template**: Look for a PR template in `.github/` (ask the user if multiple exist). Fallback to the `Context` template if none are found.
4. **Create PR**: Build the PR body with the selected template and open the pull request.
5. **Assign**: Add the resolved `{reviewers}` and `{assignees}` if provided.

## Output

- Pull request URL.
- Pull request title.
- Target branch.
- Reviewers and assignees added.

## Error Handling

- If pull request creation succeeds but reviewer or assignee assignment partially fails, report the successful PR creation separately from the assignment failure.
