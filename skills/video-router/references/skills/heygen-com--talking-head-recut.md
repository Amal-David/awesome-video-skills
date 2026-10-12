# talking-head-recut

Adds transcript-timed graphic cards to an existing talking-head video while the full source clip plays untouched; this workflow does not perform a transcript cut.

**ID:** `heygen-com--talking-head-recut` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** agent-portable · **Provider scope:** any
**Prerequisites:** node-22-plus, hyperframes, ffmpeg
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/heygen-com/hyperframes/blob/86521b94f592bcf0ca86aba63068893cf658af16/skills/talking-head-recut/SKILL.md)
Repository revision: `86521b94f592bcf0ca86aba63068893cf658af16`
File SHA-256: `d1c5138cb05ce27f123f414aa2ef1404098d08eb8f056fe95f3425b917bc61ff`
Repository license: Apache-2.0; skill-declared license: not found.

## Before use

- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.
- The standalone updater follows upstream main; versioned plugin installs should update through their plugin manager. Pin the renderer separately from this skill revision.
- The full input clip remains untouched. Removing pauses, reordering speech or shortening the source requires a different editing workflow.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
