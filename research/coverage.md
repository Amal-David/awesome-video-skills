# Research coverage and limitations

Snapshot: **October 1, 2026**. Preferred model-release window: **April 1–October 1, 2026**. This is a broad, source-backed curation, not a census of every model, social post or skill directory.

| Surface | How it was used | Limitation |
| --- | --- | --- |
| GitHub | Inspect repository trees, SKILL paths, frontmatter, licenses and selected instruction bodies; pin revisions and content hashes. | 193 selected paths across 41 repositories are not all deeply audited or runtime-tested. |
| Model/provider documentation | Resolve actual versions, modes, output constraints, release evidence and backend differences. | Documentation can conflict or lag account rollout; live preflight is still required. |
| Hacker News | Discover creator projects, integrations and practical critiques through representative threads and search-visible thread text. | Not every comment or linked demo was inspected. |
| X/Twitter | Follow creator/demo leads through accessible references and roundups, then verify projects on GitHub. | Direct original-post access was incomplete. Linked or secondary-only evidence is labeled. |
| Reddit | Search for practical video/motion reports and inspect accessible search/secondary references. | Direct thread/video access was incomplete; secondary reports are not promoted into capability evidence. |
| Skill directories | Find candidate repositories and specialized packs, then inspect the upstream source. | Directory descriptions, popularity and claimed benchmarks are not treated as proof. |

## Representative discovery trail

See [discovery.json](discovery.json) for stable links and access status. HN leads included Hyperframes, Cartoon Studio and RxFilm; these were followed to the actual repositories. Motion-focused directories and Opus 5.5 roundups led to code-animation packs, including Charlie’s 13-skill collection. MiniMax’s own repository exposed an important split between a portable prompt skill and MiniMax Hub-only production workflows.

Primary endpoint/model evidence is in [sources.json](../registry/sources.json). Individual upstream cards carry immutable GitHub links, revision, file hash, license observations and review level. No upstream skill bodies, videos, model weights or proprietary reference assets are vendored.

## Exclusions and unresolved areas

Mirrored host/plugin copies and obvious vendored duplicates were reduced where identified. A repository without `SKILL.md` is not counted as an installable skill merely because it is useful. ClaudeAnimationBase is a starter/guide; Blender MCP is an integration; RxFilm and Shipvideo are projects requiring separate adoption work. They remain useful discovery leads rather than falsely classified skills.

Runway, Veo, Luma, Grok and other families can appear in upstream discovery skills without having an approved current model surface in this initial router. New endpoint records need primary evidence and regression cases before promotion. Unverified Apple-Silicon H3 performance/8K claims and similar directory assertions were not admitted as approved runtime facts.

## Maintenance

Run `python3 scripts/check_sources.py --limit 100` or the manual GitHub Actions audit to flag changed repository revisions. This does not automatically certify changed skill bodies or model APIs. Re-read affected files, dependency paths, licensing and live schemas; update facts and tests; rebuild generated files; review the diff. There is no automatic merge, paid generation or scheduled polling enabled by this repository.

The completion audit rechecked all 193 skill paths against 41 recorded commit trees with zero blob/path mismatches; see [pin-verification.json](pin-verification.json). A final primary-documentation pass added LTX 2.5 API multishot and specialized local editing/EXR/restoration paths while retaining explicit 2.3-only Dub-It/Foley compatibility. These are documentary checks, not runtime tests.
