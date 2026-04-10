---
name: py-unittests
description: Generate and maintain unit tests for Python projects using unittest, unittest.mock, coverage, and ruff, managed by uv. Use this skill when adding, fixing, or improving Python unit tests with unittest-based tooling.
metadata:
  version: 1.0.0
  author: xbhel
---

# Python Unit Testing

## Goal

Generate, run, and iteratively improve unit tests for a Python project using the `unittest` framework, `unittest.mock` for isolation, `coverage` for reporting, and `ruff` for linting — all managed through `uv`.

## When to Use

Use this skill when:

- the task is to add, update, or improve Python unit tests in a `unittest`-based project
- test failures, coverage gaps, or test quality issues need iterative cleanup
- the workflow uses or should use `uv`, `coverage`, and `ruff`

## Inputs

| name | description | default | required | source |
| ---- | ----------- | ------- | -------- | ------ |
| project_layout | Source and test directory layout. `src_dir` is the production code root; `test_dir` is the test root. | src_dir=`src` or `src/lambda`, test_dir=`tests/unit` | No | user or derived |
| coverage_target | Minimum line-coverage percentage to pass the coverage gate. | 80% | No | user or default |
| max_iterations | Maximum number of test-and-fix loop iterations before stopping. | 5 | No | user or default |

## Context

### Test design

- Treat **tests as production-grade code**: clear names, focused assertions, and maintainable setup.
-  Follow the **AAA pattern** (Arrange, Act, Assert) to give every test a clear setup, action, and verification phase.
- Prefer **black-box testing**: verify externally observable behavior rather than internal implementation details so tests remain stable during refactoring.
- Each test targets the **smallest meaningful unit** — typically one method or function. Assume collaborators are correct; stub only what crosses system boundaries or introduces side effects.
- Keep tests **small, focused, and intent-revealing**. Use clear names; add comments only when setup or expectations are non-obvious.
- Isolate side effects with `Mock`, `MagicMock`, `AsyncMock`, `patch`, `patch.object`, and lightweight fakes when that is simpler than deep mocking.
- Keep tests deterministic by controlling time, randomness, environment variables, filesystem effects, and network calls.

### Naming and organization

- Test files: `test_<module>.py` inside `<test_dir>`.
- Test classes: `Test<ClassName>` extending `unittest.TestCase`.
- Test methods: `test_<method>_should_<expected>_when_<condition>` (BDD-style).
- Skip `__init__.py` unless it contains real logic.

### Project layout

```
<src_dir>/          # Production code
<test_dir>/         # Unit tests (mirrors <src_dir> structure)
pyproject.toml      # Project & tool configuration
```

### Environment and tooling

| Concern | Tool / Detail |
| ------- | ------------- |
| Runtime | Python 3.11+ in a virtual env `.venv/` |
| Package manager | `uv` |
| Test framework | `unittest` (stdlib) |
| Assertions | `unittest` assert methods (`assertEqual`, `assertRaises`, …) |
| Mocking | `unittest.mock` — `patch`, `MagicMock`, `PropertyMock` |
| Coverage | `coverage` package |
| Linting | `ruff` (via `uvx`) |

### Commands

| Action | Command |
| ------ | ------- |
| Sync dependencies | `uv sync` |
| Run all tests | `uv run python -m unittest discover -s <test_dir> -v` |
| Run specific test module | `uv run python -m unittest {test_module}` |
| Run with custom runner | `uv run python test_runner.py` |
| Lint (source + tests) | `uvx ruff check` |
| Coverage run | `uv run python -m coverage run -m unittest discover -s <test_dir>` |
| Coverage report | `uv run python -m coverage report -m` |

### Assertions

Use `unittest` assertion methods that produce clear failure messages:

- `assertEqual`, `assertNotEqual`, `assertTrue`, `assertFalse`
- `assertIs`, `assertIsNone`, `assertIn`, `assertIsInstance`
- `assertRaises`, `assertWarns` as context managers
- `assertAlmostEqual` for floating-point comparisons

### Test data management

- Use `setUp` / `tearDown` or `setUpClass` / `tearDownClass` for shared fixtures.
- Keep test data explicit and local to the test when possible; extract to helper factories only when reuse justifies it.

### Parameterized and data-driven tests

Use `subTest` to run multiple input sets inside one test method without stopping at the first failure:

```python
def test_parse_should_return_expected_when_given_valid_inputs(self):
    cases = [("1", 1), ("2", 2), ("0", 0)]
    for text, expected in cases:
        with self.subTest(text=text):
            self.assertEqual(parse(text), expected)
```

### Edge cases and failures

Cover boundary conditions, invalid inputs, empty collections, `None` values, exception paths, and expected error messages or types.

### Mocking and isolation

- **Patch where the name is looked up**, not where it is defined:
  ```python
  # module_under_test.py imports `requests` → patch 'module_under_test.requests'
  @patch("module_under_test.requests.get")
  def test_fetch(self, mock_get): ...
  ```
