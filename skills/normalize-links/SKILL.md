---
name: normalize-links
description: Extract links from text and convert them into a consistent markdown link format. Use this skill when links in mixed text need to be extracted and normalized into one markdown format.
metadata: 
  version: 1.0.0
  author: xbhel
---

# Normalize Links

## Goal

Extract links from mixed content (raw URLs, markdown links, or mixed prose) and convert them into a consistent markdown link format:

## When to Use

Use this skill when:

- the input mixes raw URLs, markdown links, or prose with embedded links
- links should be rewritten into one consistent markdown format
- inferred metadata is needed for clean, repeatable reference lists or notes

`[{from}/{author}/{type}/{title}]({url}): {description} #{topic}`

Fields:

- `from`: 2-20 chars, lowercased ASCII, inferred from domain/brand.
- `author`: Optional, 2-20 chars, lowercased ASCII, inferred from domain/brand or content creator.
- `type`: 2-15 chars, lowercased ASCII, inferred from URL path or content. such as `article`, `video`, `repo`, `docs`, `blog`, `news`, `forum`, `wiki`, `industry`, `report` etc.
- `title`: kebab-case, lowercased ASCII, max 60 chars.
- `url`: The URL of the link.
- `description`: concise English summary, max 150 chars, English.
- `topic`: Optional, inferred subject domain and subtopic, formatted as `domain` or `domain/subtopic`. Use `/` to express a subtopic within a domain. Examples: `ai/agent`, `web/springboot`, `bigdata/flink`, `devops/ci`.

## Inputs

|name| description|default|required|source|
|-|-|-|-|-|
|text|text containing raw URL, markdown link, or mixed prose with links.| |Yes|user or upstream|

## Core Principles 

- When `author` and `from` are the same, only include `from` to avoid redundancy.

## Output

Output one normalized link per detected URL and nothing else.

## Examples

URL:
- Input: https://github.com/punkpeye/awesome-mcp-servers
- Output: [github/punkpeye/repo/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers): A collection of excellent MCP servers. #ai/agent

Markdown link:
- Input: [The State of MCP in 2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- Output: [glama/blog/the-state-of-mcp-in-2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025): An analysis predicting or discussing the state and trends of MCP by 2025. #ai/mcp
