---
name: react-vitest
description: Generate and maintain React component and hook unit tests using pnpm, Vitest, Testing Library, MSW, and ESLint. Use this skill when adding, fixing, or improving frontend unit tests that cover component behavior, async UI state, mocked network interactions, or component-level integration boundaries.
metadata:
  version: 1.0.0
  author: xbhel
---

# React Vitest Unit Testing

## Goal

Generate, run, and iteratively improve React unit tests for frontend repositories using Vitest, Testing Library, MSW, and ESLint, with concrete guidance for async UI state, mocked network calls, and the boundary between unit and component-integration tests.

## When to Use

Use this skill when:

- the task is to add, update, or improve unit tests for React components, hooks, or small UI utilities
- the repository uses `pnpm`, `vitest`, Testing Library, MSW, and ESLint, or should align to that stack
- the work includes loading, error, empty, retry, or success states driven by async UI behavior
- networked components need realistic request mocking without calling live APIs
- the user needs guidance on whether a behavior belongs in a unit test, a component-integration test, or a broader E2E test

Do not use this skill to design full browser E2E coverage. Use it for unit and component-level integration work inside the frontend test runner.

## Inputs

| name | description | default | required | source | example |
| ---- | ----------- | ------- | -------- | ------ | ------- |
| project_layout | Source, test, setup, and mock-server layout to follow when the repository already has conventions. | `src/` with colocated `*.test.tsx` or nearest `__tests__/`; shared setup in `test/setup.ts`; MSW files in `test/msw/` | No | user or derived | `src/`, `src/test/`, `test/setup.ts`, `test/msw/` |
| coverage_target | Minimum coverage gate to treat the run as complete after tests and lint pass. | 80% | No | user or default | 85% |
| max_iterations | Maximum number of test-and-fix iterations before stopping and reporting remaining gaps. | 3 | No | user or default | 4 |
| context | Extra repository conventions such as existing scripts, shared render helpers, provider wrappers, aliases, or lint rules. | none | No | user or derived | `Use pnpm test:unit and renderWithProviders from src/test/utils.tsx.` |

## Context

### Test design

- Treat tests as production-grade code: small, readable, and maintained with the same discipline as the components they cover.
- Follow the AAA pattern so each test has a clear setup, action, and verification phase.
- Prefer black-box verification over implementation details. Assert on what the user can observe: text, roles, labels, enabled or disabled states, error messaging, focus, and callbacks visible at the component boundary.
- Test one meaningful behavior per test. For React, that usually means one user-visible state transition or one contract at the component or hook boundary.
- Keep tests deterministic by controlling timers, network calls, dates, random values, and shared mock state.

### Naming and organization

- Respect `{project_layout}` if the repository already defines it.
- If the repository has no strong convention, default to colocated test files named `ComponentName.test.tsx`, `hookName.test.ts`, or a nearby `__tests__/` directory mirroring the source tree.
- Prefer BDD-style names such as `it('shows an error banner when the save request fails')`.
- Keep shared test utilities in one obvious place such as `test/setup.ts`, `test/utils.tsx`, and `test/msw/`.
- Skip pure barrel files, generated types, stylesheets, icons, and Storybook stories unless they contain real logic worth unit testing.

### Project layout

Use the lightest structure that matches the repo:

```text
src/                      # React components, hooks, utilities
src/components/           # UI components
src/hooks/                # Custom hooks
test/setup.ts             # Vitest + Testing Library + MSW setup
test/utils.tsx            # renderWithProviders and shared helpers
test/msw/handlers.ts      # Default request handlers
test/msw/server.ts        # setupServer(...) for Node-based tests
```

If the repo already uses `src/test/` or colocated utilities, keep that structure rather than moving files around.

### Environment and tooling

| Concern | Tool / Detail |
| ------- | ------------- |
| Package manager | `pnpm` |
| Test runner | `vitest` |
| DOM environment | `jsdom` unless the repo already uses `happy-dom` |
| Rendering and queries | `@testing-library/react` |
| User interactions | `@testing-library/user-event` |
| DOM assertions | `@testing-library/jest-dom/vitest` |
| Network mocking | `msw` with `setupServer` |
| Module mocking | `vi.mock`, `vi.fn`, `vi.spyOn` |
| Coverage | `@vitest/coverage-v8` unless the repo already standardizes on Istanbul |
| Linting | `eslint` |

Ensure the repo has these dependencies before relying on them. If the repo defines package scripts such as `test`, `test:unit`, `coverage`, or `lint`, prefer those scripts over raw `pnpm exec` commands.

### Commands

| Action | Command |
| ------ | ------- |
| Install dependencies | `pnpm add -D vitest @vitest/coverage-v8 jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom msw eslint` |
| Run all unit tests | `pnpm exec vitest run` |
| Run in watch mode | `pnpm exec vitest` |
| Run one test file | `pnpm exec vitest run src/components/Button.test.tsx` |
| Run one test by name | `pnpm exec vitest run src/components/Button.test.tsx -t "shows loading state"` |
| Run coverage | `pnpm exec vitest run --coverage` |
| Run lint | `pnpm exec eslint . --ext .js,.jsx,.ts,.tsx` |

