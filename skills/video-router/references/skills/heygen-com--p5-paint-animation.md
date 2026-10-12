# p5-paint-animation

Community code-rendering workflow for handwriting, brushstroke photo reveals and short painted-video loops using p5.brush and a seeded stroke layout.

**ID:** `heygen-com--p5-paint-animation` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** agent-portable · **Provider scope:** any
**Prerequisites:** node-22.12-plus, ffmpeg, puppeteer, p5, p5.brush
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/heygen-com/hyperframes-community-skills/blob/ba7a0bb6d3567d124c51f6074625043bfe0b32eb/skills/p5-paint-animation/SKILL.md)
Repository revision: `ba7a0bb6d3567d124c51f6074625043bfe0b32eb`
File SHA-256: `5590180ff81dd7a6c9cf92c141d6d0600d23dba596043e5fb0d3113c73a77b8c`
Repository license: Apache-2.0; skill-declared license: not found.

## Before use

- This is an offline render recipe, not a generative video model, live web animation or an exact-typography workflow.
- The author scopes video repainting to short clips of about ten seconds because each output frame is expensive; runtime and quality claims are not benchmarked here.
- Setup downloads pinned browser and npm dependencies. p5 is LGPL-2.1 and p5.brush is MIT; review these separately from the skill repository license.
- Optional subject matting uses a separate HyperFrames local backend; camera tracking is translation-only and fast zooms can drift.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
