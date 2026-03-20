---
name: git-commit-and-push
description: Create or update a branch, commit and push local changes, or cherry-pick specified commits onto a target branch.  
allowed-tools: Bash(git {remote,rev-parse,branch,checkout,status,log,diff,fetch,rebase,stash,add,restore,commit,push,switch,pull,cherry-pick}:*)
metadata:
  version: 1.0.0
  author: xbhel
  tags: [git, commit, push, cherry-pick]
  aliases: [gcp]
---

## Goal

Create or update a branch, commit and push local changes, or cherry-pick specified commits from `source` onto a new branch created from `target`, then push that new branch.

## Inputs

|name|description|default|required|source|allowed values|
|---|---|---|---|---|---|
|source|`Commit & Push`: branch to commit and push. `Cherry-pick & Push`: branch that provides the commits.|Current branch or created branch|Yes|derived||
|target|`Commit & Push`: sync base branch. `Cherry-pick & Push`: clean base branch for the new destination branch.|`dev`|No|user or default||
|type|The type of change being made. Used for the commit message and new branch name.|`feat`|No|user or derived|`feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `revert`, `release`|
|workitem|The work item number this change belongs to.|Inferred from branch name (e.g., `feat/12345` → `12345`), otherwise auto-generated 7-digit random number|No|user or derived||

## Context

### Commands

- Get repo URL: `git remote get-url origin`
- Get repo root: `git rev-parse --show-toplevel`
- Get current branch: `git branch --show-current`
- Create a new branch: `git checkout -b <new_branch> origin/<branch>`
- Check working tree status: `git status --short`
- Log commits: `git log origin/<branch>..HEAD --oneline`
- List changed files: `git diff --name-status origin/<branch>..HEAD`
- Inspect changes: `git diff` and `git diff --cached`
- Fetch latest from branch: `git fetch origin <branch>`
- Rebase current branch on branch: `git rebase origin/<branch>`
- Stash changes: `git stash push -m <message> --include-untracked`
- Restore stashed changes: `git stash pop`
- Add changes to staging: `git add <files>`
- Unstage files: `git restore --staged <files>`
- Commit changes: `git commit -m <subject> -m <body>`
- Push target without force: `git push origin <branch>`
- Push branch (safe force): `git push origin <branch> --force-with-lease`

ONLY for **Cherry-pick & Push** workflow:

- Switch branch: `git switch <branch>`
- Pull latest target: `git pull origin <branch>`
- Filter commits: `git log --oneline origin/<branch> [--grep="<keyword>"] [--author="<name>"] [--after="<date>"] [--before="<date>"]`
- Cherry-pick commits: `git cherry-pick <commit>...`
- Abort/continue/skip cherry-pick: `git cherry-pick --abort/--continue/--skip`

### Commit message format

Subject: `<type>(<scope>)#{workitem}: <short_description>`

Body: Detailed description of the change, context, and intent. MUST use a Markdown list.

Where:

- `type`: the `{type}` input value.
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
- `scope`: optional, area of the codebase affected (e.g., `auth`, `ui`, `api`, `config`, etc.)
- `workitem`: the work item number provided as input.
- `short_description`: a short, concise summary of the change, derived from the work item title or change context.
- If the change is breaking, use `!` after `type` or `type(scope)`, and add a `BREAKING CHANGE:` note in the commit body.

Example:

- Subject: `feat(auth)!#12345: switch to JWT authentication`
- Body:
```markdown
- Replace session-based authentication with JWT.
- Update the login flow and token validation.
- BREAKING CHANGE: Clients must send a bearer token instead of using session cookies.
```

### Branch name format

`{type}/{workitem}-<descriptive_name>`

Where:

  - `type` and `workitem` are the same as in the commit message.
  - `descriptive_name`: max 20 characters, hyphen-separated description of the change, derived from the work item title or change context.

Example: `feat/12345-add-user-auth`

## Core Principles

- ONLY use the git commands listed in the `Context` section. When consecutive commands have no dependency on each other's output, MUST combine them with `&&` in a single execution to reduce round-trips.
- Simple cherry-pick, rebase, or merge conflicts MUST BE resolved directly. If the correct resolution is unclear, MUST stop and report the issue instead of guessing.

## Workflow

When user asks to move, apply, or merge specific commits from one branch to another, use the **Cherry-pick & Push** workflow. Otherwise, use the **Commit & Push** workflow by default.

### Commit & Push 

1. If the current branch is `{target}`, `dev`, `main`, or `master`, MUST create a new branch from it and switch to it. NEVER commit or push directly to these branches.
2. Stash any uncommitted or untracked changes to keep the working tree clean for the next step.
3. Fetch the latest `origin/{target}` and rebase the current branch on top of it.
4. Restore the stash if one was created in step 2.
5. Stage and commit any remaining changes using the commit message format defined in `Context`. 
6. Push the branch using the following command.

```bash
git fetch origin && git push origin <current_branch> --force-with-lease || git push origin <current_branch>
```

### Cherry-pick & Push

1. If commits are not explicit SHAs, resolve them first from `{source}` using the appropriate commit filters from `Context` (by keyword, author, date, or combination). List the matched commits and confirm with the user before proceeding.
2. Switch to the target branch and pull the latest changes.
3. MUST create a new branch from `{target}` and switch to the new branch. `{target}` MUST remain a clean base branch and MUST NOT receive the cherry-picked commits directly.
4. Cherry-pick the resolved commits onto the current branch.
5. Push the current branch to the remote.

```bash
git push origin <current_branch>
```

## Output

- The pushed branch name.
- List of commits included in the push, with their messages.
- List of files changed, added, or deleted in the commit.

## Error Handling

- If branch creation, synchronization, commit, or push fails, MUST report the exact failing step and preserve the branch state for manual recovery.
- If a cherry-pick conflict cannot be resolved, MUST run `git cherry-pick --abort` and switch back to the original branch.
