# Examples

Use these examples as concrete input sets when creating a unit testing skill from the shared template.

## Create Python unit testing skill

- language: Python
- env: Virtual env `.venv/`, Python 3.11+
- testing_stack: framework=unittest, assertion=unittest, mock=unittest.mock, coverage=coverage, lint=ruff
- build_tool: uv
- project_layout: src=`src` or `src/lambda`, test=`tests/unit`
- coverage_target: 80%
- max_iterations: 5
- context:
  - Test file naming: `test_<module>.py`
  - Run all tests: `uv run python -m unittest discover -s tests/unit -v`
  - Run specific tests: `uv run python -m unittest <test_module>`
  - Run with custom runner: `uv run python test_runner.py`
  - Lint: `uvx ruff check`
  - Coverage: `uv run python -m coverage report -m`
  - Skip `__init__.py` unless it contains real logic

## Create Java unit testing skill

- language: Java
- env: JDK 11+, Maven 3.6+
- testing_stack: framework=JUnit 5, assertion=AssertJ, mock=Mockito, coverage=JaCoCo, lint=SonarLint
- build_tool: Maven
- project_layout: src=`src/main/java`, test=`src/test/java`
- coverage_target: 80%
- max_iterations: 5
- context:
  - Test class naming: `<ClassName>Test.java`
  - Test method naming: `<methodName>_should<ExpectedBehavior>When<Condition>`
  - Run all tests: `mvn test`
  - Run specific test class: `mvn test -Dtest=<ClassName>Test`
  - Run specific test method: `mvn test -Dtest=<ClassName>Test#<methodName>`
  - Coverage report: `mvn verify` (JaCoCo bound to `verify` phase), report at `target/site/jacoco/index.html`
  - Lint: SonarLint IDE plugin for real-time analysis
  - List dependency tree: `mvn dependency:tree`
  - Inspect a specific dependency: `mvn dependency:tree -Dincludes=<groupId>:<artifactId>`
  - Analyze unused/undeclared dependencies: `mvn dependency:analyze`
  - Use `@BeforeEach` and `@AfterEach` for per-test setup and teardown.
  - Use `@BeforeAll` and `@AfterAll` for per-class setup and teardown (must be static methods).
  - Use `@DisplayName` to provide a human-readable name for test classes and methods.
  - Use Mockito's `@Mock` and `@InjectMocks` annotations for test doubles, and `MockitoExtension` to enable them.
  - Use AssertJ's fluent assertions for clear, descriptive test expectations.
