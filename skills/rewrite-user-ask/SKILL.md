---
name: rewrite-user-ask
description: Rewrite the user’s request into clear, natural, and correct English, producing a refined ask before any downstream action. Apply this when the input is non-English, mixed-language, grammatically incorrect, telegraphic (e.g., “can fix this?”, “make function return unique sorted”), or vague/underspecified. Skip only for fluent, unambiguous English restatements. If the request includes `#teacher`, switch into a beginner-friendly interactive English-teacher mode that works with the user turn by turn to correct and improve the ask until a final clear ask is agreed.
metadata:
  version: 1.1.0
  author: xbhel
---

# Rewrite User Ask

## Goal

Rewrite `{user_ask}` into clear, correct, natural English before any downstream action.

## When to Use

Use this skill as a global pre-processing step before any downstream action.

Do NOT use this skill when `{user_ask}` is already clear, grammatically correct, and actionable without refinement.

## Inputs

| name | description | default | required | source | allowed values | example |
| ---- | ----------- | ------- | -------- | ------ | -------------- | ------- |
| user_ask | Original user request to translate, normalize, and rewrite. | None | Yes | user or upstream | Any natural-language request | `Bang wo zongjie zhege PR` |
| mode | Response mode inferred from `{user_ask}`. | `standard` | No | derived | `standard`, `teacher` | `teacher` |

## Context

- The user may be learning English. Translation quality and concise phrasing matter.
- `standard` mode is non-interactive and inference-first.
- `teacher` mode is interactive and collaborative.

## Core Principles

- `mode` MUST be `teacher` when `{user_ask}` explicitly contains `#teacher`.
- MUST improve the ask first and MUST NOT jump directly into solving the underlying task.
- ALWAYS output a corrected English rendering of `{user_ask}` first.
- ALWAYS translate non-English content into natural English.
- ALWAYS repair grammar, word choice, and awkward phrasing when the input is already partly in English.
- NEVER trigger this skill for asks that are already clear, correct, and specific enough to execute directly.
- ALWAYS infer likely missing details when the intent is recoverable from context.
- In `standard` mode, NEVER ask the user follow-up clarification questions inside this skill.
- NEVER preserve obvious ambiguity when a reasonable inference can make the ask more actionable.
- NEVER over-expand the ask with speculative requirements that are not supported by `{user_ask}`.
- When the request is too ambiguous to resolve perfectly, MUST provide the best inferred ask and MUST state the assumptions briefly.
- In `teacher` mode, MUST be beginner-friendly, concrete, and encouraging without becoming verbose.
- In `teacher` mode, MUST interact with the user to correct and improve the ask instead of finalizing everything in one response.
- In `teacher` mode, MUST ask focused questions or offer small revision choices when user input is needed to make the ask truly clear.
- In `teacher` mode, MUST end with a final rewritten ask only after at least one collaborative correction step, unless the user explicitly asks for the final version immediately.

## Workflow

1. Read `{user_ask}` and detect whether `#teacher` is present.
2. Extract the core intent, constraints, target object, and desired output.
3. Translate non-English text into natural English.
4. Correct grammar, spelling, and phrasing errors.
5. Infer missing but likely details needed to make the ask clearer.
6. If `mode` is `standard`, rewrite the ask into a concise, executable English request while preserving the original meaning.
7. If `mode` is `teacher`, explain the corrections, including tense usage, highlight important vocabulary, and guide the user through a short interactive refinement step.
8. In `teacher` mode, continue refining across turns until the ask is clear enough to finalize.

## Output

For `standard` mode, use this structure:

```markdown
Corrected English:
[A faithful English rendering of the original ask]

Rewritten Ask:
[A clearer, more concise, more actionable English ask]

Assumptions:
[Omit when unnecessary. Otherwise list only the key inferred assumptions.]
```

For `teacher` mode, every response shares this base structure:

```markdown
Corrected English:
[A faithful English rendering of the original ask]

Grammar Fixes:
- [Short explanation of the important grammar corrections]
- [Explain important tense choices when relevant]

Key Words and Phrases:
- [Important vocabulary, collocation, or fixed expression]

More Natural Ways to Say It:
- [One or two more idiomatic alternatives]
```

During the interactive refinement loop, append:

```markdown
Practice:
- [Optional short exercise only when the mistakes justify it]

Next Step:
- [One concise question or 2-3 short revision options that help the user improve the ask]

Draft Rewritten Ask:
[A provisional improved version to react to]
```

For the final `teacher` mode response, once the ask is converged, append instead:

```markdown
Rewritten Ask:
[The final clear English ask]
```

## Error Handling

- If `{user_ask}` mixes languages, normalize everything into one coherent English ask.
- If the original wording is extremely sparse, infer the most likely meaning and note the assumption briefly.
- In `teacher` mode, if the ask is underspecified, ask the smallest useful follow-up needed to help the user improve it.

## Examples

Example 1:

Input:
`Bang wo review zhege PR, zhongdian kan you mei you breaking change`

Output:

```markdown
Corrected English:
Please review this pull request and focus on whether it introduces any breaking changes.

Rewritten Ask:
Review this pull request with emphasis on potential breaking changes or backward-incompatible behavior.
```

Example 2:

Input:
`#teacher help me write more clear ask for fix login bug`

Output:

```markdown
Corrected English:
Please help me write a clearer request for fixing the login bug.

Grammar Fixes:
- Add an article before `clearer request`.
- Use `for fixing the login bug` instead of `for fix login bug`.
- Use the base action `fix the login bug` for a direct task, or `investigate the login bug` when the request is about understanding the cause rather than reporting a past action.

Key Words and Phrases:
- `clearer request`
- `fix the login bug`

More Natural Ways to Say It:
- Help me phrase a clearer request about fixing the login bug.
- Help me rewrite my request so it clearly asks for a fix to the login bug.

Practice:
- Rewrite this sentence using `help me rewrite` and `clearly`.

Next Step:
- Which meaning do you want?
- Option A: Ask someone to fix the login bug.
- Option B: Ask someone to investigate and explain the cause of the login bug.

Draft Rewritten Ask:
Help me rewrite this request in clear English: investigate the login bug and explain the likely cause.
```
