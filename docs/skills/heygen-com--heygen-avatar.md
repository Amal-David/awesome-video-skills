# heygen-avatar

Maintainer workflow for creating a reusable presenter identity from a description or supplied photo, selecting a voice and saving the HeyGen identity for later videos.

**ID:** `heygen-com--heygen-avatar` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** platform-bound · **Provider scope:** heygen
**Prerequisites:** heygen-mcp-or-cli, heygen-account
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/heygen-com/skills/blob/1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a/heygen-avatar/SKILL.md)
Repository revision: `1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a`
File SHA-256: `9f27d6d1724143a5a07c7535c509a8bef2be5ba2c69daf834bdd9b6c74794eba`
Repository license: MIT; skill-declared license: not found.

## Before use

- Identity setup returns reusable avatar and voice identifiers; it does not itself produce a finished video.
- Photo uploads and generation use HeyGen services and account credits. The CLI feedback step can transmit a task description; follow the host privacy and telemetry policy.
- Confirm the installed MCP or CLI schema and supported v3 operations; do not infer endpoint availability from the skill alone.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
