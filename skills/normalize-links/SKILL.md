---
name: normalize-links
description: Extract links from text and convert them into a consistent markdown link format.
metadata: 
  version: 1.0.0
  author: xbhel
  tags: [link, normalization, url, markdown]
---

# Normalize Links

## Goal

Extract links from mixed content (raw URLs, markdown links, or mixed prose) and convert them into a consistent markdown link format:

## When to Use This Skill

Use this skill when:

- the input contains raw URLs, markdown links, or prose with embedded links that need normalization
- the user wants links rewritten into one consistent markdown format with inferred metadata
- you need clean, repeatable link formatting for notes, reading lists, or reference documents

`[{from}/{author}/{type}/{title}]({url}): {description}`

Fields:

- `from`: 2-20 chars, lowercased ASCII, inferred from domain/brand.
- `author`: Optional, 2-20 chars, lowercased ASCII, inferred from domain/brand or content creator.
- `type`: 2-15 chars, lowercased ASCII, inferred from URL path or content. such as `article`, `video`, `repo`, `docs`, `blog`, `news`, `forum`, `wiki`, `industry`, `report` etc.
- `title`: kebab-case, lowercased ASCII, max 60 chars.
- `url`: The URL of the link.
- `description`: concise English summary, max 150 chars, English. 

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
- Output: [github/punkpeye/repo/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers): A collection of excellent MCP servers.

Markdown link:
- Input: [The State of MCP in 2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- Output: [glama/blog/the-state-of-mcp-in-2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025): An analysis predicting or discussing the state and trends of MCP by 2025.
