# Xbhel's Copilot Workspace

A personal workspace for building, testing, and organizing custom GitHub Copilot agents, reusable skills, and MCP-related tooling.

## Overview

This repository is set up as a working area for experimenting with Copilot customization. It keeps agent guidance, skill definitions, local instructions, and supporting folders in one place so they can be versioned together.

## Setup

Create a symlink so Copilot can load this repo.

Linux/macOS:

```bash
ln -s "path/to/copilot-workspace" "~/.copilot"
```

Windows (PowerShell):

```powershell
New-Item -ItemType SymbolicLink -Path "$HOME\.copilot" -Target "path\to\copilot-workspace"
```
