---
name: java-junit5
description: Add, run, fix, and report Java unit tests in Maven repositories using JUnit 5, AssertJ, Mockito, JaCoCo, and SonarLint.
metadata:
  version: 1.0.0
  author: xbhel
---

# Java JUnit 5

## Goal

Add, update, run, and iteratively improve Java unit tests in a Maven repository using JUnit 5, AssertJ, Mockito, JaCoCo, and SonarLint, with focused test execution first and explicit blocker reporting.

## When to Use

Use this skill when:

- the task is to create, fix, or expand unit tests for Java code in a Maven repository
- the repository uses or should use JUnit 5, AssertJ, Mockito, JaCoCo, and SonarLint
- the work needs concrete Maven commands, coverage-guided test additions, and a clear test-fix-report loop

## Inputs

| name | description | default | required | source | example |
| ---- | ----------- | ------- | -------- | ------ | ------- |
| target_scope | Production class, package, or method currently being changed or reviewed. | current task scope | No | user or derived | `com.example.billing.InvoiceService` |
| project_layout | Source and test layout the skill should assume. | `src/main/java` for source and `src/test/java` for tests | No | user or derived | `src/main/java`, `src/test/java` |
| coverage_target | Minimum JaCoCo coverage target to use as the default exit gate. | 80% | No | user or default | 85% |
| max_iterations | Maximum number of test-fix iterations before stopping and reporting remaining gaps. | 3 | No | user or default | 4 |

## Context

### Test design

- Tests MUST be treated as first-class code artifacts with the same readability and maintenance standards as production code.
- Tests MUST follow the AAA pattern so setup, action, and verification remain easy to inspect.
- Tests MUST prefer black-box verification of externally observable behavior over implementation-detail assertions.
- Each test MUST cover one meaningful behavior of one unit at a time, usually a single public method.
- Tests MUST stay deterministic by controlling clocks, randomness, threads, executors, filesystem access, and network boundaries.
- Tests MUST use clear names and minimal comments; comments are only for non-obvious setup or intent.

### Naming and organization

- Test files MUST live under `src/test/java` and mirror the package of the production type under `src/main/java`.
- Test classes MUST use the filename pattern `<ClassName>Test.java`.
- Test methods MUST use the pattern `<methodName>_should<ExpectedBehavior>When<Condition>`.
- Tests SHOULD use `@DisplayName` when it improves failure output for complex scenarios.
- Shared builders, fixtures, and test-only helpers SHOULD stay in `src/test/java` near the tests that use them.

### Project layout

```text
src/main/java/        Production code
src/test/java/        Unit tests mirroring production packages
pom.xml               Maven build, Surefire, dependencies, and JaCoCo configuration
target/site/jacoco/   Generated JaCoCo HTML report after `mvn verify`
```

### Environment and tooling

| Concern | Tool / Detail |
| ------- | ------------- |
| Runtime | JDK 11+ |
| Build tool | Maven 3.6+ |
| Test framework | JUnit 5 (`org.junit.jupiter:junit-jupiter`) |
| Assertions | AssertJ (`org.assertj:assertj-core`) |
| Mocking | Mockito (`org.mockito:mockito-core`, `org.mockito:mockito-junit-jupiter`) |
| Coverage | JaCoCo Maven Plugin bound to `verify` |
| Linting | SonarLint IDE plugin diagnostics |

### Commands

| Action | Command |
| ------ | ------- |
| Compile without running tests | `mvn -q -DskipTests compile` |
| Run all unit tests | `mvn test` |
| Run one test class | `mvn -Dtest=<ClassName>Test test` |
| Run one test method | `mvn -Dtest=<ClassName>Test#<methodName> test` |
| Run coverage and generate JaCoCo report | `mvn verify` |
| Inspect dependency tree | `mvn dependency:tree` |
| Analyze undeclared or unused dependencies | `mvn dependency:analyze` |
| Review lint findings | Inspect SonarLint diagnostics in the IDE Problems panel after each edit; no Maven CLI is assumed for SonarLint |

### Assertions and failure checks

