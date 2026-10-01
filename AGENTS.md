# Agent entry point

This repository is a decision workflow for video and motion tasks, not a bundle to load wholesale.

1. Read `skills/video-router/SKILL.md` first.
2. Separate host, controller, task, render engine or video model, version, provider and skill adapter. Opus 5.5 and GPT-6 Astra are controllers, not video endpoints.
3. Route a structured request with `python3 scripts/avs.py route --request <file.json>`. For exact typography, UI or charts use a procedural renderer; for generated footage select a model-specific surface; for both use hybrid.
4. Read only the selected model guide, full registry record and relevant pinned upstream skill. `search`, `show`, `list` and `stats` are offline navigation commands.
5. Treat required capabilities, exact models, privacy and verified limits as hard constraints. Six-calendar-month recency is a preference after filtering. Unknown release dates receive no freshness boost.
6. Resolve live provider schemas, account access, licenses, costs and tool availability before execution. The router never authorizes spend or certifies output quality.
7. Inspect real playback, sound and encoded metadata before delivery. Preserve prompts, model/backend identifiers, job IDs, source assets, edits and QA findings.

## Repository changes

Canonical facts live in `registry/*.json`; original guidance lives in `docs/`. Update evidence and regression tests with every capability change. Run:

```bash
python3 scripts/avs.py validate
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

Generated indexes, retrieval chunks and standalone skill bundles must stay synchronized. Never vendor unlicensed upstream skill bodies, infer a model release date from a repository update, or mark static inspection as runtime testing. Read `SECURITY.md` before installing an upstream skill and `CONTRIBUTING.md` before promoting a new model surface.
