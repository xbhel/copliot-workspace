---
name: analyze-words
description: Analyze words and provide pronunciation, part of speech, beginner-friendly meanings, morphology, common phrases, and example sentences.
metadata: 
  version: 1.0.0
  author: xbhel
  tags: [word analysis, linguistics, language learning]
---

## Goal

Given one or more words, analyze each word and present a short, beginner-friendly explanation in a consistent markdown format.

For each word, include:

- `word`: The original word.
- `pronunciation`: IPA, if available.
- `part_of_speech`: The main grammatical category, such as noun, verb, adjective, or adverb.
- `meanings`: Up to 3 simple English meanings.
- `morphology`: A simple word breakdown when useful, including:
  - `prefixes`: Optional.
  - `root`: Required when a meaningful root can be identified.
  - `suffixes`: Optional.
- `common_phrases`: Up to 3 common phrases or collocations.
- `example_sentences`: Up to 3 short English example sentences, max 30 characters each.

## Inputs

|name| description|default|required|source|
|-|-|-|-|-|
|words|A list of words to analyze.| |Yes|user or upstream|

## Output

Return one section per word using this format:

```markdown
**{word}** /{pronunciation}/

{part_of_speech}. {meaning 1}
{optional meaning 2}
{optional meaning 3}

{morphology}
- prefixes: {prefix explanation if any}
- root: {root explanation}
- suffixes: {suffix explanation if any}

Phrases:
- {phrase 1}
- {phrase 2}
- {phrase 3}

Sentences:
- {sentence 1}
- {sentence 2}
- {sentence 3}
```

When multiple words are provided, separate each word block with `---`.

## Core Principles

- Use simple, beginner-friendly English.
- Prefer common usage over rare or technical meanings.
- Keep each explanation concise and practical.
- Include morphology only when it helps understanding.
- If morphology is unclear or not useful, keep it simple rather than forcing an analysis.
- Prefer English explanations and examples unless the user asks for another language.

## Workflow

1. Identify the word and its most common part of speech.
2. Provide up to 3 common meanings in simple English.
3. Add a useful morphology breakdown when possible.
4. Add up to 3 common phrases.
5. Add up to 3 short example sentences.
6. If multiple words are given, repeat the format for each word and separate sections with `---`.

## Error Handling

- If pronunciation is uncertain, omit it rather than guessing.
- If a word has multiple parts of speech, prioritize the most common one unless the user asks for more detail.
- If morphology is not meaningful, use a minimal breakdown or omit optional parts.
- If the input is not a valid word, say so briefly and do not invent meanings.

## Examples

Single word:

- Input: inevitably
- Output:
```markdown
**inevitably** /ɪˈnevɪtəbli/

adv. in a way that is certain to happen.
adv. in a way that cannot be avoided.

in + evitab(le) + ly
- prefixes: in = not
- root: avoidable = able to be avoided
- suffixes: ly = makes an adverb

Phrases:
- inevitably lead to
- inevitably result in
- almost inevitably

Sentences:
- This will inevitably lead to problems.
- Hard work will inevitably improve your skills.
- When costs rise, prices inevitably increase.
```

Multiple words:

- Input: happy, unhappy
- Output:
```markdown
**happy** /ˈhæpi/

adj. feeling pleased or satisfied.

...(other fields for "happy")

---

**unhappy** /ʌnˈhæpi/

adj. not happy; feeling sad or upset.

...(other fields for "unhappy")
```
