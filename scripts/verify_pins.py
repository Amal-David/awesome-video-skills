#!/usr/bin/env python3
"""Verify that pinned upstream skill paths resolve to their recorded Git blobs."""
import concurrent.futures
import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def verify(group):
    (repository, revision), skills = group
    try:
        result = subprocess.run(['gh', 'api', f'repos/{repository}/git/trees/{revision}?recursive=1'], capture_output=True, text=True, timeout=45, check=True)
        tree = json.loads(result.stdout)
        if tree.get('truncated'):
            return {'repository': repository, 'status': 'incomplete-tree'}
        entries = {entry['path']: entry for entry in tree['tree']}
        bad = [skill['id'] for skill in skills if entries.get(skill['path'], {}).get('sha') != skill['blob_sha']]
        return {'repository': repository, 'revision': revision, 'paths_checked': len(skills), 'status': 'mismatch' if bad else 'verified', 'mismatches': bad}
    except (subprocess.SubprocessError, ValueError, OSError):
        return {'repository': repository, 'status': 'lookup-failed'}

def main():
    skills = json.loads((ROOT / 'registry/skills.json').read_text())
    groups = {}
    for skill in skills:
        groups.setdefault((skill['repository'], skill['revision']), []).append(skill)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(verify, groups.items()))
    report = {'snapshot_date': json.loads((ROOT / 'registry/manifest.json').read_text())['snapshot_date'], 'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'scope': 'Pinned skill paths and Git blob IDs against immutable commit trees. Not execution or script auditing.', 'skill_paths': len(skills), 'repository_snapshots': len(results), 'results': results}
    destination = ROOT / 'research/pin-verification.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    failures = [r for r in results if r['status'] != 'verified']
    print(json.dumps({'paths': len(skills), 'snapshots': len(results), 'failures': failures}, indent=2))
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
