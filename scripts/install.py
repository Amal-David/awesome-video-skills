#!/usr/bin/env python3
"""Copy an original, self-contained skill. Dry run by default; never overwrite."""
from __future__ import annotations
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def copy_skill(name: str, target: Path, apply: bool = False, source_root: Path = ROOT / 'skills') -> dict:
    if not re.fullmatch(r'video-[a-z0-9-]+', name):
        raise ValueError('Invalid skill name.')
    source = source_root / name
    if not source.is_dir() or not (source / 'SKILL.md').is_file():
        raise ValueError('Unknown skill: ' + name)
    if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Source contains symlinks; review it before copying.')
    target = target.expanduser().absolute()
    destination = target / name
    if target.is_symlink() or destination.exists() or destination.is_symlink():
        raise ValueError('Destination exists or is a symlink. Nothing was overwritten.')
    if destination.resolve().is_relative_to(source.resolve()):
        raise ValueError('Destination cannot be inside the source skill.')
    files = [p for p in source.rglob('*') if p.is_file()]
    result = {'skill': name, 'destination': str(destination), 'files': len(files), 'applied': apply}
    if apply:
        target.mkdir(parents=True, exist_ok=True)
        destination.mkdir()  # Atomic reservation: a concurrent existing destination fails.
        try:
            shutil.copytree(source, destination, dirs_exist_ok=True)
        except Exception:
            shutil.rmtree(destination)  # Only the directory reserved by this invocation.
            raise
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', default='video-router')
    parser.add_argument('--target', required=True, type=Path, help='Parent skill directory, such as .claude/skills.')
    parser.add_argument('--apply', action='store_true', help='Actually copy; otherwise print the plan only.')
    args = parser.parse_args()
    try:
        print(json.dumps(copy_skill(args.skill, args.target, args.apply), indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc), 'applied': False}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
