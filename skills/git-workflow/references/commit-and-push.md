## Goal

Commit the intended local changes from a working branch, rebase onto the selected base branch, and push the result safely.

## Inputs

|name|description|default|required|source|
|---|---|---|---|---|
|target|Branch to update and push.|Current branch|No|user or derived|
|base|Branch used as the rebase target.|`dev`|No|user or default|
|workitem|The work item number this change belongs to.|Inferred from branch name (e.g., `feat/1234567_xxx → 1234567_xxx`) or auto-generated 7-digit random number|No|user or derived|

## Context

### Protected Branches

`dev`, `main`, `master`, `{base}`.

### Commit Message Format

**Subject:** `<type>(<scope>)#{workitem}: <short_description>`

**Body:** Detailed description of the change, context, and intent. MUST use a Markdown list.

**Breaking Changes:**

- MUST `!` after `type` or `type(scope)` in the subject.
- MUST include a `BREAKING CHANGE:` note in the body.

Fields:

- `type`: inferred from the branch name, changes, or user input. Common values: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `revert`, `release`.
- `scope`: optional, area of the codebase affected (e.g., auth, ui, api, config)
- `workitem`: required work item ID.
- `short_description`: concise summary derived from the work item or change context.

Example:

```markdown
Subject: feat(auth)!#1234567: switch to JWT authentication
Body:
Switch authentication from session-based to JWT for improved security and scalability. 
- Replace session-based authentication with JWT 
- Update login flow and token validation 
- BREAKING CHANGE: Clients must send a bearer token instead of session cookies
```

## Workflow

1. If `{target}` is protected, must create a new branch from it by [create-branch](./create-branch.md) and switch to it. NEVER commit or push directly to protected branches.
2. Stash any uncommitted or untracked changes to keep the working tree clean for the next step.
3. Fetch the latest `origin/{base}` and rebase the current branch on top of it.
4. Restore the stash if one was created in step 2.
5. Stage and commit any remaining changes using the [Commit Message Format](#commit-message-format) defined in `Context`.
6. Push the branch using the following command.

```bash
git push origin <current_branch> --force-with-lease || git push origin <current_branch> || git push -u origin <current_branch>
```

## Output

- Pushed branch name.
- Commit subject.
- Included commits.
- Summary of changed files.

## Error Handling

- MUST stop and ask the user to resolve it manually if a rebase conflict cannot be confidently resolved.
- MUST stop and report the exact failing step if branch creation, synchronization, commit, or push fails, and preserve the branch state for manual recovery.
