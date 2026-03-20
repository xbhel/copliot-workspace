# Layer Templates

Use this file as the detailed reference for the six-layer unit testing skill template. Every checklist item must be turned into concrete, target-specific guidance for the generated skill.

## Layer 1: Language-agnostic principles template checklist

1. [ ] **Tests as first-class citizens:** Treat tests as essential code artifacts that deserve the same care, review standards, and maintenance discipline as production code.
2. [ ] **Test design:** Follow the AAA pattern (Arrange, Act, Assert) to give every test a clear setup, action, and verification phase.
3. [ ] **Black-box testing preference:** Verify externally observable behavior rather than internal implementation details so tests remain stable during refactoring.
4. [ ] **Unit scope:** Each test should target the smallest meaningful unit of behavior — typically a single method or function. Assume its collaborators are correct and already tested; stub only those that cross system boundaries or introduce side effects.
5. [ ] **Readability and maintainability:** Keep tests small, focused, and intent-revealing. Use clear names and only add comments when they clarify non-obvious setup or expectations.
6. [ ] **Naming and organization:** Test files, classes, and methods should follow consistent, discoverable naming conventions, using BDD-style names where appropriate, and be grouped so the suite is easy to navigate.
7. [ ] **Project structure:** Source code, test files, shared fixtures, test data, and helper utilities should have a clear, predictable directory layout.
8. [ ] **Environment and tooling:** Ensure the test environment is reproducible and its testing, assertion, mocking, and coverage tools are explicitly declared.
9. [ ] **Build and test commands:** Tests must be runnable with a single command covering the full suite, individual tests, and coverage reports.
10. [ ] **Assertions:** Use clear, specific assertions that produce useful failure output and make the expected behavior obvious. Prefer fluent assertion styles when supported by the testing stack.
11. [ ] **Test data management:** Use fixtures, factories, or builders to keep test data explicit, reusable, and easy to evolve.
12. [ ] **Parameterized and data-driven tests:** When multiple inputs exercise the same behavior, share one test definition rather than duplicating test logic.
13. [ ] **Edge cases and failures:** Cover boundary conditions, invalid inputs, exception paths, and expected failure scenarios.
14. [ ] **Mocking and isolation:** Isolate the unit under test from external dependencies using test doubles (mocks, stubs, fakes, or spies), without obscuring the behavior being verified.
15. [ ] **Determinism and isolation:** Keep tests repeatable and independent by controlling time, randomness, network calls, concurrency, and shared mutable state.
16. [ ] **Async and concurrent behavior:** Asynchronous and concurrent logic must be tested deterministically, with explicit control over timing, retries, and completion signaling.
17. [ ] **Difficult-to-test code:** For static methods, private logic, legacy code, or other hard-to-test areas, prefer refactoring first. If refactoring is not feasible, use seams, dependency injection, or advanced mocking only when justified, and treat invasive testing approaches as a last resort.
18. [ ] **Coverage and reporting:** Coverage reports should guide test investment toward untested paths and critical behavior, not serve as a vanity metric.
19. [ ] **Failure analysis:** Diagnose failing tests with useful output, and distinguish test defects from production defects so fixes target the right problem.
20. [ ] **Flaky or low-value tests:** Identify unstable, redundant, or low-signal tests, then improve, quarantine, or remove them as appropriate.
21. [ ] **Refactoring feedback loop:** Use test friction and test results as signals for improving production code design, modularity, and testability.
22. [ ] **Defect reporting:** When testing reveals a bug, document a minimal reproduction, expected versus actual behavior, impact, and the relevant test evidence.

## Layer 2: Language-specific adapters template checklist

For each item, replace the generic guidance with concrete details for `{language}`, `{testing_stack}`, `{build_tool}`, and `{project_layout}`.

1. [ ] **Framework and assertion style:** Specify the test framework, assertion API, and any required configuration or plugins. Map `{testing_stack}` keys to concrete packages and versions.
2. [ ] **Project layout:** Define directory conventions, test file naming, module discovery rules, and how `{project_layout}` maps to the language's toolchain expectations.
3. [ ] **Environment setup:** Describe how to create and activate the runtime environment (`{env}`), install test dependencies with `{build_tool}`, and handle version or platform constraints.
4. [ ] **Commands:** Provide concrete commands using `{build_tool}` for: running the full suite, running specific tests, and running with a custom runner if applicable.
5. [ ] **Mocking and fixtures:** Document the language-idiomatic patterns for test doubles — mock libraries, patching mechanisms, fixture lifecycle hooks, and common pitfalls such as patch-target resolution.
6. [ ] **Parameterized tests:** Show the language-specific mechanism for data-driven or parameterized tests (e.g., `subTest`, `@ParameterizedTest`, `pytest.mark.parametrize`).
7. [ ] **Async testing:** Describe the language's async test support — base classes, decorators, event-loop handling, and how to patch time-based or scheduler dependencies.
8. [ ] **Lint integration:** Specify the linter and the commands for checking both source and test code, including any test-specific lint rules or suppressions.
9. [ ] **Coverage tooling:** Name the coverage tool, show how to run it, interpret output, and configure branch-level or statement-level reporting.
10. [ ] **Common pitfalls:** List language-specific mistakes that frequently cause test failures or flakiness, such as import-path errors, shared mock state, implicit global state, or encoding issues.