- Use `MagicMock` for complex collaborators and `PropertyMock` for properties.
- Prefer `spec=True` or `spec_set=True` to catch attribute typos at test time.
- Reset or re-create mocks between tests — `setUp` is the safest place.

### Async testing

For `asyncio`-based code (Python 3.11+), subclass `unittest.IsolatedAsyncioTestCase`:

```python
class TestAsyncFetch(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_should_return_data(self):
        result = await fetch_data()
        self.assertEqual(result, expected)
```

Patch async callables with `AsyncMock`.

### Lint integration

- Run `uvx ruff check` on both source and test code.
- Fix auto-fixable issues with `uvx ruff check --fix`.
- Suppress specific rules per-line only when justified (`# noqa: <rule>`).

### Coverage tooling

- Run: `uv run python -m coverage run -m unittest discover -s <test_dir>`
- Report: `uv run python -m coverage report -m` (shows missing lines).
- HTML: `uv run python -m coverage html` for detailed browsing.
- Configure in `pyproject.toml` under `[tool.coverage.run]` and `[tool.coverage.report]`.
- Target: **{coverage_target}** line coverage.

### Common pitfalls

| Pitfall | Remedy |
| ------- | ------ |
| Patching the definition site instead of the import site | Always patch where the name is looked up in the module under test. |
| Shared mutable state across tests | Use `setUp` to reinitialize state; avoid module-level mutable fixtures. |
| Forgetting to call `super().setUp()` in subclasses | Always call `super().setUp()` / `super().tearDown()` when overriding. |
| Import errors from wrong `PYTHONPATH` | Ensure `<src_dir>` is on the path — `uv run` handles this for packages declared in `pyproject.toml`. |
| Tests passing in isolation but failing together | Guard against shared global state, module-level side effects, and mock leaks. |
| Encoding issues on Windows | Use explicit `encoding="utf-8"` when opening files in tests. |

## Core Principles

- If a custom runner such as `test_runner.py` exists, use it when it is the established path.
- If the repository lacks `coverage` or `ruff`, report the blocker and continue with the strongest verifiable test result available.

## Workflow

### 1. Identify scope

- Map each source module under `<src_dir>` to its corresponding test file under `<test_dir>`.
- Skip files without meaningful logic: empty `__init__.py`, pure configuration, generated code.

### 2. Review existing tests

- Check that existing tests are correct, current, and meaningful.
- Identify untested behaviors, branches, and edge cases — avoid duplicating existing coverage.
- Rewrite tests only when they are stale, brittle, duplicated, or asserting the wrong behavior.

### 3. Add tests

- Prioritize: happy paths → boundary/edge cases → exception handling → business-logic branches.
- One behavior per test method; follow naming and AAA conventions from Context above.
- For filesystem, HTTP, database, clock, randomness, process, and environment boundaries, replace the dependency with a mock, stub, or fake rather than touching the real system.

### 4. Test-and-fix loop

Repeat up to **{max_iterations}** times:

1. **Run focused tests:** Run the focused test command first when possible.
2. **Run full test suite:** Run the full unit suite before finishing.
3. **Run lint:** `uvx ruff check`
4. **Fix failures:** Resolve all failing tests and lint violations before adding or refining tests.
5. **Measure coverage:** 
    - Run `uv run python -m coverage run -m unittest discover -s <test_dir>`
    - Report results with `uv run python -m coverage report -m`.
6. **Add or refine tests:** Target untested paths identified in the coverage report.
7. **Evaluate exit conditions:**
   - Stop if all tests pass, lint is clean, and coverage ≥ `{coverage_target}`.
   - Stop if `{max_iterations}` is reached; report any remaining coverage gaps.

### 5. Report the result

- Return the standardized summary from the Output section.
- Include remaining risks, meaningful coverage gaps, and any production-code issues discovered while testing.

## Output

After the final iteration, produce a summary:

| Item | Detail |
| ---- | ------ |
| Modules tested | List of source modules covered. |
| Test files created / updated | Paths of new or modified test files. |
| Tests added / changed | Count of new and modified test methods. |
| Coverage | Measured percentage (or estimate with justification). |
| Test status | Pass / fail counts from the final run. |
| Lint status | Clean or list of remaining violations. |
| Remaining coverage gaps | Untested paths or behaviors still needing coverage. |
| Code issues found | Production bugs, design concerns, or testability improvements discovered. |
| Iterations used / exit reason | Number of iterations consumed and which exit condition was met. |

## Error Handling

- **Untestable code:** Document why the code is hard to test, recommend the smallest design improvement, and describe the best available alternative test strategy.
- **Source code defects:** Document the bug, suggest a fix, and add a targeted regression test.
- **Testability refactoring:** Note the opportunity; ensure tests reflect intended behavior, not just current implementation.
- **Environment blockers:** Report the exact command, error output, and the corrective step taken or recommended.
- **Convention mismatch:** If the repository uses a different runner, layout, or naming convention than expected, adapt to match the project or explain the tradeoff.
