# camera-3d-captions

Community workflow for deterministic depth captions around a talking head, combining a person matte, word timings, camera motion and measured font spacing.

**ID:** `heygen-com--camera-3d-captions` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** agent-portable · **Provider scope:** any
**Prerequisites:** node-22-plus, hyperframes-0.8.62, ffmpeg, python3-fonttools-brotli-numpy-pillow, word-level-transcription, licensed-font-files
**Model binding:** not-model-specific

[Pinned upstream SKILL.md](https://github.com/heygen-com/hyperframes-community-skills/blob/ba7a0bb6d3567d124c51f6074625043bfe0b32eb/skills/camera-3d-captions/SKILL.md)
Repository revision: `ba7a0bb6d3567d124c51f6074625043bfe0b32eb`
File SHA-256: `2f5507777cea180934471344a98cd7bfd59444269a09b007a94eb9e5908444e8`
Repository license: Apache-2.0; skill-declared license: not found.

## Before use

- The inspected recipe pins HyperFrames 0.8.62 and is scoped to static-camera medium or wider shots, typically 5–20 seconds. Do not silently upgrade its renderer.
- Requires a usable person-segmentation matte and accurate word timestamps; fine hair, close-ups and moving cameras can break the treatment.
- Matting downloads a local model and preview/render loads GSAP from a CDN. No media upload is described, but the workflow is not fully offline.
- The hand-drawn option additionally requires p5-paint-animation and its setup. Its local-matting backend must be checked on the target platform.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
