# video-editing

Community HyperFrames standard for short-form edits: supplied script and media, themed layouts, eased camera moves, captions, sound effects and a bundled ffprobe export gate.

**ID:** `nopefallacy--video-editing` · **Tier:** review-required
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** agent-portable · **Provider scope:** any
**Prerequisites:** node, hyperframes, ffmpeg, ffprobe, approved-script-and-media, style-pack
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/nopefallacy/vertical-video-editing-skills/blob/8de3a875a7856dba658027a8f64a6bdfe9800b9e/skills/video-editing/SKILL.md)
Repository revision: `8de3a875a7856dba658027a8f64a6bdfe9800b9e`
File SHA-256: `a2e6b58b6be1a9bf49180cb523e3970efa7ea93c44cdb1ab0b1ce42afbf98928`
Repository license: MIT; skill-declared license: not found.

## Before use

- Defaults to 1080×1920 vertical shorts; other aspect ratios require explicit style and verification settings.
- The June recipe contains version-sensitive overlap and multi-track audio workarounds. Reconcile them with the installed HyperFrames core/audio contract before use.
- A clean ffprobe gate and sampled frames do not prove smooth motion or audible synchronization; review full encoded playback.
- Its creator-quality and anti-jitter claims are author guidance rather than benchmarks measured by this repository.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
