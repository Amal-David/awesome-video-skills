# Practical video workflow recipes

Choose the output first, then the operation and skill. These stacks are curation recommendations grounded in the linked upstream instructions. They are not benchmark rankings, and the CLI plans work without installing or executing those upstream skills.

## App launch or exact UI motion

Route code motion when the app screen, numbers, text and layout need to remain correct and editable:

```bash
python3 scripts/avs.py route --task motion --agent astra --engine remotion
python3 scripts/avs.py route --task motion --engine hyperframes
```

Start with the maintainer's [Remotion create](skills/remotion-dev--remotion-create.md) or [HyperFrames router](skills/heygen-com--hyperframes.md), then load the narrower launch or motion skill. With Remotion, plan independently editable scenes as separate source nodes. With HyperFrames, preserve seekable motion and inspect the encoded result as well as the browser preview. See [motion guidance](motion.md).

For a launch containing generated footage, use a hybrid request:

```bash
python3 scripts/avs.py route --task hybrid --duration 8 --require exact-text
```

Here `duration` means one generated shot. The assembled film can be longer. Global privacy and runtime constraints apply to both stages; the final stage supplies exact copy and branding.

## A researched explainer

Inspect [collage explainer](skills/heygen-com--vox-explainer.md) when the deliverable needs researched sources, narration and designed motion. Read [faceless explainer](skills/heygen-com--faceless-explainer.md) for the corresponding maintained HyperFrames workflow.

Gather the evidence and write the narrative before buying generated footage. Establish narration and word timings, assemble a small visual sample, then build and inspect each scene. Verify factual claims independently of visual polish. A numerical transition check can catch a seam; it does not validate the underlying story.

## Captions, overlays or a shorter recording

| Intended change | Skill to inspect | What still needs checking |
| --- | --- | --- |
| Display the actual spoken words | [Embedded captions](skills/heygen-com--embedded-captions.md) | Accurate words and timing, readable sizes, and existing burned-in subtitles. |
| Add graphic cards while retaining the whole take | [Talking-head graphic treatment](skills/heygen-com--talking-head-recut.md) | The upstream `talking-head-recut` preserves the source duration and speech. |
| Add depth captions around a person | [Camera 3D captions](skills/heygen-com--camera-3d-captions.md) | The recipe's pinned renderer, usable person matte, suitable camera framing and word timings. |
| Remove pauses or rearrange an edit | [Rendley adapter](skills/rendleyhq--video-editing-skill.md) or an adopted timeline editor | Source uploads, retained meaning, edited timing and the service's current operations. |

Do not select an overlay workflow on the assumption that its name promises transcript cutting. The [vertical editing candidate](skills/nopefallacy--video-editing.md) remains `review-required` because its older renderer workarounds need reconciliation with current releases.

## Presenters and translation

Use [HeyGen avatar](skills/heygen-com--heygen-avatar.md) to establish the identity and voice, then [HeyGen video](skills/heygen-com--heygen-video.md) for presenter-led production. Identity creation alone does not deliver the finished video.

For an existing recording in another language, inspect [HeyGen translate](skills/heygen-com--heygen-translate.md). Preserve the distinction between dubbing, lip-sync treatment and audio-only translation. Review translated subtitles and named entities. Check whether a changed delivery duration requires downstream retiming; translated audio does not erase text already burned into the source.

These are discoverable provider workflows, not approved automatic HeyGen model routes. Read their skill cards and live MCP/CLI contracts.

## Paint a short clip or animate a photograph

Inspect [p5 paint animation](skills/heygen-com--p5-paint-animation.md) for seeded brushstroke reveals, handwriting and short repainted clips. This uses code and browser rendering. Check its browser/runtime pins and the p5/component licenses separately. Budget for rendering every frame; do not assume a ten-second technique scales cheaply to a full film.

## Create or edit a shot with Runway

```bash
python3 scripts/avs.py route --task generate --model gen4.5 --duration 8
python3 scripts/avs.py route --task edit --model aleph2 --reference-images 3
python3 scripts/avs.py route --task outpaint --model aleph2
```

Read the [Runway guide](models/runway.md) and [official API transport](skills/runwayml--use-runway-api.md). Gen-4.5 creates footage from a prompt or opening frame. Aleph 2.0 needs a source clip and can use timed guidance images. The source clip and keyframe timestamps remain provider-preflight inputs; the CLI does not upload them.

An outpaint request expands the canvas. It does not ask for a temporal continuation. Preserve model-specific format restrictions and inspect the transport's retry behavior before a paid submission.

## Assemble and evaluate a longer piece

The selected [VideoWeaver processing and evaluation skills](evaluation.md) expose a useful split between media operations, composition knowledge and evaluation. Its [merge-video](skills/jianhuiwei7--merge-video.md) entry documents normalization and center-cropping; [video-shot-split](skills/jianhuiwei7--video-shot-split.md) helps locate scenes. Both need their own dependency and output checks.

Use [process evaluation](skills/jianhuiwei7--process-eval.md) to investigate how a result was produced, and [output evaluation](skills/jianhuiwei7--output-eval.md) to inspect the finished artifact. These are research-workspace skills with unresolved repository licensing, not drop-in hosted generators. Follow the original [evaluation protocol](evaluation.md) to compare a baseline and revision without treating a valid MP4 as sufficient evidence of quality.
