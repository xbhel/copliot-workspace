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
