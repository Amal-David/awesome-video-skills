# Runway: choose generation, editing or performance capture

Runway Dev is a provider with several distinct video contracts. Select a specific model and operation before preparing assets. The curated surfaces here cover **Gen-4.5 creation** and **Aleph 2.0 editing**. The [current provider index](https://docs.dev.runwayml.com/guides/models/) lists additional models; that does not give this guide or an upstream skill access to them.

## Covered surfaces

| Surface | API model ID | Operation | Required media | Verified duration |
| --- | --- | --- | --- | --- |
| `runway-gen-4-5` | `gen4.5` | `/v1/text_to_video` or `/v1/image_to_video` | Prompt; a first image for image mode | Whole seconds from 2–10 |
| `runway-aleph-2` | `aleph2` | `/v1/video_to_video` | Source video; optional timed guidance images | Source video from 2–30 seconds |

Gen-4.5's [model launch](https://runway.com/research/introducing-runway-gen-4.5) was December 1, 2025. Its February 10, 2026 API availability is a separate event. Aleph 2.0's recorded June 2, 2026 date is **provider availability**, not an inferred model launch. Runway's [changelog](https://docs.dev.runwayml.com/api-details/api_changelog/) also records the July 30 removal of `gen4_aleph` and `gen3a_turbo`. Old snippets using those IDs need migration.

## Gen-4.5: new footage from a prompt or opening image

The [pinned text contract](https://github.com/runwayml/sdk-python/blob/91703c372f3041f4ca0426417628d91a62e78e70/src/runwayml/types/text_to_video_create_params.py) accepts `1280:720` or `720:1280`. The [pinned image contract](https://github.com/runwayml/sdk-python/blob/91703c372f3041f4ca0426417628d91a62e78e70/src/runwayml/types/image_to_video_create_params.py) accepts these dimensions:

| Mode | Allowed `ratio` values |
| --- | --- |
| Text to video | `1280:720`, `720:1280` |
| Image to video | `1280:720`, `720:1280`, `1104:832`, `960:960`, `832:1104`, `1584:672` |

These are output dimensions, not interchangeable aspect-ratio strings. The router records the [nominal 720p tier](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5) and does not validate this dimension matrix. Validate the actual request against the selected operation before submission. The creator guide describes web settings; its frame-rate selector is not established by the inspected API contracts.

`promptImage` in the inspected image contract accepts an opening image, with `position: "first"` in its structured form. It does not expose last-frame control. Route a required first/last transition to another verified surface. The inspected Gen-4.5 contracts do not establish native generated audio; keep an audio requirement unresolved rather than inferring it from another Runway-hosted model.

Write the shot as observable action, camera movement and timing. For image mode, use the image to establish appearance and write the motion that follows. Both contracts cap the prompt at 1,000 UTF-16 code units. Begin with one representative shot, inspect it, then adjust the specific visual or timing problem. Exact brand typography and charts belong in a procedural finishing stage.

## Aleph 2.0: edit or expand an existing shot

Use `videoUri` to supply the source clip. The [pinned edit contract](https://github.com/runwayml/sdk-python/blob/91703c372f3041f4ca0426417628d91a62e78e70/src/runwayml/types/video_to_video_create_params.py) accepts up to five timed keyframes. Each provides an image URI and a location in the source timeline; it is not a loose image-reference list. When the router receives `reference_images` for this surface, interpret that count as guidance keyframes during preflight.

Describe the intended change and what needs to remain stable. For a product replacement, prepare a guidance image with the desired product at the matching timestamp and inspect the object's boundaries throughout the edit. If using edit windows, all keyframes must supply a window or none may; each timestamp must fall inside its own window. Check those constraints in the provider request because the offline router does not model timestamps.

For expansion, use the edit contract's `targetAspectRatio` control. This covers generative outpainting of the source canvas. It is a separate operation from generating a new shot or extending its running time. API resolution and frame-rate limits remain unrecorded here; do not copy the web application's input limits into this provider contract.

## Delivery formats need their own checks

Runway's [professional output guide](https://docs.dev.runwayml.com/guides/professional-outputs/) distinguishes Gen-4.5 HDR generation from Aleph SDR editing. An Aleph edit requires a separate Ruby conversion for HDR delivery. EXR output alone does not establish an HDR input roundtrip, so neither surface claims the catalog's `exr-hdr-roundtrip` capability.

ProRes 4444 output also does not establish useful transparency: the inspected Aleph contract specifies an opaque alpha plane. Keep `alpha-output` requests rejected on this surface. Check output-format access and any additional charges before execution, then inspect the downloaded codec, pixel format, color metadata, duration and sound along with actual playback.

## Performance capture remains a separate follow-up

Runway's [Act-Two contract](https://github.com/runwayml/sdk-python/blob/91703c372f3041f4ca0426417628d91a62e78e70/src/runwayml/types/character_performance_create_params.py) requires a 3–30 second performance video plus a character image or video with a visible face. It transfers a performance; it is not a prompt-only generation endpoint. This pass does not add an automatic Act-Two route because the request schema does not yet express those distinct required inputs.

## Execution checklist

1. Choose the exact provider model and operation. Read the current schema and confirm account access.
2. Check source ownership, upload format, dimensions, duration, guidance timing and the output-format cost.
3. Record the request, model ID, SDK/API version, asset identifiers and returned task ID. Inspect a pending task before retrying a submission.
4. Review playback and technical metadata before delivering or composing the shot into a longer video.

Evidence reviewed on 2026-10-12. The SDK references are pinned to `91703c372f3041f4ca0426417628d91a62e78e70`. This is static contract review; no generation, editing or account-access test was performed.
