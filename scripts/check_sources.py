#!/usr/bin/env python3
"""Read-only GitHub revision audit. A changed repository is not a verified model update."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def audit(limit: int = 5) -> dict:
    if not 1 <= limit <= 100:
        raise ValueError('limit must be between 1 and 100.')
    if not shutil.which('gh'):
        raise ValueError('Install/configure GitHub CLI to run this optional audit. Offline routing does not need it.')
    skills = json.loads((ROOT / 'registry/skills.json').read_text())
    repos = sorted({s['repository'] for s in skills})[:limit]
    results = []
    for repo in repos:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
            raise ValueError('Invalid repository identifier.')
        pinned = sorted({s['revision'] for s in skills if s['repository'] == repo})
        try:
            response = subprocess.run(['gh', 'api', f'repos/{repo}/commits?per_page=1', '--jq', '.[0].sha'], capture_output=True, text=True, timeout=30, check=True)
            head = response.stdout.strip()
            if not re.fullmatch(r'[a-f0-9]{40}', head):
                raise ValueError('Unexpected GitHub revision response.')
            results.append({'repository': repo, 'pinned_revisions': pinned, 'current_head': head, 'repository_changed': any(p != head for p in pinned)})
        except (subprocess.SubprocessError, ValueError):
            results.append({'repository': repo, 'status': 'lookup_failed', 'instruction': 'Check gh authentication, rate limits and repository access.'})
    return {'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'repositories_checked': len(results),
            'scope': 'GitHub default-branch revisions only; no automatic semantic or model capability certification.',
            'next_action': 'Review changed skill paths, dependencies, licenses and live model schemas before updating the catalog.', 'results': results}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.limit)
        content = json.dumps(report, indent=2) + '\n'
        if args.output:
            args.output.write_text(content)
        print(content, end='')
        return 1 if any(r.get('status') == 'lookup_failed' for r in report['results']) else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
