## Goal

Open a pull request from a source branch to a target branch, using a repository template when available and adding reviewers or assignees when needed.

## Inputs

|name|description|default|required|source|
|---|---|---|---|---|
|source|Source branch for the pull request.|current branch|No|user or derived|
|target|Target branch for the pull request.|`dev`|No|user or default|
|reviewers|Reviewers to request on the pull request.|current user|No|user or derived|
|assignees|Assignees to add to the pull request.||No|user or derived|

## Context

### PR Title Format

`<type>(<scope>)#{workitem}: <short_description>`

Fields are derived from the source branch name, user input, or commits in `target..source`:

- `type`: The type of changes, such as `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `revert`, `release`.
- `scope`: optional, area of the codebase affected (e.g., auth, ui, api, config).
- `workitem`: optional, reference to a work item or issue number.
- `short_description`: concise summary derived from the commits or user input.

### PR Body Template

- Prefer repository PR templates if present in
  - `.github/PULL_REQUEST_TEMPLATE.md`
  - `.github/pull_request_template.md`
  - `.github/PULL_REQUEST_TEMPLATE/*.md`
- If multiple templates exist without clear precedence, ask the user to select one.
- If no template exists, use fallback:

```markdown
## Summary
<brief summary of the change>

- type: <type>
- workitem: <workitem>
- <what changed>

## Validation
- <tests or checks run>

## Risks
- <known risks or follow-up items>
```

## Workflow

1. Resolve `{source}`, `{target}`, `{reviewers}`, and `{assignees}` from the request and context.
2. Compute commit diff set using `git log --oneline {target}..{source}`.
3. Derive PR title from the commit diff set using the format defined in `Context`.
4. Check for a repository pull request template.
5. Build PR body using repository template if available, otherwise use fallback template in `Context`.
6. Create the pull request with resolved title and body.
7. Assign reviewers and assignees if provided or derivable.

## Output

- Pull request URL.
- Pull request title.
- Target branch.
- Reviewers and assignees added.

## Error Handling

- If pull request creation succeeds but reviewer or assignee assignment partially fails, report the successful PR creation separately from the assignment failure.
