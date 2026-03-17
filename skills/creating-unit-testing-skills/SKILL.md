---
name: creating-unit-testing-skills
description: Create or adapt unit testing skills across languages and testing stacks from a shared template.
metadata: 
  version: 1.0.0
  tags: [unit testing, test automation, meta-skill, template]
---

## Goal

Provide a reusable template for creating structured unit testing skills across languages by composing three layers: language-agnostic testing principles, language-specific adapters for conventions and best practices, and optional domain- or framework-specific extensions.

## Inputs

|name| description|default|required|source|example|
|-|-|-|-|-|-|
|language|Target programming language for generating unit tests.| |Yes|user or derived|Python|
|env|Runtime environment or version constraints for the target setup, such as `JDK 11` or `venv Python 3.12`.| |No|user or derived|venv Python 3.12|
|testing_stack|Testing stack in comma-separated `key=value` form. Supported keys: `framework`, `assertion`, `mock`, `coverage`. If omitted, infer sensible defaults from the language ecosystem.| ecosystem default |No|user or derived|framework=pytest,assertion=assert,mock=unittest.mock,coverage=coverage|
|build_tool|Package manager or build tool used to manage dependencies and run tests.| ecosystem default |No|user or derived|uv|
|project_layout|Source and test directory layout for the project.| ecosystem default |No|user or derived|src/ and tests/ directories|
|domain_context|Optional framework or domain context to tailor the generated tests (e.g., Spring, Flink, Vue).| |No|user or derived|Spring|

## Context

Use this skill as a template for creating unit testing skills for a specific language, testing stack, and optional framework or domain. Each layer is expressed as checklist items. For every applicable item, add concrete, target-specific details rather than leaving it as a generic prompt. Tailor the content to the target language, testing stack, and, when relevant, the business domain or framework context.

- Layer 1: **Language-agnostic principles** for test design, coverage, isolation, and readability.
- Layer 2: **Language- and stack-specific guidance** for the target framework, assertions, mocks, project layout, and test execution workflow.
- Layer 3: **Optional domain or framework extensions** for context-specific patterns, constraints, and examples such as Spring, Flink, or Vue.


### Layer 1: Language-agnostic principles

1. [ ] **Tests as first-class citizens:** Treat tests as essential code artifacts that deserve the same care, review standards, and maintenance discipline as production code.
2. [ ] **Test design:** Follow the AAA pattern (Arrange, Act, Assert) and verify externally observable behavior rather than internal implementation details (Black-box approach).
3. [ ] **Readability and maintainability:** Keep tests small, focused, and intent-revealing. Use clear names and only add comments when they clarify non-obvious setup or expectations.
4. [ ] **Naming and organization:** Define consistent naming conventions for test files, classes, and methods, using BDD-style names where appropriate, and group related tests so the suite is easy to navigate.
5. [ ] **Project structure:** Describe how to organize source code, test files, shared fixtures, test data, and helper utilities.
6. [ ] **Environment and tooling:** Explain how to set up the test environment and choose appropriate testing, assertion, mocking, and coverage tools.
7. [ ] **Build and test commands:** Describe the commands for running the full suite, targeting specific tests, inspecting dependencies, and generating coverage reports.
8. [ ] **Assertions:** Use clear, specific assertions that produce useful failure output and make the expected behavior obvious. Prefer fluent assertion styles when supported by the testing stack.
9. [ ] **Test data management:** Use fixtures, factories, or builders to keep test data explicit, reusable, and easy to evolve.
10. [ ] **Parameterized and data-driven tests:** Reuse the same test logic across multiple inputs when it improves coverage and reduces duplication.
11. [ ] **Edge cases and failures:** Cover boundary conditions, invalid inputs, exception paths, and expected failure scenarios.
12. [ ] **Mocking and isolation:** Use mocks, stubs, fakes, or spies to isolate the unit under test from external dependencies without obscuring the behavior being verified.
13. [ ] **Determinism and isolation:** Keep tests repeatable and independent by controlling time, randomness, network calls, concurrency, and shared mutable state.
14. [ ] **Async and concurrent behavior:** Explain how to test asynchronous logic, retries, timers, and concurrent behavior deterministically, and ensure tests wait for completion before asserting outcomes.
15. [ ] **Difficult-to-test code:** For static methods, private logic, legacy code, or other hard-to-test areas, prefer refactoring first. If refactoring is not feasible, use seams, dependency injection, or advanced mocking only when justified, and treat invasive testing approaches as a last resort.
16. [ ] **Coverage and reporting:** Use coverage reports to find untested paths, validate that critical behavior is exercised, and guide further test investment.
17. [ ] **Failure analysis:** Diagnose failing tests with useful output, and distinguish test defects from production defects so fixes target the right problem.
18. [ ] **Flaky or low-value tests:** Identify unstable, redundant, or low-signal tests, then improve, quarantine, or remove them as appropriate.
19. [ ] **Refactoring feedback loop:** Use test friction and test results as signals for improving production code design, modularity, and testability.
20. [ ] **Defect reporting:** When testing reveals a bug, document a minimal reproduction, expected versus actual behavior, impact, and the relevant test evidence.
