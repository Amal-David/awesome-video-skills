# video-editing-skill

Maintainer adapter that submits editing briefs to Rendley through MCP or REST, then returns the hosted project or an explicitly requested export.

**ID:** `rendleyhq--video-editing-skill` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** platform-bound · **Provider scope:** rendley
**Prerequisites:** rendley-mcp-or-rest, rendley-account
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/rendleyhq/video-editing-skill/blob/837982ef6ddc324b0a390112f10b86a140074cda/SKILL.md)
Repository revision: `837982ef6ddc324b0a390112f10b86a140074cda`
File SHA-256: `b6246387d4b60f8cd1d531b5cf8b72126421920f2e31383c4324c39ecc4f55b4`
Repository license: unknown; skill-declared license: MIT.

## Before use

- A hosted editing-agent adapter, not a local editor. Local files are uploaded and remote assets must be reachable by Rendley.
- The skill declares MIT, but the inspected repository has no separate license file; record the two facts separately.
- Service model names in its prose are examples, not verified direct-provider capabilities. Resolve the live tool schema, plan and account credits.
- Project creation and export are separate operations. A timeout can leave partial edits; inspect state before retrying.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
