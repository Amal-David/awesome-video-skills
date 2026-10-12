"""Provider contracts and operation-specific reference and duration constraints."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import avs


RUNWAY_CASES = [
    ('gen45_generate', True, dict(task='generate', model='gen4.5', duration=5, resolution='720p')),
    ('gen45_image', True, dict(task='animate-image', model='gen4.5', duration=10)),
    ('gen45_long', False, dict(task='generate', model='gen4.5', duration=11)),
    ('gen45_last_frame', False, dict(task='transition', model='gen4.5', duration=5)),
    ('gen45_native_audio', False, dict(task='generate', model='gen4.5', require=['native-audio'])),
    ('gen45_1080', False, dict(task='generate', model='gen4.5', resolution='1080p')),
    ('aleph_edit', True, dict(task='edit', model='aleph2', duration=10, reference_images=5)),
    ('aleph_too_many_keyframes', False, dict(task='edit', model='aleph2', reference_images=6)),
    ('aleph_long_source', False, dict(task='edit', model='aleph2', duration=31)),
    ('aleph_creation', False, dict(task='generate', model='aleph2')),
    ('aleph_opaque_alpha', False, dict(task='edit', model='aleph2', require=['alpha-output'])),
    ('aleph_outpaint', True, dict(task='outpaint', model='aleph2', duration=5)),
    ('gen45_fractional_duration', False, dict(task='generate', model='gen4.5', duration=5.5)),
]


class OperationConstraintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = avs.load_catalog()

    def route(self, **request):
        return avs.route({'as_of': '2026-10-12', **request}, self.catalog)

    def test_edit_keyframes_require_editing_and_image_guidance(self):
        result = self.route(task='edit', model='aleph2', reference_images=5)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertEqual(result['required_capabilities'], ['image-reference', 'video-editing'])

    def test_outpainting_keyframes_do_not_imply_generation(self):
        result = self.route(task='outpaint', model='aleph2', reference_images=2)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertEqual(result['required_capabilities'], ['image-reference', 'outpainting'])

    def test_edit_does_not_drop_an_explicit_generation_requirement(self):
        result = self.route(task='edit', model='aleph2', reference_images=1,
                            require=['reference-to-video'])
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertIn('reference-to-video', result['required_capabilities'])

    def test_edit_guidance_does_not_establish_source_video_presence(self):
        result = self.route(task='edit', model='aleph2', reference_images=1)
        self.assertFalse(result['ready_to_execute'])
        self.assertNotIn('reference_videos', result['request'])
        self.assertIn('source-video', result['workflow']['inputs'])
        self.assertTrue(any('reference counts do not establish source-media presence' in check
                            for check in result['candidates'][0]['preflight_checks']))

    def test_edit_still_checks_each_supplied_guidance_modality(self):
        result = self.route(task='edit', model='aleph2', reference_videos=1)
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertIn('video-reference', result['required_capabilities'])
        self.assertNotIn('reference-to-video', result['required_capabilities'])

    def test_audio_guided_edit_is_not_audio_only_generation(self):
        catalog = copy.deepcopy(self.catalog)
        editor = next(m for m in catalog['models'] if m['id'] == 'runway-aleph-2')
        # A hypothetical future editing adapter supports audio guidance, but no
        # prompt/reference creation. Do not assert this capability for real Aleph.
        editor['capabilities'].append('audio-reference')
        result = avs.route({'task': 'edit', 'model': 'aleph2', 'reference_audio': 1,
                            'as_of': '2026-10-12'}, catalog)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertEqual(result['required_capabilities'], ['audio-reference', 'video-editing'])

    def test_creation_still_requires_reference_generation(self):
        result = self.route(task='generate', model='gen4.5', reference_images=1)
        self.assertEqual(result['status'], 'no_compatible_route')
        self.assertIn('reference-to-video', result['required_capabilities'])
        self.assertIn('image-reference', result['required_capabilities'])

    def test_creation_with_audio_only_guidance_keeps_audio_only_requirement(self):
        result = self.route(task='generate', model='h3-max', provider='fal', reference_audio=1)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertIn('reference-to-video', result['required_capabilities'])
        self.assertIn('audio-only-reference', result['required_capabilities'])

    def test_gen45_every_whole_second_is_supported(self):
        for duration in range(2, 11):
            with self.subTest(duration=duration):
                self.assertEqual(self.route(task='generate', model='gen4.5', duration=duration)['status'],
                                 'preflight_required')

    def test_gen45_duration_evidence_does_not_fabricate_frame_rate_support(self):
        result = self.route(task='generate', model='gen4.5', duration=5, fps=24)
        self.assertEqual(result['status'], 'preflight_required')
        self.assertIn('fps is not verified in this snapshot.', result['candidates'][0]['preflight_checks'])
        model = next(m for m in self.catalog['models'] if m['id'] == 'runway-gen-4-5')
        self.assertNotIn('fps', model['limits'])
        self.assertNotIn('profiles', model['limits'])

    def test_allowed_seconds_alone_are_sufficient_duration_evidence(self):
        catalog = copy.deepcopy(self.catalog)
        model = next(m for m in catalog['models'] if m['id'] == 'runway-gen-4-5')
        model['limits'] = {'allowed_seconds': [2, 5, 10]}
        accepted = avs.route({'task': 'generate', 'model': 'gen4.5', 'duration': 5,
                              'as_of': '2026-10-12'}, catalog)
        self.assertNotIn('duration is not verified in this snapshot.', accepted['candidates'][0]['preflight_checks'])
        rejected = avs.route({'task': 'generate', 'model': 'gen4.5', 'duration': 6,
                              'as_of': '2026-10-12'}, catalog)
        self.assertEqual(rejected['status'], 'no_compatible_route')

    def test_operation_duration_override_replaces_creation_allowed_seconds(self):
        model = {'limits': {'allowed_seconds': [2, 5, 10]},
                 'operation_limits': {'edit': {'min_seconds': 2, 'max_seconds': 30}}}
        self.assertEqual(avs.limit_errors(model, {'task': 'edit', 'duration': 12.5}), [])
        self.assertTrue(avs.limit_errors(model, {'task': 'generate', 'duration': 12.5}))


def contract_case(expected, request):
    def test(self):
        result = self.route(**request)
        self.assertEqual(result['status'], 'preflight_required' if expected else 'no_compatible_route')
        self.assertFalse(result['ready_to_execute'])
        if not expected:
            self.assertTrue(result['excluded'])
    return test


for name, expected, request in RUNWAY_CASES:
    setattr(OperationConstraintTests, 'test_contract_' + name, contract_case(expected, request))


if __name__ == '__main__':
    unittest.main()
