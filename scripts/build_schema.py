"""Machine-readable contracts for consumers that do not use the Python CLI."""
import json
from avs import REQUEST_KEYS, load_catalog

def outputs():
    catalog = load_catalog()
    props = {key: {'type': 'string'} for key in sorted(REQUEST_KEYS)}
    for key in ('task', 'model', 'family', 'engine', 'agent', 'host', 'runtime', 'provider', 'resolution'):
        props[key].update(minLength=1, pattern=r'\S')
    props['task'] = {'type': 'string', 'enum': [w['id'] for w in catalog['workflows']]}
    props['require'] = {'type': 'array', 'items': {'type': 'string', 'enum': [c['id'] for c in catalog['capabilities']]}, 'uniqueItems': True}
    props['available_tools'] = {'type': 'array', 'items': {'type': 'string'}}
    for key in ('recent_only', 'audio_only', 'media_local_only', 'auto_duration'):
        props[key] = {'type': 'boolean'}
    for key in ('duration', 'fps', 'input_audio_seconds'):
        props[key] = {'type': 'number', 'exclusiveMinimum': 0}
    for key in ('reference_images', 'reference_videos', 'reference_audio'):
        props[key] = {'type': 'integer', 'minimum': 0}
    for key in ('reference_video_seconds', 'reference_audio_seconds', 'budget_usd'):
        props[key] = {'type': 'number', 'minimum': 0}
    props['limit'] = {'type': 'integer', 'minimum': 1, 'maximum': 100, 'default': 5}
    props['runtime'] = {'enum': ['either', 'local', 'cloud']}
    props['host'] = {'enum': ['generic', 'claude-code', 'codex']}
    props['as_of'] = {'type': 'string', 'format': 'date', 'pattern': r'^\d{4}-\d{2}-\d{2}$'}
    props['input_audio_seconds']['description'] = 'Positive source-audio duration for audio-driven generation. The router also checks the task inferred from query.'
    constraints = [
        {'if': {'properties': {'media_local_only': {'const': True}}, 'required': ['media_local_only']},
         'then': {'not': {'properties': {'runtime': {'const': 'cloud'}}, 'required': ['runtime']}}},
        {'if': {'properties': {'audio_only': {'const': True}}, 'required': ['audio_only']},
         'then': {'properties': {'reference_images': {'maximum': 0}, 'reference_videos': {'maximum': 0}}}},
        {'if': {'properties': {'auto_duration': {'const': True}}, 'required': ['auto_duration']},
         'then': {'not': {'required': ['duration']}}},
        {'if': {'required': ['input_audio_seconds']},
         'then': {'properties': {'task': {'const': 'audio-driven'}}}},
    ]
    for kind, count in (('video', 'reference_videos'), ('audio', 'reference_audio')):
        field = 'reference_' + kind + '_seconds'
        props[field]['description'] = 'A positive duration requires a positive ' + count + ' count.'
        constraints.append({'if': {'properties': {field: {'exclusiveMinimum': 0}}, 'required': [field]},
                            'then': {'required': [count], 'properties': {count: {'minimum': 1}}}})
    request = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Video routing request v1', 'type': 'object', 'additionalProperties': False, 'properties': props, 'allOf': constraints}
    result = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Successful routing response v1', 'type': 'object', 'required': ['schema_version', 'status', 'ready_to_execute', 'candidates', 'excluded', 'warnings'], 'properties': {'schema_version': {'const': '1.0.0'}, 'status': {'enum': ['needs_brief', 'preflight_required', 'no_compatible_route']}, 'ready_to_execute': {'const': False}, 'candidates': {'type': 'array'}, 'excluded': {'type': 'array'}, 'warnings': {'type': 'array', 'items': {'type': 'string'}}}}
    manifest = {'schema_version': '1.0.0', 'kind': 'project-specific-discovery-manifest', 'entrypoint': 'skills/video-router/SKILL.md', 'navigation': 'registry/navigation.json', 'retrieval': 'registry/retrieval.jsonl', 'route_argv': ['python3', 'scripts/avs.py', 'route', '--request', '{request_file}'], 'request_schema': 'schemas/request.schema.json', 'result_schema': 'schemas/result.schema.json', 'routing_network_access': False, 'minimum_python': '3.10'}
    return {path: json.dumps(value, indent=2) + '\n' for path, value in [('schemas/request.schema.json', request), ('schemas/result.schema.json', result), ('agent-manifest.json', manifest)]}
