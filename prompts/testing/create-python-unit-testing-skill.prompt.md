---
description: Create a Python unit testing skill by analyzing existing test code and project structure, filling gaps with sensible Python/uv defaults.
argument-hint: Optionally specify domain/framework context (e.g., FastAPI, Flask) or project-specific overrides.
---

# Creating a Python Unit Testing Skill

## Defaults

Use the following preset details to fill gaps when the workspace or user request does not provide enough information. **Existing project conventions always take priority over these defaults.**

- language: Python
- env: Virtual env `.venv/`, Python 3.11+
- testing_stack: framework=unittest, assertion=unittest, mock=unittest.mock, coverage=coverage, lint=ruff
- build_tool: uv
- project_layout: src=`src` or `src/lambda`, test=`tests/unit`
- coverage_target: 80%
- max_iterations: 5
- context:
  - Test file naming: `test_<module>.py`
  - Run all tests: `uv run .venv/Scripts/python.exe -m unittest discover -s Tests/Unit -v`
  - Run specific tests: `uv run .venv/Scripts/python.exe -m unittest {test_module}`
  - Run with custom runner: `uv run .venv/Scripts/python.exe test_runner.py`
  - Lint: `uvx ruff check`
  - Coverage: `uv run .venv/Scripts/python.exe -m coverage report -m`
  - Skip `__init__.py` unless it contains real logic

## Workflow

1. Review `AGENTS.md` and `creating-unit-testing-skills` skill before drafting a new unit testing skill.
2. If the editor selection contains an example block, treat it as the highest-priority source for conventions and defaults.
3. Analyze existing test code, build files (`pyproject.toml`, `setup.cfg`, `requirements*.txt`), and project structure to infer conventions already in use. Existing project conventions always take priority — do not override them with the defaults above.
4. For any detail not covered by the project, fill in from the Defaults section above.
5. Do not ask for information that can be inferred from the workspace or selected context. Ask the user only for missing information that would materially change the generated skill.
6. Infer the destination path from repository conventions, such as `.copilot/skills/`, `.github/skills/`, `.claude/skills/`, or `skills/`.
7. Before creating the skill, present all resolved input values (per the `creating-unit-testing-skills` Inputs table) and the destination path for the user to confirm.
8. If the user does not confirm, clarify what is missing or incorrect, then re-infer as needed.
9. Create the skill by calling `creating-unit-testing-skills` and output the result along with a brief summary of the inferred assumptions and which values came from the project vs. defaults.
