import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import avs
import build
import install

class PackagingTests(unittest.TestCase):
    def test_dry_run_makes_no_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'not-created'
            result = install.copy_skill('video-router', target)
            self.assertFalse(result['applied'])
            self.assertFalse(target.exists())

    def test_installed_router_is_self_contained(self):
        with tempfile.TemporaryDirectory() as tmp:
            install.copy_skill('video-router', Path(tmp) / 'skills', apply=True)
            script = Path(tmp) / 'skills/video-router/scripts/avs.py'
            proc = subprocess.run([sys.executable, str(script), 'route', '--task', 'generate', '--model', 'ltx-2-5-pro', '--duration', '8', '--as-of', '2026-10-01'], cwd=tmp, capture_output=True, text=True, check=True)
            result = json.loads(proc.stdout)
            self.assertEqual(result['status'], 'preflight_required')
            self.assertTrue(Path(result['candidates'][0]['guide']).is_file())
            self.assertTrue(Path(result['candidates'][0]['guide']).resolve().is_relative_to(Path(tmp).resolve()))

    def test_existing_install_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'video-router'
            destination.mkdir()
            sentinel = destination / 'keep.txt'
            sentinel.write_text('keep')
            with self.assertRaises(ValueError):
                install.copy_skill('video-router', Path(tmp), apply=True)
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_invalid_install_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('../../escape', 'video-not-in-catalog', 'video-router/child'):
                with self.assertRaises(ValueError):
                    install.copy_skill(name, Path(tmp), apply=True)

    def test_single_model_skill_is_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            install.copy_skill('video-ltx', Path(tmp), apply=True)
            records = json.loads((Path(tmp) / 'video-ltx/references/records.json').read_text())
            self.assertTrue(records)
            self.assertEqual({r['family'] for r in records}, {'ltx'})

    def test_generated_files_are_current(self):
        build.generate()
        for path, expected in build.OUT.items():
            self.assertEqual((ROOT / path).read_text(), expected, path)

    def test_local_markdown_links_resolve(self):
        files = list(ROOT.glob('*.md')) + [ROOT / 'llms.txt'] + list((ROOT / 'research').glob('*.md')) + list((ROOT / 'docs').rglob('*.md')) + list((ROOT / 'skills').rglob('*.md'))
        for file in files:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', file.read_text()):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                path = target.split('#', 1)[0]
                self.assertTrue((file.parent / path).exists(), f'{file}: {target}')

    def test_native_skill_frontmatter(self):
        skills = list((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 11)
        for file in skills:
            text = file.read_text()
            self.assertTrue(text.startswith('---\n'))
            self.assertIn('\nname: ' + file.parent.name + '\n', text)
            description = re.search(r'^description: (.*)$', text, re.M).group(1)
            self.assertLessEqual(len(description), 1024)

    def test_retrieval_chunk_ids_unique(self):
        rows = [json.loads(line) for line in (ROOT / 'registry/retrieval.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), len({r['id'] for r in rows}))
        self.assertTrue(all(re.fullmatch('[a-f0-9]{64}', r['content_sha256']) for r in rows))

    def test_manifest_counts(self):
        c = avs.load_catalog()
        self.assertEqual(c['manifest']['counts']['upstream_skill_paths'], len(c['skills']))
        self.assertEqual(c['manifest']['counts']['model_surfaces'], len(c['models']))