### Assertions and test data

- Use Testing Library queries in this order: `getBy*` for synchronous presence, `findBy*` for eventual presence, `queryBy*` for absence.
- Prefer `toBeInTheDocument`, `toHaveTextContent`, `toBeDisabled`, `toHaveAccessibleName`, and other `jest-dom` assertions that explain failures well.
- Use `it.each` or `describe.each` when the same UI rule must hold across multiple inputs, roles, or feature-flag combinations.
- Keep fixtures explicit. For UI tests, vary data by user-visible states: loading, success, empty, partial data, validation failure, permission denied, and retry-after-error.

### Async UI state

Async UI tests MUST verify the full visible state transition, not just the final settled state.

- Create a `user` instance with `userEvent.setup()` and `await` every meaningful interaction.
- Use `await screen.findBy...` for content that appears after a promise resolves.
- Use `await waitFor(...)` when the expected change is indirect or not tied to a single element query.
- Use `await waitForElementToBeRemoved(...)` for spinners, skeletons, toasts, and temporary placeholders.
- If the component uses debouncing, polling, or delayed dismissal, use fake timers only around that behavior and always restore them after the test.
- Do not assert immediately after a click if the component schedules asynchronous state updates.

Example:

```tsx
it('shows a spinner before rendering the loaded profile', async () => {
  const user = userEvent.setup()
  render(<ProfilePanel userId="42" />)

  expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /reload/i }))

  expect(await screen.findByRole('heading', { name: /ada lovelace/i })).toBeInTheDocument()
  await waitForElementToBeRemoved(() => screen.queryByRole('status', { name: /loading/i }))
})
```

### Mocking and fixtures

- Use MSW for HTTP boundaries. For components that call `fetch`, `axios`, React Query, SWR, or a thin API client, prefer MSW over mocking `fetch` directly because it preserves the real request path and response timing.
- Use `vi.mock` for non-network collaborators such as analytics, feature flags, date helpers, or router hooks when those dependencies are outside the behavior under test.
- Build a shared `renderWithProviders` helper when components require router, theme, i18n, auth, query-client, or state-provider wrappers.
- Reset mock state after each test with `vi.restoreAllMocks()` and reset MSW handlers with `server.resetHandlers()`.

Minimal MSW setup:

```ts
// test/msw/server.ts
import { setupServer } from 'msw/node'

export const server = setupServer()
```

```ts
// test/setup.ts
import '@testing-library/jest-dom/vitest'
import { afterAll, afterEach, beforeAll, vi } from 'vitest'
import { cleanup } from '@testing-library/react'
import { server } from './msw/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => {
  server.resetHandlers()
  vi.restoreAllMocks()
  cleanup()
})
afterAll(() => server.close())
```

Per-test network override:

```ts
server.use(
  http.get('/api/profile/42', () => {
    return HttpResponse.json({ message: 'temporarily unavailable' }, { status: 503 })
  })
)
```

### React-specific patterns and integration boundaries

Use the smallest environment that still exercises the real behavior.

- Treat a test as a unit test when it focuses on one component or one hook and stubs only true boundaries such as network, time, storage, or browser APIs.
- Treat a test as a component-integration test when the behavior crosses real providers or multiple collaborating components: router state, query cache, auth context, form libraries, or a parent-child interaction that would be brittle to fake.
- Keep both unit and component-integration tests inside Vitest when the behavior can be modeled with `render` plus lightweight providers and MSW.
- Escalate to E2E only for concerns that require a real browser or full application shell: navigation across pages, CSS layout, file downloads, focus traps across route transitions, or integration with a real backend.

Rules of thumb:

- If the test only needs props plus one mocked boundary, keep it unit-level.
- If the test must prove several components, providers, and async data flow work together, keep it as a component-integration test but still mock the network with MSW.
- Never mock React itself, Testing Library queries, or the component under test.
- Never assert on internal state variables, hook call counts, or implementation-only DOM structure when a user-observable assertion is available.

Representative React scenarios to cover when relevant:

- loading to success transition
- loading to empty state transition
- loading to error state with retry
- optimistic update success and rollback on failure
- validation errors after user input
- permission-based rendering
- stale data refresh or refetch after interaction

### Coverage tooling

- Run `pnpm exec vitest run --coverage`.
- Treat the report as a guide for missed branches and user-visible states, not a vanity metric.
- Target `{coverage_target}` as the default gate after tests and lint pass.
- Prefer adding tests for uncovered branches in components, hooks, and adapters before chasing total-file percentages on passive wrappers.

### Common pitfalls

