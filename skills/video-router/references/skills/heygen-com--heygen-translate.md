# heygen-translate

Maintainer workflow for dubbing existing video, choosing lip-sync or audio-only output and reviewing translated subtitles before the final render.

**ID:** `heygen-com--heygen-translate` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** platform-bound · **Provider scope:** heygen
**Prerequisites:** heygen-mcp-or-cli, heygen-account, source-video
**Model binding:** provider-workflow; exact endpoint preflight required

[Pinned upstream SKILL.md](https://github.com/heygen-com/skills/blob/1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a/heygen-translate/SKILL.md)
Repository revision: `1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a`
File SHA-256: `d4b1d860abf2dfee6c28598e3c290c43b45d7a8f9a4263b3510edd27e99bffc0`
Repository license: MIT; skill-declared license: not found.

## Before use

- Requires an existing recording. Source-language text burned into the video is not removed by translating the audio.
- The inspected skill exposes single-language translation through MCP but sends batch translation and proofreads through CLI; confirm the current tool surface.
- Dynamic-duration translation can change the clip length and requires retiming downstream edits.
- Upstream asks for API keys in chat and a CLI feedback submission; use secure credential setup and the host privacy policy instead. Media processing uses a hosted paid service.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
