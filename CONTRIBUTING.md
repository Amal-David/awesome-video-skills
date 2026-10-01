# Contributing

A useful contribution adds a reliable decision, not just another link. Small, evidence-backed additions are easier to review than unfiltered dumps.

## Add a skill

Find the actual upstream `SKILL.md`, not only a directory listing. Record repository, path, immutable commit, Git blob ID, file SHA-256, purpose, version binding, provider scope, prerequisites and license observations in `registry/skills.json`. Distinguish portable prompting from provider integrations and project-bound instructions. Do not vendor upstream text without permission. Use `review-required` when important assertions conflict with primary evidence.

## Add or update a model surface

Create a record for the exact family, version, provider and operation contract. Cite primary documentation and keep model release, provider availability and repository-update dates separate. Add new capabilities to the taxonomy only when they represent a distinct decision. Record joint limits and operation-specific overrides; do not transfer one mode’s constraints to another. Unknown dates or abilities stay unknown.

Link an original model guide and an installable family skill. Document what is new, what inputs it requires, where it is available, how to prompt it, which workflow to use and where it should not be selected. Add at least one compatible routing test and one rejection test. A current API contract takes precedence over a stale directory description, with the conflict documented.

## Validate and publish

```bash
python3 scripts/avs.py validate
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

Update manifest counts when adding records. Check Markdown links, evidence IDs, generated bundles and example requests. Optional network checks are `scripts/verify_pins.py` for pinned path/blob identity and `scripts/check_sources.py` for upstream revision drift. Neither performs an upstream execution audit.

Explain the evidence, scope and tests in the pull request. Do not claim a runtime was tested unless the actual generation/rendering workflow was run and its result inspected. Do not add generated media, credentials, local environment files or model weights. Keep this project’s metadata and original playbooks separate from upstream licenses.
