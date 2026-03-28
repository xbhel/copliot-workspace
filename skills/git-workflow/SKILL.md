---
name: git-workflow
description: Execute common Git workflow actions with shared conventions for branch creation, commit/push, cherry-pick/push, branch cleanup, and pull request creation.
metadata:
  version: 1.0.0
  author: xbhel
  tags: [git, branch, commit, push, cherry-pick, pull-request]
---

## Goal

Execute the requested Git workflow action by using the matching action reference.

## Context

### Action References

Use the matching reference under `references/` based on the user's intent:

|reference|does|use when|
|---|---|---|
|`references/create-branch.md`|Creates a new working branch from a base branch using the shared naming convention.|starting new work, creating a branch, branching from `dev` or another base|
|`references/commit-and-push.md`|Commits local changes on the working branch and pushes the result.|saving changes, committing work, syncing with the base branch, pushing updates|
|`references/cherry-pick-and-push.md`|Cherry-picks selected commits onto a new branch created from the target branch and pushes it.|moving, replaying, or applying existing commits onto another branch|
|`references/clean-branch.md`|Deletes local branches and optionally deletes the matching remote branch.|cleaning up, removing, or pruning branches that are no longer needed|
|`references/create-pull-request.md`|Creates a pull request and adds reviewers or assignees when needed.|opening a PR, requesting review, assigning ownership for a branch|

### Commands

- Get repo URL: `git remote get-url origin`
- Get repo root: `git rev-parse --show-toplevel`
- Get current branch: `git branch --show-current`
- Create a new branch: `git checkout -b <new_branch> origin/<target>`
- Check working tree status: `git status --short`
- Log commits: `git log origin/<target>..HEAD --oneline`
- List changed files: `git diff --name-status origin/<target>..HEAD`
- Inspect changes: `git diff` and `git diff --cached`
- Fetch latest from branch: `git fetch origin <target>`
- Rebase current branch on branch: `git rebase origin/<target>`
- Stash changes: `git stash push -m <message> --include-untracked`
- Restore stashed changes: `git stash pop`
- Add changes to staging: `git add <files>`
- Unstage files: `git restore --staged <files>`
- Commit changes: `git commit -m <subject> -m <body>`
- Push branch without force: `git push origin <target>`
- Push branch (safe force): `git push origin <target> --force-with-lease`
- Switch branch: `git switch <target>`
- Pull latest from branch: `git pull origin <target>`

## Core Principles

- Use the commands listed in the `Context` section to perform common Git operations efficiently.
- MUST read and follow the selected reference before executing any action.
- MUST execute multiple actions in the required order if the request spans more than one.
- MUST combine consecutive commands with no dependency on each other's output using `&& ` in a single execution to reduce round-trips.

## Workflow

1. Identify the required action from the user request.
2. Select the corresponding reference.
3. Read the reference and gather required inputs.
4. Execute the action using that reference.
5. If multiple actions are requested, repeat the process in order.

## Output

- The action that ran.
- The result defined by the executed action reference.

## Error Handling

- If an action fails, report the failing step and preserve the current state described by the executed reference.