- Assertions MUST use AssertJ as the default style: `assertThat(...)`, `assertThatThrownBy(...)`, and `assertThatExceptionOfType(...)`.
- Exception tests MUST verify the exception type and the most meaningful message or state change.
- Collection, optional, and numeric assertions SHOULD use AssertJ fluent matchers instead of bare boolean checks.

### Mocking, fixtures, and data design

- Mockito tests MUST use `@ExtendWith(MockitoExtension.class)` when annotation-based mocks are used.
- Collaborators that cross process, time, filesystem, network, database, or messaging boundaries MUST be isolated with mocks, stubs, or lightweight fakes.
- Tests SHOULD prefer constructor injection and plain object setup over partial mocks and deep spies.
- `@Mock`, `@InjectMocks`, `ArgumentCaptor`, `verify`, `never`, and `times` SHOULD be used only when they clarify behavior rather than lock tests to implementation noise.
- Test data MUST stay explicit. Extract builders or fixture factories only when repeated setup starts hiding intent.

### Parameterized tests

- Repeated input-output checks MUST use JUnit 5 parameterized tests instead of duplicated test methods.
- Use `@ParameterizedTest` with `@CsvSource`, `@MethodSource`, `@EnumSource`, or `@ValueSource` based on the data shape.

### Async and concurrent behavior

- Async code MUST be tested with deterministic coordination primitives such as `CompletableFuture`, injected `Executor` implementations, or `CountDownLatch`.
- Tests MUST NEVER rely on `Thread.sleep(...)` when a controllable executor, latch, or clock abstraction can make timing explicit.
- Time-sensitive code SHOULD depend on `Clock` or another injectable time source so tests can control time progression without waiting.

### Coverage tooling

- JaCoCo coverage MUST be produced with `mvn verify` and reviewed from `target/site/jacoco/index.html`.
- Coverage MUST be used to target untested branches, decision points, and exception paths rather than to inflate the raw percentage.
- If the JaCoCo plugin is missing, not bound to `verify`, or does not emit a report, that MUST be reported as a blocker instead of being silently ignored.

### Common pitfalls

| Pitfall | Remedy |
| ------- | ------ |
| Forgetting `MockitoExtension` so annotated mocks stay null | Add `@ExtendWith(MockitoExtension.class)` to the test class. |
| Verifying internal call order instead of observable outcomes | Assert returned values, state changes, thrown exceptions, or collaborator effects that matter to callers. |
| Using `Thread.sleep(...)` in tests | Inject controllable executors, latches, or clocks and wait on explicit completion signals. |
| Shared mutable fixtures leaking between tests | Rebuild fixtures per test and keep mutable state local. |
| Static utilities or hard-wired constructors make tests brittle | Refactor to constructor injection or extract a seam before resorting to static mocking. |
| JaCoCo report missing after `mvn verify` | Confirm the JaCoCo Maven plugin is configured and bound to the `verify` phase in `pom.xml`. |

## Core Principles

- The workflow MUST run the most focused Maven test command available before broader commands.
- The workflow MUST run the full unit suite before finalizing a change unless a documented blocker prevents it.
- The workflow MUST run coverage and inspect the JaCoCo report before claiming the work is complete unless coverage generation is blocked.
- The workflow MUST review SonarLint findings after edits and report any unresolved diagnostics that materially affect source or tests.
- When testing exposes a production defect, the workflow MUST document the defect and add a regression test when feasible.
- The workflow MUST prefer small refactors that improve testability over brittle mocks, reflection hacks, or implementation-coupled assertions.
- The workflow MUST preserve repository conventions when they differ from the defaults above and MUST report the tradeoff.
- The workflow MUST NEVER hide blockers; it must record the exact command, relevant error output, impact, and next corrective step.
- The workflow MUST NEVER stop after a focused test passes if the full suite, coverage run, or lint review still has pending issues.

## Workflow

### 1. Identify scope

- The workflow MUST map each changed production class in `src/main/java` to the matching test package and test class in `src/test/java`.
- The workflow MUST derive the most focused runnable target from `{target_scope}`:
  - method-level scope uses `mvn -Dtest=<ClassName>Test#<methodName> test`
  - class-level scope uses `mvn -Dtest=<ClassName>Test test`
  - broader or unknown scope falls back to `mvn test`
