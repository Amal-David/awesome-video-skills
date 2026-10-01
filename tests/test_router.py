import copy
import datetime as dt
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import avs

class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = avs.load_catalog()

    def route(self, **request):
        return avs.route({'as_of': '2026-10-01', **request}, self.catalog)

    def test_catalog_integrity(self):
        self.assertEqual(avs.validate_catalog(self.catalog), [])

    def test_no_false_runtime_certification(self):
        for row in self.catalog['models'] + self.catalog['skills']:
            self.assertIs(row['runtime_tested'], False)

    def test_calendar_month_window(self):
        self.assertEqual(avs.six_months_before(dt.date(2026, 10, 31)), dt.date(2026, 4, 30))

    def test_request_is_not_mutated_and_round_trips(self):
        original = {'task': 'motion', 'agent': 'astra', 'as_of': '2026-10-01'}
        saved = copy.deepcopy(original)
        result = avs.route(original, self.catalog)
        self.assertEqual(original, saved)
        avs.route(result['request'], self.catalog)

    def test_controller_cannot_be_used_as_video_model(self):
        with self.assertRaises(ValueError):
            self.route(task='generate', model='gpt-6stra')

    def test_motion_transfer_is_not_motion_graphics(self):
        result = self.route(query='transfer motion from a reference video')
        self.assertEqual(result['task'], 'reference')
        self.assertIn('motion-transfer', result['required_capabilities'])

    def test_hybrid_splits_exact_text_into_finishing(self):
        result = self.route(task='hybrid', require=['exact-text'], model='seedance')
        self.assertEqual(result['status'], 'preflight_required')
        self.assertEqual(result['finishing_stage']['status'], 'preflight_required')
        self.assertNotIn('exact-text', result['required_capabilities'])

    def test_provider_adapter_is_not_cross_wired(self):
        result = self.route(task='reference', model='seedance', provider='byteplus', available_tools=['scenario-mcp', 'scenario-core-skill'])
        self.assertTrue(result['candidates'])
        self.assertFalse(any(s['id'].startswith('scenario-labs--') for c in result['candidates'] for s in c['skills']))

    def test_lexical_search_and_exact_id(self):
        rows = avs.search('kinetic typography', self.catalog, kind='skills')
        self.assertTrue(any('kinetic' in row['id'] for row in rows))
        self.assertEqual(avs.search('seedance-2-5-byteplus', self.catalog)[0]['id'], 'seedance-2-5-byteplus')
        self.assertEqual(avs.search('', self.catalog), [])

    def test_local_media_filter(self):
        result = self.route(task='generate', media_local_only=True)
        self.assertTrue(result['candidates'])
        self.assertTrue(all(c['runtime'] == 'local' for c in result['candidates']))

    def test_unknown_numeric_limit_stays_pending(self):
        result = self.route(task='retake', model='ltx-2-3', duration=9)
        self.assertIn('duration is not verified in this snapshot.', result['candidates'][0]['preflight_checks'])
        self.assertFalse(result['ready_to_execute'])

    def test_future_snapshot_warning(self):
        result = self.route(task='motion', as_of='2026-11-01')
        self.assertTrue(any('newer than the catalog' in w for w in result['warnings']))

CASES = [
    ('chatcut_h3max_refs_rejected', dict(task='reference', model='h3-max', provider='chatcut'), False),
    ('fal_h3max_refs_accepted', dict(task='reference', model='h3-max', provider='fal'), True),
    ('chatcut_missing_tools', dict(task='generate', model='chatcut-h3-max', available_tools=[]), False),
    ('chatcut_ready_tools', dict(task='generate', model='chatcut-h3-max', available_tools=['chatcut-mcp','chatcut-project']), True),
    ('scenario_ready_tools', dict(task='reference', model='scenario-seedance', available_tools=['scenario-mcp','scenario-core-skill']), True),
    ('astra_remotion', dict(task='motion', agent='gpt-6stra', engine='remotion'), True),
    ('h3_audio_only_rejected', dict(task='reference', model='h3', audio_only=True), False),
    ('max_audio_only_accepted', dict(task='reference', model='h3-max', audio_only=True), True),
    ('base_reference_overflow', dict(task='reference', model='h3', reference_images=10, reference_audio=3), False),
    ('base_valid_mixed_refs', dict(task='reference', model='h3', reference_images=9, reference_audio=3), True),
    ('ltx_fast_20_supported', dict(task='generate', model='ltx-2-5-fast', duration=20, resolution='1080p', fps=24), True),
    ('ltx_fast_20_high_fps_rejected', dict(task='generate', model='ltx-2-5-fast', duration=20, resolution='1080p', fps=48), False),
    ('ltx_fast_20_4k_rejected', dict(task='generate', model='ltx-2-5-fast', duration=20, resolution='4k', fps=24), False),
    ('ltx_pro_20_rejected', dict(task='generate', model='ltx-2-5-pro', duration=20), False),
    ('ltx25_retake_rejected', dict(task='retake', model='ltx-2-5'), False),
    ('ltx23_retake_fallback', dict(task='retake', model='ltx-2-3'), True),
    ('kling_not_recent', dict(task='generate', model='kling', recent_only=True), False),
    ('local_unknown_date_not_recent', dict(task='generate', model='ltx-local', recent_only=True), False),
    ('release_in_future', dict(task='generate', model='seedance', as_of='2026-06-01'), False),
    ('happyhorse_video_refs_not_verified', dict(task='reference', model='happyhorse', reference_videos=1), False),
    ('wan_document_route', dict(task='document-to-video', model='wan-prime'), True),
    ('flux_enhancement', dict(task='draft-enhance', model='flux3'), True),
    ('omni_stateful_edit', dict(task='edit', model='omni', require=['stateful-editing']), True),
    ('unknown_motion_requirement_rejected', dict(task='motion', require=['native-audio']), False),
]

def route_case(request, expected):
    def test(self):
        result = self.route(**request)
        self.assertEqual(result['status'], 'preflight_required' if expected else 'no_compatible_route')
        self.assertFalse(result['ready_to_execute'])
        if not expected:
            self.assertTrue(result['excluded'])
    return test

for name, request, expected in CASES:
    setattr(RouterTests, 'test_' + name, route_case(request, expected))

INVALID = [
    ('unknown_field', {'secret_option': True}),
    ('unknown_capability', {'require': ['magic-video']}),
    ('wrong_require_type', {'require': 'text-to-video'}),
    ('zero_duration', {'duration': 0}),
    ('negative_fps', {'fps': -1}),
    ('non_finite', {'duration': math.nan}),
    ('boolean_number', {'duration': True}),
    ('fractional_count', {'reference_images': 1.5}),
    ('bad_limit', {'limit': 0}),
    ('wrong_limit_type', {'limit': 1.5}),
    ('privacy_conflict', {'media_local_only': True, 'runtime': 'cloud'}),
    ('audio_only_conflict', {'audio_only': True, 'reference_images': 1}),
    ('bad_host', {'host': 'imaginary'}),
    ('bad_agent', {'agent': 'imaginary'}),
    ('bad_model', {'model': 'imaginary'}),
]

def invalid_case(fields):
    def test(self):
        with self.assertRaises(ValueError):
            self.route(task='generate', **fields)
    return test

for name, fields in INVALID:
    setattr(RouterTests, 'test_invalid_' + name, invalid_case(fields))
