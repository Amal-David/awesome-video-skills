"""Regressions for constraints that must survive inference and staged routing."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import avs


class ConstraintRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = avs.load_catalog()

    def route(self, **request):
        return avs.route({'as_of': '2026-10-01', **request}, self.catalog)

    def test_inferred_motion_transfer_survives_saved_request(self):
        request = {'query': 'transfer motion from a reference video', 'as_of': '2026-10-01'}
        original = copy.deepcopy(request)
        first = avs.route(request, self.catalog)
        replay = avs.route(first['request'], self.catalog)
        self.assertEqual(request, original)
        self.assertIn('motion-transfer', first['request']['require'])
        self.assertEqual(first['required_capabilities'], replay['required_capabilities'])
        self.assertEqual([c['id'] for c in first['candidates']], [c['id'] for c in replay['candidates']])

    def test_hybrid_cloud_constraint_applies_to_finishing(self):
        result = self.route(task='hybrid', model='seedance', runtime='cloud')
        self.assertTrue(result['candidates'])  # The failure is in the finishing stage.
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertEqual(result['finishing_stage']['status'], 'no_compatible_route')
        self.assertEqual(result['finishing_stage']['request']['runtime'], 'cloud')
        self.assertFalse(result['finishing_stage']['candidates'])

    def test_hybrid_privacy_filters_future_cloud_renderers(self):
        catalog = copy.deepcopy(self.catalog)
        # Existing renderers are local, which used to conceal the missing filter.
        for engine in catalog['engines']:
            if engine['id'] != 'remotion':
                engine['runtime'] = 'cloud'
        result = avs.route({'task': 'hybrid', 'media_local_only': True,
                            'as_of': '2026-10-01'}, catalog)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertTrue(result['finishing_stage']['request']['media_local_only'])
        self.assertEqual([c['id'] for c in result['finishing_stage']['candidates']], ['remotion'])
        self.assertTrue(all(c['runtime'] == 'local' for c in result['candidates']))

    def test_hybrid_preserves_declared_tool_availability(self):
        catalog = copy.deepcopy(self.catalog)
        for engine in catalog['engines']:
            engine['required_tools'] = ['test-renderer']
        result = avs.route({'task': 'hybrid', 'available_tools': [],
                            'as_of': '2026-10-01'}, catalog)
        self.assertEqual(result['status'], 'no_compatible_route')
        finishing = result['finishing_stage']
        self.assertEqual(finishing['request']['available_tools'], [])
        self.assertTrue(all(any('Missing declared adapter prerequisites' in reason
                                for reason in row['reasons']) for row in finishing['excluded']))

    def test_hybrid_preserves_controller_host_and_output_settings(self):
        result = self.route(task='hybrid', model='seedance', agent='astra', host='codex',
                            fps=24, resolution='4K')
        finishing = result['finishing_stage']
        self.assertEqual(finishing['controller']['id'], result['controller']['id'])
        for key in ('agent', 'host', 'fps', 'resolution'):
            self.assertEqual(finishing['request'][key], result['request'][key])
        self.assertEqual(finishing['request']['resolution'], '2160p')
        self.assertNotIn('model', finishing['request'])

    def test_audio_duration_cannot_bypass_task_check_through_inference(self):
        with self.assertRaisesRegex(ValueError, 'audio-driven task'):
            self.route(query='make cinematic footage', input_audio_seconds=12)

    def test_audio_duration_accepts_an_inferred_audio_driven_task(self):
        result = self.route(query='audio-driven video', input_audio_seconds=12)
        self.assertEqual(result['task'], 'audio-driven')
        self.assertEqual(result['status'], 'preflight_required')
        self.assertIn('audio-driven-video', result['required_capabilities'])

    def test_source_audio_duration_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, 'input_audio_seconds must be positive'):
            self.route(task='audio-driven', input_audio_seconds=0)

    def test_reference_durations_cannot_hide_missing_media_counts(self):
        for seconds, count in (('reference_video_seconds', 'reference_videos'),
                               ('reference_audio_seconds', 'reference_audio')):
            for supplied_count in ({}, {count: 0}):
                with self.subTest(seconds=seconds, supplied_count=supplied_count):
                    with self.assertRaisesRegex(ValueError, 'requires a positive ' + count):
                        self.route(task='generate', **{seconds: 5, **supplied_count})

    def test_paired_reference_duration_enforces_media_capability(self):
        result = self.route(task='generate', model='happyhorse', reference_videos=1,
                            reference_video_seconds=5)
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertIn('video-reference', result['required_capabilities'])

    def test_paired_reference_duration_accepts_supported_media(self):
        result = self.route(task='reference', model='h3-max', provider='fal',
                            reference_videos=1, reference_video_seconds=5)
        self.assertEqual(result['status'], 'preflight_required')

    def test_large_json_integers_are_rejected_by_limits_without_overflow(self):
        for field in ('duration', 'reference_images'):
            with self.subTest(field=field):
                result = self.route(task='reference', model='h3', **{field: 10 ** 400})
                self.assertEqual(result['status'], 'no_compatible_route')

    def test_mixed_numeric_audio_durations_do_not_overflow(self):
        for duration, source in ((1.0, 10 ** 400), (10 ** 400, 1.0)):
            with self.subTest(duration_type=type(duration).__name__):
                result = self.route(task='audio-driven', model='ltx-2-5-pro',
                                    duration=duration, input_audio_seconds=source)
                self.assertEqual(result['status'], 'no_compatible_route')
                self.assertFalse(result['candidates'])
                self.assertTrue(any('differs from the requested duration' in reason
                                    for item in result['excluded'] for reason in item['reasons']))

    def test_mixed_numeric_reference_counts_do_not_overflow(self):
        result = self.route(task='reference', model='h3', reference_images=10 ** 400,
                            reference_videos=1.0)
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertIsInstance(result['request']['reference_videos'], int)
        self.assertTrue(any('Combined reference count exceeds' in reason
                            for item in result['excluded'] for reason in item['reasons']))

    def test_integral_decimal_reference_counts_are_accepted_and_normalized(self):
        request = {'task': 'reference', 'model': 'h3', 'as_of': '2026-10-12',
                   'reference_images': 1.0, 'reference_videos': 1.0, 'reference_audio': 1.0}
        result = avs.route(request, self.catalog)
        self.assertEqual(result['status'], 'preflight_required')
        for field in ('reference_images', 'reference_videos', 'reference_audio'):
            self.assertEqual(result['request'][field], 1)
            self.assertIsInstance(result['request'][field], int)
            self.assertIsInstance(request[field], float)  # Caller input is unchanged.

    def test_audio_duration_comparison_preserves_millisecond_tolerance(self):
        for source, expected in ((12.0005, 'preflight_required'), (12.002, 'no_compatible_route')):
            with self.subTest(source=source):
                result = self.route(task='audio-driven', model='ltx-2-5-pro',
                                    duration=12, input_audio_seconds=source)
                self.assertEqual(result['status'], expected)

    def test_blank_selectors_are_not_silently_ignored(self):
        for field in ('task', 'model', 'family', 'engine', 'agent', 'host', 'runtime',
                      'provider', 'resolution', 'as_of'):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'must not be blank'):
                    self.route(**{field: ''})
        self.assertEqual(self.route(query='')['status'], 'needs_brief')

    def test_specialized_tasks_are_not_inferred_as_generic_footage(self):
        cases = {
            'inpaint this video': 'inpaint',
            'outpaint the video': 'outpaint',
            'restore this video': 'restore',
            'EXR video roundtrip': 'exr-hdr',
            'dub this video': 'dub',
            'video-to-audio Foley': 'foley',
            'draft-enhance video': 'draft-enhance',
        }
        for query, task in cases.items():
            with self.subTest(query=query):
                result = self.route(query=query)
                self.assertEqual(result['task'], task)
                self.assertEqual(result['status'], 'preflight_required')
                self.assertNotIn('text-to-video', result['required_capabilities'])


if __name__ == '__main__':
    unittest.main()
