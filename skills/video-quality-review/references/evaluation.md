# Evaluate a video workflow before calling it better

A skill can follow every instruction and still deliver a poor film. It can also produce an appealing clip while losing required references, overspending or making an editable project impossible to revise. Evaluate the production process and the finished artifact separately.

## What the research contributes

| Primary source | Useful idea | How this repository applies it |
| --- | --- | --- |
| [VideoWeaver](https://github.com/JianhuiWei7/VideoWeaver/tree/cf9990f49a9203c01f2f2a75649e4c92d643e183) and its [paper](https://arxiv.org/abs/2606.08091) | Separate atomic media tools from composition skills, and inspect both traces and outputs. | Keep model/renderer selection distinct from workflow knowledge; retain intermediate artifacts and inspect the source of a failure. |
| [VideoWeaver process evaluation](https://github.com/JianhuiWei7/VideoWeaver/blob/cf9990f49a9203c01f2f2a75649e4c92d643e183/skills/process-eval/SKILL.md) | Review planning, input preparation, reference use, errors and assembly. | Require evidence for process claims. A successful tool invocation is not an output-quality score. |
| [VideoWeaver output evaluation](https://github.com/JianhuiWei7/VideoWeaver/blob/cf9990f49a9203c01f2f2a75649e4c92d643e183/skills/output-eval/SKILL.md) | Reuse metadata, transcripts and visual/audio inspection while scoring individual requirements. | Use inexpensive checks first, then inspect suspicious intervals. Sparse frame grids do not prove temporal quality. |
| [VISTA](https://g-vista.github.io/) | Compare candidate videos, obtain separate visual/audio/context critiques, and revise the prompt iteratively. | Keep a baseline, revise a diagnosed failure and bound the number of attempts. Treat this as a method to evaluate, not a promised improvement. |

These are research references and original operating recommendations. This project has not reproduced the papers' benchmarks. VideoWeaver's inspected repository did not expose a license file; its catalog entries link source for review without bundling or granting reuse rights. Its own rubric formats and sibling skills require the research workspace.

## A practical comparison protocol

### 1. Freeze the brief and acceptance checks

Write down the input assets, exact copy, intended audience, required actions, output format and editable-source requirements before running either workflow. Separate fixed constraints from creative choices. Keep a copy of the original brief so later prompt refinement cannot quietly weaken it.

Choose representative cases for the intended use. An app-launch skill needs real UI, legible copy and repeatable brand styling; a long-form story needs continuity across shots; a dubbing skill needs intelligible, faithful speech. Include at least one difficult case and reserve additional cases for checking a revision. Avoid claiming broad success from the example used to write the skill.

### 2. Preserve a comparable baseline

Use the same inputs, provider operation, output target and authorized resource ceiling. Record the controller and skill revisions separately from renderer/model versions. If a provider exposes a seed, retain it; do not assume a seed makes two different models directly comparable.

Count every attempt, including failed jobs, discarded clips and manual fixes. Report elapsed time, generation attempts, actual billed cost where available, and the amount of editable work delivered. A better-looking result produced with many more retries is a useful result only when that tradeoff is explicit.

### 3. Score process and output independently

| Dimension | Process evidence | Final artifact evidence |
| --- | --- | --- |
| Brief fidelity | Required actions and exact copy in the shot plan | The requested action occurs and the copy is readable and correct. |
| Reference handling | Asset IDs and the exact reference roles submitted | Identity, product appearance and relevant scene details remain faithful. |
| Motion and continuity | Shot order, timing, transition and revision records | Full playback shows complete actions and coherent cuts. |
| Audio | Voice/music sources, transcript and audio-layer edits | Listening confirms intelligibility, timing and usable transitions. |
| Technical delivery | Renderer options and finishing commands | Probe the encoded file; inspect dimensions, duration, streams and requested color/alpha behavior. |
| Editability | Source project, named assets and editable scene structure | Make a small requested revision without rebuilding the entire piece. |

Use `pass`, `partial`, `fail` or `not_observed` per acceptance check. Retain the observation and its timestamp or artifact path. Do not average away a failed hard constraint such as incorrect numbers, missing dialogue or the wrong required format. Leave a dimension `not_observed` when the reviewer lacks the needed playback, hearing or source access.

### 4. Diagnose the failing stage

Classify the failure before changing instructions: brief interpretation, source preparation, unsupported operation, prompt/action design, generation, timing/compositing, audio, export or review. Patch the smallest stage that explains the evidence. Preserve successful shots and assets when the problem is local.

A frame grid can locate a suspicious interval; watch that interval to evaluate motion. A transcript can find missing words; listen to assess delivery and synchronization. A metadata check can reject the wrong format; it cannot prove that a shot looks good.

### 5. Re-evaluate the revision

Keep the previous result and compare the revision against the unchanged brief. Where practical, hide candidate labels from the reviewer and vary their presentation order. Check the reserved cases as well as the motivating failure. Record regressions, reviewer disagreements and differences in cost or attempts.

Promote the revised skill only when its intended improvement survives those checks. Keep the evidence and an easy way to return to the prior version. Stop when the acceptance checks are met, the authorized resources are exhausted, or further revisions lack a concrete diagnosis.

## Report the result accurately

An evaluation report should identify the brief, skill/controller/backend versions, inputs, outputs, attempts, resource usage, individual checks, unobserved dimensions and the reason for any revision. Use the original [example record](https://github.com/Amal-David/awesome-video-skills/blob/main/examples/evaluation-record.json) as a starting point; it is a reporting template, not a completed benchmark or a request for the routing CLI.

Keep three kinds of verification separate: catalog tests verify routing logic, source pins verify file identity, and actual rendered-video evaluation measures the workflow's delivered result. Improvements to the first two do not establish a measured quality gain in the third.
