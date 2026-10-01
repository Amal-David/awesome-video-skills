"""Machine-readable contracts for consumers that do not use the Python CLI."""
import json
from avs import REQUEST_KEYS, load_catalog

def outputs():
    catalog = load_catalog()
    props = {key: {'type': 'string'} for key in sorted(REQUEST_KEYS)}
    props['task'] = {'type': 'string', 'enum': [w['id'] for w in catalog['workflows']]}
    props['require'] = {'type': 'array', 'items': {'type': 'string', 'enum': [c['id'] for c in catalog['capabilities']]}, 'uniqueItems': True}
    props['available_tools'] = {'type': 'array', 'items': {'type': 'string'}}
    for key in ('recent_only', 'audio_only', 'media_local_only', 'auto_duration'):
        props[key] = {'type': 'boolean'}
    for key in ('duration', 'fps'):
        props[key] = {'type': 'number', 'exclusiveMinimum': 0}
    for key in ('reference_images', 'reference_videos', 'reference_audio'):
        props[key] = {'type': 'integer', 'minimum': 0}
    for key in ('reference_video_seconds', 'reference_audio_seconds', 'budget_usd', 'input_audio_seconds'):
        props[key] = {'type': 'number', 'minimum': 0}
    props['limit'] = {'type': 'integer', 'minimum': 1, 'maximum': 100, 'default': 5}
    props['runtime'] = {'enum': ['either', 'local', 'cloud']}
    props['host'] = {'enum': ['generic', 'claude-code', 'codex']}
    props['as_of'] = {'type': 'string', 'format': 'date'}
    request = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Video routing request v1', 'type': 'object', 'additionalProperties': False, 'properties': props}
    result = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Successful routing response v1', 'type': 'object', 'required': ['schema_version', 'status', 'ready_to_execute', 'candidates', 'excluded', 'warnings'], 'properties': {'schema_version': {'const': '1.0.0'}, 'status': {'enum': ['needs_brief', 'preflight_required', 'no_compatible_route']}, 'ready_to_execute': {'const': False}, 'candidates': {'type': 'array'}, 'excluded': {'type': 'array'}, 'warnings': {'type': 'array', 'items': {'type': 'string'}}}}
    manifest = {'schema_version': '1.0.0', 'kind': 'project-specific-discovery-manifest', 'entrypoint': 'skills/video-router/SKILL.md', 'navigation': 'registry/navigation.json', 'retrieval': 'registry/retrieval.jsonl', 'route_argv': ['python3', 'scripts/avs.py', 'route', '--request', '{request_file}'], 'request_schema': 'schemas/request.schema.json', 'result_schema': 'schemas/result.schema.json', 'routing_network_access': False, 'minimum_python': '3.10'}
    return {path: json.dumps(value, indent=2) + '\n' for path, value in [('schemas/request.schema.json', request), ('schemas/result.schema.json', result), ('agent-manifest.json', manifest)]}
