import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import avs

class SpecializedTests(unittest.TestCase):
    def check(self, expected, **request):
        result = avs.route({'as_of': '2026-10-01', **request})
        self.assertEqual(result['status'], 'preflight_required' if expected else 'no_compatible_route')
        self.assertFalse(result['ready_to_execute'])

CASES = [
    ('api_multishot', True, dict(task='multishot', model='ltx-2-5-fast')),
    ('automatic_duration', True, dict(task='generate', model='ltx-2-5-fast', auto_duration=True)),
    ('auto_with_anchors', False, dict(task='transition', model='ltx-2-5-fast', auto_duration=True)),
    ('inpaint_25', True, dict(task='inpaint', model='ltx-2-5')),
    ('dub_25_unverified', False, dict(task='dub', model='ltx-2-5')),
    ('dub_23', True, dict(task='dub', model='ltx-2-3')),
    ('foley_25_unverified', False, dict(task='foley', model='ltx-2-5')),
    ('foley_23', True, dict(task='foley', model='ltx-2-3')),
    ('exr_25', True, dict(task='exr-hdr', model='ltx-2-5')),
    ('a2v_source_length', True, dict(task='audio-driven', model='ltx-2-5-pro', duration=12, input_audio_seconds=12)),
    ('a2v_length_conflict', False, dict(task='audio-driven', model='ltx-2-5-pro', duration=8, input_audio_seconds=12)),
    ('extend_20_rejected', False, dict(task='extend', model='flux3', duration=20)),
    ('extend_15_accepted', True, dict(task='extend', model='flux3', duration=15)),
]

def make_case(expected, request):
    def test(self):
        self.check(expected, **request)
    return test

for name, expected, request in CASES:
    setattr(SpecializedTests, 'test_' + name, make_case(expected, request))

class ExtraValidationTests(unittest.TestCase):
    def test_fixed_and_automatic_duration_conflict(self):
        with self.assertRaises(ValueError):
            avs.route({'task': 'generate', 'duration': 8, 'auto_duration': True})

    def test_source_audio_length_is_operation_specific(self):
        with self.assertRaises(ValueError):
            avs.route({'task': 'generate', 'input_audio_seconds': 12})
