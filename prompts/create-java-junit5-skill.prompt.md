---
description: Create a Java + JUnit 5 unit testing skill by analyzing existing test code and project structure, filling gaps with sensible Java defaults.
argument-hint: Optionally specify domain/framework context (e.g., Spring, Flink) or project-specific overrides.
---

# Creating a Java JUnit 5 Unit Testing Skill

## Defaults

Use the following preset details to fill gaps when the workspace or user request does not provide enough information. **Existing project conventions always take priority over these defaults.**

- language: Java
- env: JDK 11+
- testing_stack: framework=JUnit 5, assertion=AssertJ, mock=Mockito, coverage=JaCoCo, lint=SonarLint
- build_tool: Maven or Gradle (infer from project; default to Maven if ambiguous)
- project_layout: src_dir=`src/main/java`, test_dir=`src/test/java`
- context:
  - Generated skill inputs: `project_layout`, `coverage_target`, `max_iterations` (inferred from project or defaulted as above).
  - Test class naming: `<ClassName>Test.java`
  - Test method naming: `<methodName>_should<ExpectedBehavior>When<Condition>`
  - **Maven commands:**
    - Run all tests: `mvn test`
    - Run specific test class: `mvn test -Dtest=<ClassName>Test`
    - Run specific test method: `mvn test -Dtest=<ClassName>Test#<methodName>`
    - Coverage report: `mvn verify` (JaCoCo bound to `verify` phase), report at `target/site/jacoco/index.html`
    - List dependency tree: `mvn dependency:tree`
    - Inspect a specific dependency: `mvn dependency:tree -Dincludes=<groupId>:<artifactId>`
    - Analyze unused/undeclared dependencies: `mvn dependency:analyze`
  - **Gradle commands:**
    - Run all tests: `./gradlew test`
    - Run specific test class: `./gradlew test --tests <ClassName>Test`
    - Run specific test method: `./gradlew test --tests <ClassName>Test.<methodName>`
    - Coverage report: `./gradlew jacocoTestReport`, report at `build/reports/jacoco/test/html/index.html`
    - List dependencies: `./gradlew dependencies`
    - Inspect a specific dependency: `./gradlew dependencies --configuration testImplementation`
  - Lint: SonarLint IDE plugin for real-time analysis
  - Use `@BeforeEach` and `@AfterEach` for per-test setup and teardown.
  - Use `@BeforeAll` and `@AfterAll` for per-class setup and teardown (must be static methods).
  - Use `@DisplayName` to provide a human-readable name for test classes and methods.
  - Use Mockito's `@Mock` and `@InjectMocks` annotations for test doubles, and `MockitoExtension` to enable them.
  - Use AssertJ's fluent assertions for clear, descriptive test expectations.

## Workflow

1. Review `AGENTS.md` and `unit-testing-skill-creator` skill before drafting a new unit testing skill.
2. If the editor selection contains an example block, treat it as the highest-priority source for conventions and defaults.
3. Analyze existing test code, build files (`pom.xml`, `build.gradle`, `build.gradle.kts`), and project structure to infer the build tool and conventions already in use. Existing project conventions always take priority — do not override them with the defaults above.
4. For any detail not covered by the project, fill in from the Defaults section above.
5. Do not ask for information that can be inferred from the workspace or selected context. Ask the user only for missing information that would materially change the generated skill.
6. Infer the destination path from repository conventions, such as `.copilot/skills/`, `skills/`, or other equivalent directories.
7. Before creating the skill, present all resolved input values (per the `unit-testing-skill-creator` Inputs table) and the destination path for the user to confirm.
8. If the user does not confirm, clarify what is missing or incorrect, then re-infer as needed.
9. Create the skill by calling `unit-testing-skill-creator` and output the result along with a brief summary of the inferred assumptions and which values came from the project vs. defaults.