| Pitfall | Remedy |
| ------- | ------ |
| Using `getBy*` for async content | Use `findBy*` or `waitFor` so the test waits for the real UI transition. |
| Not awaiting `userEvent` calls | Always `await` interactions that trigger state updates. |
| Mocking `fetch` or `axios` directly in component tests | Prefer MSW so request behavior stays realistic and reusable. |
| Forgetting to reset MSW handlers or spies | Reset in `afterEach` to prevent state leaking between tests. |
| Over-mocking child components, providers, or hooks | Render the real collaboration unless the dependency is outside the unit boundary. |
| Relying on snapshots for dynamic UI states | Prefer explicit assertions on visible content and accessibility roles. |
| Leaving unresolved timers or promises | Use fake timers only when needed, then restore them and wait for the DOM to settle. |
| Ignoring repository-specific scripts or helpers in `{context}` | Reuse established scripts and helpers before introducing new ones. |

## Core Principles

- You MUST apply any repository-specific conventions from `{context}` before adding new patterns.
- You MUST prefer package scripts and shared helpers that already exist over inventing parallel commands or utilities.
- You MUST test user-visible behavior rather than implementation details.
- You MUST use MSW for networked component behavior unless the repository already has a stronger established boundary-mocking pattern.
- You MUST keep unit tests deterministic by controlling timers, request handlers, spies, and shared provider state.
- You MUST explain when a requested scenario belongs in a component-integration or E2E test instead of forcing it into a brittle unit test.
- You MUST keep tests readable: focused setup, clear actions, and assertions that communicate intent.
- NEVER leave live network access enabled in component tests.
- NEVER mock React internals, Testing Library itself, or the component under test.
- NEVER rewrite existing tests only for style if they are already correct, readable, and stable.

## Workflow

### 1. Identify scope

- Map each target component, hook, or utility under the repo's source tree to its expected test file under `{project_layout}`.
- Skip generated files, passive exports, style-only modules, and files without meaningful logic.
- Note required wrappers early: router, auth, query client, i18n, feature flags, theme, or form providers.

### 2. Review existing tests

- Check whether current tests still reflect real user-observable behavior.
- Identify gaps in happy paths, boundary cases, error states, retries, empty states, and accessibility-sensitive interactions.
- Rewrite tests only if they are stale, flaky, or overly coupled to implementation details.

### 3. Add or refine tests

- Prioritize behavior in this order: happy path, loading state, error or retry path, empty state, boundary conditions, and business-critical branches.
- Keep one behavior per test.
- For reusable provider setup, add or reuse `renderWithProviders` rather than duplicating wrapper code in every file.
- For networked flows, add or refine MSW handlers instead of replacing the component's data layer with direct function stubs.

### 4. Test-and-fix loop

Repeat up to `{max_iterations}` times:

1. Run the most focused test command available for the changed file or test name.
2. Run the broader unit suite with `pnpm exec vitest run` or the repo's established unit-test script.
3. Run lint with `pnpm exec eslint . --ext .js,.jsx,.ts,.tsx` or the repo's lint script.
4. Fix failing tests and lint issues before adding more coverage.
5. Run coverage with `pnpm exec vitest run --coverage`.
6. Use the coverage report to target missed branches, especially alternate async UI states and failure modes.
7. Stop when tests pass, lint is clean, coverage reaches `{coverage_target}`, or `{max_iterations}` is exhausted.

### 5. Report the result

- Return the standardized summary from the Output section.
- Call out any remaining risks, meaningful coverage gaps, and production-code issues discovered while testing.
- If a requested behavior belongs outside unit scope, say so explicitly and recommend the correct next test level.

## Output

After the final iteration, produce a summary:

| Item | Detail |
| ---- | ------ |
| Modules tested | Source components, hooks, and utilities covered by the run. |
| Test files created or updated | New or modified `*.test.ts(x)` files and shared test helpers. |
| Tests added or changed | Count of new and modified test cases. |
| Coverage | Measured percentage from Vitest coverage, or an estimate with justification. |
| Test status | Final pass and fail counts from the last test run. |
| Lint status | Clean or list of remaining ESLint violations. |
| Remaining coverage gaps | Untested states, branches, or interaction flows still needing coverage. |
| Code issues found | Production bugs, design concerns, or testability refactors discovered. |
| Iterations used and exit reason | Number of iterations consumed and which stop condition ended the run. |

## Error Handling

- If code is hard to unit test because of tight coupling, hidden globals, or provider sprawl, document the smallest design change that would improve testability and describe the lightest acceptable fallback test strategy.
- If testing exposes a production defect, document the expected behavior, actual behavior, impact, and the regression test that reproduces it.
- If environment setup fails, report the exact command, the observed error, and the corrective step taken or recommended.
- If the repo uses a different test layout, coverage provider, or DOM environment than the defaults above, adapt to that convention and explain the tradeoff.
- If a scenario cannot be verified honestly at unit level, say so and recommend a component-integration or E2E test instead of forcing a brittle mock-heavy test.