## Layer 3: Optional domain or framework extensions template checklist

This layer applies only when `{domain_context}` is specified. Populate each item with concrete, framework- or domain-specific details.

1. [ ] **Framework test utilities:** Document built-in test tools (e.g., base classes, harnesses, test clients) and specify when they should be used instead of general-purpose mocks or stubs.
2. [ ] **Domain-specific test patterns:** Define testing idioms unique to the domain (e.g., stateful vs. stateless validation, request-response flows, event-driven processing, component lifecycle testing).
3. [ ] **Domain-specific test data design:** Specify how test data should vary across domain-critical dimensions (e.g., event ordering, timestamps, schema versions, auth states, user interaction sequences).
4. [ ] **Representative scenarios:** Identify realistic scenarios covering business workflows, known failure modes, and boundary conditions beyond generic edge cases.
5. [ ] **Integration boundaries:** Clarify what should be unit tested vs. deferred to integration/E2E tests, and how framework utilities can simulate external dependencies at the unit level.
6. [ ] **Minimal test environment:** Recommend the lightest viable test setup that preserves correctness, and outline tradeoffs versus heavier environments (e.g., full containers, embedded runtimes).
7. [ ] **Framework-managed state and lifecycle:** Describe how to test framework-controlled state and lifecycle events (e.g., initialization, teardown, recovery, session/state stores).
8. [ ] **Serialization and data contracts:** Define strategies for testing serialization, schema evolution, format compatibility, and cross-boundary type safety where applicable.
9. [ ] **Framework-specific pitfalls:** List common testing mistakes and gotchas (e.g., threading assumptions, hidden global config, discrepancies between test and production behavior).

## Layer 4: Iterative test-and-fix workflow template checklist

This layer defines the execution workflow for the generated skill, controlled by `{max_iterations}` and `{coverage_target}`.

### 1. Identify scope

- [ ] **Target mapping:** Identify all source modules and map each to its corresponding test file location.
- [ ] **Exclusion rules:** Define files to skip (e.g., modules without logic, generated code, configuration-only files).

### 2. Review existing tests

- [ ] **Correctness check:** Ensure existing tests are still correct, current, and meaningful.
- [ ] **Gap analysis:** Identify untested behaviors, branches, and edge cases without duplicating existing coverage.
- [ ] **Rewrite criteria:** Rewrite tests only if they are incorrect, obsolete, or excessively brittle.

### 3. Add tests

- [ ] **Coverage priorities:** Focus new tests on happy paths, boundary/edge cases, exception handling, and business-logic branches.
- [ ] **One behavior per test:** Each new test should verify a single behavior aligned with the unit scope principle (Layer 1 #4).

### 4. Test-and-fix loop

- [ ] **Loop structure:** For each iteration: run tests -> run lint -> fix failures -> add/refine tests -> evaluate exit conditions.
- [ ] **Fix priority:** Resolve failing tests and lint issues before introducing new tests.
- [ ] **Coverage-driven additions:** Use coverage reports to target untested paths rather than adding tests blindly.
- [ ] **Exit conditions:** Stop when all tests pass, lint is clean, coverage meets `{coverage_target}`, or `{max_iterations}` is reached.

## Layer 5: Output template checklist

This layer defines the output template for the generated skill.

1. [ ] **Modules tested:** List all source modules that were covered by the test run.
2. [ ] **Test files created or updated:** List test files that were newly created or modified.
3. [ ] **Number of tests added or changed:** Count of new and modified test methods.
4. [ ] **Measured or estimated coverage:** Coverage percentage from the coverage tool, or an estimate with justification.
5. [ ] **Test status:** Pass and fail counts from the final test run.
6. [ ] **Lint status:** Whether lint checks passed cleanly, with any remaining violations noted.
7. [ ] **Meaningful coverage gaps remaining:** Untested paths, branches, or behaviors that still need coverage.
8. [ ] **Code issues or refactoring opportunities found:** Production code problems, design concerns, or testability improvements discovered during testing.
9. [ ] **Iterations used and exit reason:** Number of iterations consumed and which exit condition was met.

## Layer 6: Error handling template checklist

This layer defines how the generated skill should handle problems encountered during test creation and execution.

1. [ ] **Untestable code:** When code is difficult to unit test due to tight coupling or external dependencies, document why, recommend the smallest design improvement, and describe the best available alternative test strategy.
2. [ ] **Source code defects:** When a bug is discovered in production code during testing, document the issue, suggest a fix, and add a targeted regression test where possible.
3. [ ] **Testability refactoring:** When refactoring would improve testability or correctness, note the opportunity and ensure tests reflect intended behavior rather than only the current implementation.
4. [ ] **Environment blockers:** When test execution is blocked by missing dependencies, environment misconfiguration, or toolchain issues, report the exact command, the error output, and the corrective step taken or recommended.
5. [ ] **Convention mismatch:** When the repository uses a different test runner, project layout, or naming convention than expected, adapt safely or explain the tradeoff to the user.
