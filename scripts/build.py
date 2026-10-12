#!/usr/bin/env python3
"""Generate navigation, retrieval chunks and self-contained skills from canonical data."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, str] = {}

def emit(path: str, content: str) -> None:
    OUT[path] = content if content.endswith('\n') else content + '\n'

def encoded(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'

def generate() -> None:
    OUT.clear()
    from build_schema import outputs
    OUT.update(outputs())
    data = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'registry').glob('*.json') if p.stem != 'navigation'}
    models, skills, sources = data['models'], data['skills'], data['sources']
    snapshot = data['manifest']['snapshot_date']
    version = data['manifest'].get('project_version', '1.0.0')
    counts = {
        'model_surfaces': len(models), 'engines': len(data['engines']),
        'controllers': len(data['agents']), 'upstream_skill_paths': len(skills),
        'skill_repositories': len({s['repository'] for s in skills}),
        'workflows': len(data['workflows']),
        'native_skills': len({m['family'] for m in models}) + 3,
    }
    data['manifest']['counts'] = counts
    emit('registry/manifest.json', encoded(data['manifest']))
    families = sorted({m['family'] for m in models})
    nav = {'schema_version': '1.0.0', 'entrypoint': 'skills/video-router/SKILL.md',
           'lanes': {lane: [w['id'] for w in data['workflows'] if w['lane'] == lane] for lane in ('procedural', 'generative', 'hybrid')},
           'families': {f: {'guide': 'docs/models/' + f + '.md', 'model_ids': [m['id'] for m in models if m['family'] == f], 'upstream_skill_ids': [s['id'] for s in skills if f in s['families']]} for f in families},
           'controllers': [a['id'] for a in data['agents']]}
    for family, branch in nav['families'].items():
        branch['versions'] = {version: {provider: [m['id'] for m in models if m['family'] == family and m['model_version'] == version and m['provider'] == provider] for provider in sorted({m['provider'] for m in models if m['family'] == family and m['model_version'] == version})} for version in sorted({m['model_version'] for m in models if m['family'] == family})}
    emit('registry/navigation.json', encoded(nav))
    lines = ['# Model and backend index', '', f"Catalog snapshot: {snapshot}. Check each record's checked_at for its own evidence date. A model family is not an endpoint contract. Unknown release dates receive no recency boost.", '', '| Surface | Family guide | Release/availability | Runtime | New or distinguishing abilities |', '| --- | --- | --- | --- | --- |']
    for m in sorted(models, key=lambda r: (r['release_date'] or '', r['id']), reverse=True):
        lines.append(f"| `{m['id']}` | [{m['family']}](models/{m['family']}.md) | {m['release_date'] or 'Unverified'} ({m['release_date_kind']}) | {m['runtime']} | {'; '.join(m['novel_abilities'])} |")
    lines += ['', 'Use `python3 scripts/avs.py show <id>` for complete constraints, endpoint identifiers, evidence and explicit unsupported modes. Provider schemas must be rechecked before execution.']
    emit('docs/model-index.md', '\n'.join(lines))
    lines = ['# Curated upstream skill paths', '', f"{counts['upstream_skill_paths']} pinned paths from {counts['skill_repositories']} repositories. These are linked, not vendored or runtime-certified. Mirrors and platform-specific duplicates were reduced; this is not a claim of exhaustive internet coverage.", '', 'Use the CLI for family/capability retrieval. A missing license is not permission to copy a skill.']
    for tier in ('core', 'supporting', 'review-required'):
        lines += ['', '## ' + tier.replace('-', ' ').title(), '', '| Skill card | Focus | Portability | Repository license |', '| --- | --- | --- | --- |']
        for s in (x for x in skills if x['curation_tier'] == tier):
            lines.append(f"| [{s['name']}](skills/{s['id']}.md) | {s['summary']} | {s['portability']} | {s['repository_license']} |")
    emit('docs/catalog.md', '\n'.join(lines))
    for s in skills:
        card = [f"# {s['name']}", '', s['summary'], '', f"**ID:** `{s['id']}` · **Tier:** {s['curation_tier']}", f"**Evidence:** {s['evidence']} · **Runtime tested:** no · **Checked:** {s['checked_at']}", f"**Portability:** {s['portability']} · **Provider scope:** {', '.join(s.get('provider_scope', ['any']))}", f"**Prerequisites:** {', '.join(s['requires']) or 'Read the upstream prerequisites.'}", f"**Model binding:** {s.get('model_binding', 'Inspect exact version.')}", '', f"[Pinned upstream SKILL.md]({s['url']})", f"Repository revision: `{s['revision']}`", f"File SHA-256: `{s['sha256']}`", f"Repository license: {s['repository_license']}; skill-declared license: {s['declared_skill_license'] or 'not found'}.", '', '## Before use', '', *['- ' + w for w in s['warnings']], '', 'Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.']
        emit('docs/skills/' + s['id'] + '.md', '\n'.join(card))
    chunks = []
    for kind in ('models', 'engines', 'agents', 'skills', 'workflows'):
        for row in data[kind]:
            content = json.dumps(row, sort_keys=True, ensure_ascii=False)
            chunks.append(json.dumps({'id': kind + '/' + row['id'], 'kind': kind, 'record_id': row['id'], 'content_sha256': hashlib.sha256(content.encode()).hexdigest(), 'snapshot_date': data['manifest']['snapshot_date'], 'source_urls': ([row['url']] if row.get('url') else [source['url'] for source in sources if source['id'] in row.get('source_ids', [])]), 'evidence': row.get('evidence', 'project-authored'), 'text': content}, ensure_ascii=False))
    emit('registry/retrieval.jsonl', '\n'.join(chunks))
    router_text = '---\nname: video-router\ndescription: Find a model-specific video or motion skill and produce a decision workflow. Use for Claude Code, Opus 5.5, GPT-6 Astra, Remotion, Hyperframes, LTX, MiniMax H3/H3 Max, Seedance 2.5, Wan, FLUX.3, Gemini Omni, HappyHorse or Kling. Separates code motion from generated footage, checks capabilities and prefers recent verified releases.\ncompatibility: Any file-reading agent; Python 3.10+ for the optional offline router.\nmetadata:\n  version: "1.0.0"\n  snapshot: "2026-10-01"\n---\n\n# Video workflow router\n\nStart here, not by loading the entire catalog. This skill selects and explains; it does not generate media or install third-party code.\n\n1. Separate the controller (Opus/Astra), host, task, renderer or footage model, and provider. Read [controller profiles](references/agents.md) only when needed.\n2. Form a structured request with task, required capabilities, exact model/version when specified, runtime/privacy, source modalities and output constraints.\n3. Run `python3 <skill-dir>/scripts/avs.py route --task motion --agent astra` or pass `--request <request.json>`. Use the actual installation directory, not an assumed global path. Without Python, follow [decision flow](references/decision-flow.md).\n4. Read only the selected guide and complete record with `show <id>`. Use `search "ltx 2.5" --kind skills` for additional instruction discovery.\n5. Inspect the pinned upstream directory and live provider schema. Check platform prerequisites and licensing. Never execute unreviewed downloaded instructions or confuse a community claim with an API contract.\n6. Follow the returned workflow through preflight, draft, review and delivery. `preflight_required` is not approval to spend money. `no_compatible_route` must not be bypassed by silently relaxing constraints.\n\nRead [retrieval design](references/retrieval.md) for JSONL/RAG ingestion and [quality review](references/quality.md) before delivery. The bundled registry is an offline snapshot, not live availability or pricing.\n'
    router_text += '\nMachine consumers can read the [request schema](references/schemas/request.schema.json) and [result schema](references/schemas/result.schema.json).\n'
    router_text = router_text.replace('version: "1.0.0"', f'version: "{version}"').replace('snapshot: "2026-10-01"', f'snapshot: "{snapshot}"')
    router_text = router_text.replace('HappyHorse or Kling.', 'HappyHorse, Kling or Runway.')
    router_text += '\nFor concrete task stacks read [workflow recipes](references/workflow-recipes.md). To compare workflows or revise a skill from observed failures, read [evaluation](references/evaluation.md).\n'
    emit('skills/video-router/SKILL.md', router_text)
    for path, text in list(OUT.items()):
        if path.startswith('schemas/'):
            emit('skills/video-router/references/' + path, text)
    emit('skills/video-router/scripts/avs.py', (ROOT / 'scripts/avs.py').read_text())
    registry_files = {str(p.relative_to(ROOT)): p.read_text() for p in (ROOT / 'registry').glob('*.json') if p.stem != 'navigation'}
    registry_files['registry/navigation.json'] = OUT['registry/navigation.json']
    registry_files['registry/manifest.json'] = OUT['registry/manifest.json']
    for path, text in registry_files.items():
        emit('skills/video-router/references/' + path, text)
    authored_docs = {str(p.relative_to(ROOT)): p.read_text() for p in (ROOT / 'docs').rglob('*.md') if '/skills/' not in str(p.relative_to(ROOT)) and p.name not in ('catalog.md', 'model-index.md')}
    docs = {**authored_docs, **{p: text for p, text in OUT.items() if p.startswith('docs/')}}
    for path, text in docs.items():
        emit('skills/video-router/references/' + path.removeprefix('docs/'), text)
    subjects = {f: 'models/' + f + '.md' for f in families}
    subjects.update({'motion': 'motion.md', 'quality-review': 'quality.md'})
    for subject, path in subjects.items():
        name = 'video-' + subject
        description = 'Create editable motion graphics with Claude Opus 5.5 or GPT-6 Astra using Remotion, Hyperframes, Canvas, Manim or Blender. Use for kinetic typography, UI, charts, launch videos and deterministic animation.' if subject == 'motion' else 'Review generated or code-rendered video through actual playback, audio, content, rights and encoded-file checks.' if subject == 'quality-review' else 'Model-specific video workflow for ' + ', '.join(sorted({m['model_version'] for m in models if m['family'] == subject})) + ' in the ' + subject + ' family' + '. Select exact modes, references, provider constraints and prompt structure before generation, editing or continuation.'
        content = f'---\nname: {name}\ndescription: {json.dumps(description)}\ncompatibility: File-reading agents; actual generation requires the separately verified provider or renderer.\nmetadata:\n  version: "1.0.0"\n  snapshot: "2026-10-01"\n---\n\n# {subject.title()} workflow\n\nRead [the playbook](references/guide.md), then [the scoped records](references/records.json). Select the exact backend, version and operation before writing a request.\n\nRecord inputs, rights, duration, output constraints and budget. Inspect the live provider schema or renderer dependencies. Treat unknown capabilities as unresolved; never infer them from a related checkpoint or service. Generate only after authorization, preserve job/project provenance, and review actual playback and encoded metadata before delivery.\n\nThis is an original routing playbook, not a bundled third-party runtime. Upstream skills and their licenses must be reviewed separately.\n'
        content = content.replace('version: "1.0.0"', f'version: "{version}"').replace('snapshot: "2026-10-01"', f'snapshot: "{snapshot}"')
        if subject == 'quality-review':
            content += '\nWhen evaluating a skill or comparing workflows, read [the evaluation protocol](references/evaluation.md). Separate process evidence from final-video observations and leave unobserved dimensions unrated.\n'
            emit(f'skills/{name}/references/evaluation.md', (ROOT / 'docs/evaluation.md').read_text())
        emit(f'skills/{name}/SKILL.md', content)
        guide = (ROOT / 'docs' / path).read_text().replace('(catalog.md)', '(https://github.com/Amal-David/awesome-video-skills/blob/main/docs/catalog.md)')
        emit(f'skills/{name}/references/guide.md', guide)
        records = [m for m in models if m['family'] == subject] if subject in families else data['engines']
        emit(f'skills/{name}/references/records.json', encoded(records))
        if subject == 'motion':
            emit(f'skills/{name}/references/agents.md', (ROOT / 'docs/agents.md').read_text())
    readme = (ROOT / 'README.md').read_text()
    summary = f"**{counts['upstream_skill_paths']} pinned upstream skill paths · {counts['skill_repositories']} repositories · {counts['model_surfaces']} model/backend/workflow surfaces · {counts['workflows']} workflows · {counts['native_skills']} original installable skills**"
    window = data['manifest']['preferred_release_window']
    stats = f"<!-- avs:stats:start -->\n{summary}\n\nCatalog update: **{snapshot}**. Preferred model-release window: **{window['start']}–{window['end']}**. Each record retains its own evidence date; an update does not re-certify older entries.\n<!-- avs:stats:end -->"
    readme, matches = re.subn(r'<!-- avs:stats:start -->.*?<!-- avs:stats:end -->', lambda _: stats, readme, flags=re.S)
    if matches != 1:
        raise ValueError('README must contain exactly one avs:stats block.')
    emit('README.md', readme)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report drift without writing files.')
    args = parser.parse_args()
    generate()
    differences = []
    for relative, content in sorted(OUT.items()):
        destination = ROOT / relative
        if not destination.resolve().is_relative_to(ROOT) or '..' in Path(relative).parts:
            raise ValueError('Unsafe generated path: ' + relative)
        if args.check:
            if not destination.is_file() or destination.read_text() != content:
                differences.append(relative)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding='utf-8')
    print(json.dumps({'mode': 'check' if args.check else 'write', 'generated_files': len(OUT), 'drift': differences}, indent=2))
    return 1 if differences else 0

if __name__ == '__main__':
    raise SystemExit(main())
