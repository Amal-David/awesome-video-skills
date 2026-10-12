# heygen-video

Maintainer workflow for presenter-led videos through HeyGen Video Agent v3, with avatar and voice resolution, framing checks, script review and a session link for iteration.

**ID:** `heygen-com--heygen-video` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** platform-bound · **Provider scope:** heygen
**Prerequisites:** heygen-mcp-or-cli, heygen-account
**Model binding:** provider-workflow; exact endpoint preflight required

[Pinned upstream SKILL.md](https://github.com/heygen-com/skills/blob/1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a/heygen-video/SKILL.md)
Repository revision: `1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a`
File SHA-256: `ba73aa1e0a5c6584cc7314ecbd592f9043f24705e860f297bd2cf0e9b4751d18`
Repository license: MIT; skill-declared license: not found.

## Before use

- Designed for presenter-led material, not general cinematic B-roll, streaming avatars or video translation.
- Uses a hosted service and plan credits. Duration is a requested target to check on the returned file, not a frame-accurate guarantee.
- The optional OpenClaw generation surface does not replace MCP or CLI avatar and voice discovery. Preserve the actual transport and job identifiers.
- CLI feedback may send a task description; apply the host privacy policy rather than reporting private content automatically.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
