---
name: link-builder
description: Extract links from text and convert them into a consistent markdown link format.
metadata: 
  version: 1.0.0
  tags: [link, normalization, url, markdown]
---

## Goal

Extract links from mixed content (raw URLs, markdown links, or mixed prose) and convert them into a consistent markdown link format: `[{from}/{type}/{title}]({url}): {description}`

Fields:

- `from`: 2-10 chars, lowercased ASCII, inferred from domain/brand.
- `type`: 2-10 chars, lowercased ASCII, inferred from URL path or content. such as `article`, `video`, `repo`, `docs`, `blog`, `news`, `forum`, `wiki`, `industry`, `report` etc.
- `title`: kebab-case, lowercased ASCII, max 50 chars.
- `url`: The URL of the link.
- `description`: concise English summary, max 100 chars, English. 

## Inputs

|name| description|default|required|source|
|-|-|-|-|-|
|text|text containing raw URL, markdown link, or mixed prose with links.| |Yes|user or upstream|

## Output

Output one normalized link per detected URL and nothing else.

## Examples

Example 1:
- Input: https://github.com/punkpeye/awesome-mcp-servers
- Output: [github/repo/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers): A collection of excellent MCP servers.

Example 2:
- Input: [The State of MCP in 2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- Output: [glama/blog/the-state-of-mcp-in-2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025): An analysis predicting or discussing the state and trends of MCP by 2025.
