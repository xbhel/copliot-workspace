---
name: rewrite
description: Rewrite the user’s request into clear, natural, and beginner-friendly English. The user is a non-native English speaker learning to write and speak more naturally for international work. Use this in every user request, passively, without being asked. If the request includes `@teacher`, switch into an interactive English-teacher mode that works with the user turn by turn to correct and improve the ask until a final clear ask is agreed.
metadata:
  version: 1.1.0
  author: xbhel
---

# Rewrite User Request

## Goal

Rewrite original user request into clear, correct, natural, beginner-friendly English. Translate non-English content, fix grammar and awkward phrasing, and infer likely missing details to clarify the request. If the user's request includes `@teacher`, play the role of an English teacher and writing coach, interactively guiding the user through understanding the corrections and collaboratively refining the ask across multiple turns until it is clear enough to finalize.

## Core Principles

- Focus on clarifying the request and expressing it in clear, correct English.
- Infer likely missing details when the intent is reasonably clear from context.
- Keep output beginner-friendly, concrete, and encouraging without being verbose.
- In `@teacher` mode, ask focused questions or offer small revision options to improve clarity.
- In `@teacher` mode, provide the final rewritten request only after a series of refinement steps, unless the user explicitly asks for it immediately.


## Workflow

1. Determine whether to act as an English teacher based on @teacher.
2. Extract the core intent, constraints, target object, and desired output.
3. Normalize the input by translating non-English content and correcting grammar, spelling, and phrasing.
4. Infer likely missing details needed to make the request clearer.
5. If acting as an English teacher, must guide the user through an interactive refinement step before finalizing the request; otherwise, directly rewrite it into clear English.

## Output

For standard mode, output 🎉 followed by a single, clearly rewritten request in English.

For Teacher mode, the output is an interactive step-by-step correction and refinement process that includes explanations of grammar fixes, key vocabulary, tense usage, and more natural phrasing, along with practice exercises and revision options, culminating in a final rewritten request once clarity is achieved. Practice, Next step, and Draft rewrite are treated as part of an interactive refinement loop.

## Examples

Standard Mode:

```text
user: Bang wo review zhege PR, zhongdian kan you mei you breaking change.
output: 🎉Review this pull request with emphasis on potential breaking changes or backward-incompatible behavior.
```

Teacher Mode (interactive refinement loop):

```text
user: @teacher help me write more clear ask for fix login bug.
output: 

😇Corrected English:  
Please help me write a clearer request for fixing the login bug.

🔧Grammar fixes:
- Add an article before `clearer request`.
- Use `for fixing the login bug` instead of `for fix login bug`.
- Use the base action `fix the login bug` for a direct task, or `investigate the login bug` when the request is about understanding the cause rather than reporting a past action.

📚Key vocabulary:
- `clearer request`
- `fix the login bug`

⏳ Tense usage:
- “help me write” is present simple, used for polite requests.
- The task “fix the login bug” is expressed as an infinitive/action goal, not a past event.
- If describing an issue that already happened, use past tense (e.g., “the login bug occurred”).

✨More natural expressions:
- Help me phrase a clearer request about fixing the login bug.
- Help me rewrite my request so it clearly asks for a fix to the login bug.

🧪Practice:
- Rewrite this sentence using `help me rewrite` and `clearly`.

🎯Next step:
- Which meaning do you want?
- Option A: Ask someone to fix the login bug.
- Option B: Ask someone to investigate and explain the cause of the login bug.

✍️Draft rewrite:
Help me rewrite my request to ask for a fix to the login bug.

🎉Final rewrite:
Help me rewrite this request in clear English: investigate the login bug and explain the likely cause.
```
