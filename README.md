# Xbhel's Agent Workspace

Personal workspace for custom GitHub Copilot agents, reusable skills, and MCP tooling — versioned in one place.

## Structure

| Directory      | Purpose                                            |
| -------------- | -------------------------------------------------- |
| `agents/`      | Agent definitions that orchestrate multiple skills |
| `skills/`      | Skill definitions and implementations              |
| `mcp_servers/` | MCP server implementations                         |
| `scripts/`     | Utility scripts for testing and maintenance        |

## Setup

### Load the workspace in Copilot

Point `~/.copilot` at this repo so Copilot picks it up automatically.

**Linux/macOS**

```bash
ln -s /path/to/copilot-workspace ~/.copilot
```

**Windows (PowerShell)**

```powershell
# Requires Developer Mode or Admin. Use Junction if SymbolicLink is unavailable.
New-Item -ItemType SymbolicLink -Path "$HOME\.copilot" -Target "\path\to\copilot-workspace"
# or
New-Item -ItemType Junction -Path "$HOME\.copilot" -Target "\path\to\copilot-workspace"
```

### Load skills in Codex

Codex looks for skills at `~/.codex/skills/<skill-name>/SKILL.md`. It does not scan nested folders, so link each directory under `skills/` into `~/.codex/skills`.

**Linux/macOS**

```bash
source="/path/to/copilot-workspace/skills"
for dir in "$source"/*/; do
  ln -s "$dir" "$HOME/.codex/skills/$(basename "$dir")"
done
```

**Windows (PowerShell)**

```powershell
$source = "\path\to\copilot-workspace\skills"
Get-ChildItem -LiteralPath $source -Directory | ForEach-Object {
  New-Item -ItemType Junction -Path "$HOME\.codex\skills\$($_.Name)" -Target $_.FullName
}
```

> Restart Codex after adding or updating skills.

### Python Environment

This repo uses Python 3.12 and `uv`.

```bash
uv sync
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

## Skills

### SKILL Index List

- [/architect](skills/architect/SKILL.md): Design clear, extensible, and maintainable architecture proposals before implementation.
- [/clarify](skills/clarify/SKILL.md): Clarify ambiguous requirements and turn them into an implementation-ready specification.
- [/code-analysis](skills/code-analysis/SKILL.md): Analyze a codebase to understand behavior, interactions, and safe change points.
- [/code-review](skills/code-review/SKILL.md): Review code changes for correctness, regressions, test quality, and delivery risk.
- [/code-simplifier](skills/code-simplifier/SKILL.md): Simplify existing code for clarity and maintainability without changing behavior.
- [/dba](skills/dba/SKILL.md): Analyze database design, queries, schema changes, and data access risks.
- [/decompose](skills/decompose/SKILL.md): Break work into small, executable tasks with clear sequencing and parallelism.
- [/develop](skills/develop/SKILL.md): Orchestrate end-to-end delivery for non-trivial features from requirements to handoff.
- [/email-drafter](skills/email-drafter/SKILL.md): Draft and review professional emails that match your personal writing style.
- [/explain-words](skills/explain-words/SKILL.md): Explain words with pronunciation, meanings, morphology, phrases, and examples.
- [/frontend-design](skills/frontend-design/SKILL.md): Build distinctive, production-grade frontend interfaces with strong visual design.
- [/git-workflow](skills/git-workflow/SKILL.md): Execute common Git workflows such as branching, commit and push, cleanup, and pull requests.
- [/java-junit5](skills/java-junit5/SKILL.md): Add, run, fix, and report Java unit tests in Maven repositories with JUnit 5 tooling.
- [/normalize-links](skills/normalize-links/SKILL.md): Extract links from text and convert them into a consistent Markdown format.
- [/py-unittests](skills/py-unittests/SKILL.md): Generate and maintain Python unit tests with unittest, coverage, and ruff.
- [/quickstart](skills/quickstart/SKILL.md): Create concise, beginner-friendly quickstart guides for any topic.
- [/react-vitest](skills/react-vitest/SKILL.md): Generate and maintain React unit tests with Vitest, Testing Library, and MSW.
- [/rewrite](skills/rewrite/SKILL.md): Rewrite user requests into clear, natural, beginner-friendly English.
- [/skill-creator](skills/skill-creator/SKILL.md): Create, improve, evaluate, and package reusable skills.
- [/tdd](skills/tdd/SKILL.md): Apply test-driven development before implementing a feature or bug fix.
- [/unit-testing-skill-creator](skills/unit-testing-skill-creator/SKILL.md): Create or refine reusable unit-testing skills for specific stacks and conventions.
- [/web-design-guidelines](skills/web-design-guidelines/SKILL.md): Review UI code for Web Interface Guidelines compliance.