- The workflow MUST skip generated code, configuration-only classes, and trivial containers with no behavior unless they contain real logic worth testing.

### 2. Review existing tests

- The workflow MUST inspect existing tests for correctness, current behavior, and brittleness before adding new coverage.
- The workflow MUST identify coverage gaps in happy paths, edge cases, exception paths, and meaningful business branches.
- Existing tests MUST only be rewritten when they are incorrect, obsolete, duplicated, or tightly coupled to implementation details.

### 3. Add or revise tests

- New tests MUST prioritize happy paths first, then edge cases, failure scenarios, and branching logic.
- Each test MUST verify one behavior and keep setup local unless a shared fixture clearly improves readability.
- Repeated input variants MUST be collapsed into parameterized tests where that keeps intent clearer than separate methods.
- External boundaries such as HTTP clients, repositories, filesystem access, clocks, UUID generation, and executors MUST be isolated with mocks, stubs, or fakes.

### 4. Test-fix-coverage loop

Repeat the following steps up to `{max_iterations}` times:

1. Run the most focused test command available for the current change.
2. Fix compile errors, failing assertions, and broken test setup before adding more tests.
3. Review SonarLint diagnostics for the touched production and test files, then fix newly introduced issues or record why a warning remains.
4. Re-run the same focused test command until that scope is green.
5. Run the full unit suite with `mvn test`.
6. Run coverage with `mvn verify`.
7. Inspect `target/site/jacoco/index.html` and use the uncovered lines and branches to decide the next tests to add or refine.
8. Check exit conditions:
   - stop when focused tests pass, `mvn test` passes, SonarLint is clean or explained, and coverage is at least `{coverage_target}`
   - stop when `{max_iterations}` is reached and report the remaining gaps
   - stop early only for a documented blocker that prevents trustworthy continuation

### 5. Blocker reporting

- If `mvn -Dtest=... test`, `mvn test`, or `mvn verify` fails because of missing dependencies, Surefire selection issues, JaCoCo misconfiguration, compiler errors, or environment problems, the workflow MUST report:
  - the exact command that failed
  - the relevant error output excerpt
  - whether the blocker affects focused runs, full-suite runs, coverage, or lint validation
  - the corrective step taken or the smallest recommended next step
- If SonarLint is unavailable in the IDE, the workflow MUST report that lint validation could not be completed and continue with test and coverage evidence only.

### 6. Report the result

- The workflow MUST return the standardized summary from the Output section.
- The summary MUST include remaining risks, meaningful coverage gaps, and any production-code issues or refactoring opportunities discovered during testing.

## Output

After the final iteration, return a summary in this format:

| Item | Detail |
| ---- | ------ |
| Modules tested | List the production classes or packages covered by the final run. |
| Test files created or updated | List each new or modified test file. |
| Tests added or changed | Count the new and modified test methods. |
| Coverage | Report the measured JaCoCo percentage, or an estimate with a justification if coverage could not be measured. |
| Test status | Report final pass and fail counts from `mvn test` or the most complete available run. |
| Lint status | Report SonarLint as clean, unresolved with notes, or blocked. |
| Remaining coverage gaps | List important uncovered branches, edge cases, or failure paths. |
| Code issues or refactoring opportunities found | List production defects, design issues, or testability problems discovered during the work. |
| Iterations used and exit reason | Report how many iterations were used and whether the loop exited by success, blocker, or iteration cap. |

## Error Handling

- Untestable code MUST be reported with the reason it is hard to unit test, the smallest design improvement that would help, and the best fallback strategy available now.
- Production defects found during testing MUST be reported with a minimal reproduction, expected versus actual behavior, impact, and a targeted regression test when feasible.
- Refactors that materially improve testability or correctness SHOULD be recommended, but tests MUST still reflect intended behavior rather than current incidental structure.
- Environment or toolchain blockers MUST include the exact command, the relevant error output, what was tried, and the recommended next step.
- If the repository uses different naming, layout, or execution conventions than this skill assumes, the workflow MUST adapt to those conventions or explain why adaptation is unsafe.