"""Local diagnostic serialization. Never captures frame locals or entire environments."""
import os
import re
import traceback
from dataclasses import asdict, is_dataclass
from collections.abc import Mapping


_SENSITIVE = re.compile(r'api.?key|authorization|cookie|password|secret|access.?token|refresh.?token|credential|(?:^|_)token$', re.I)


def sanitize(value, secrets=()):
    known = tuple(v for k, v in os.environ.items() if _SENSITIVE.search(k) and v)
    def clean(item):
        if isinstance(item, bytes):
            item = item.decode('utf-8', errors='replace')
        if isinstance(item, str):
            for secret in sorted(set(known + tuple(secrets)), key=len, reverse=True):
                if secret:
                    item = item.replace(secret, '[REDACTED]')
            item = re.sub(r'(?i)(bearer\s+)[^\s\"\']+', r'\1[REDACTED]', item)
            item = re.sub(r'(?i)((?:authorization|cookie)\s*[:=]\s*)[^\r\n\"\']+', r'\1[REDACTED]', item)
            item = re.sub(r'(?i)((?:api[_-]?key|password|secret|access_token|refresh_token|authorization|cookie)[\"\']?\s*[:=]\s*[\"\']?)[^\s\"\'&,;}]+', r'\1[REDACTED]', item)
            return re.sub(r'(https?://)[^/\s:@]+:[^/\s@]+@', r'\1[REDACTED]@', item)
        if isinstance(item, Mapping):
            return {str(k): '[REDACTED]' if _SENSITIVE.search(str(k)) else clean(v) for k, v in item.items()}
        if isinstance(item, (tuple, list)):
            return [clean(v) for v in item]
        if is_dataclass(item) and not isinstance(item, type):
            return clean(asdict(item))
        if hasattr(item, 'model_dump'):
            return clean(item.model_dump(mode='json'))
        if item is None or isinstance(item, (bool, int, float)):
            return item
        # Avoid arbitrary object reprs (SDK objects may contain credentials).
        return {'unserialized_type': type(item).__name__}
    return clean(value)


def exception_details(exc, secrets=()):
    """Preserve chain, traceback and useful provider/subprocess fields, without locals."""
    seen = set()
    def describe(error):
        if id(error) in seen:
            return {'cycle': True}
        seen.add(id(error))
        data = dict(type=type(error).__name__, message=str(error),
                    traceback=''.join(traceback.format_exception(type(error), error, error.__traceback__)))
        for name in ('status_code', 'request_id', 'code', 'errno', 'returncode', 'cmd',
                     'stdout', 'stderr', 'timeout', 'body', 'details'):
            value = getattr(error, name, None)
            if value is not None:
                data[name] = value
        response = getattr(error, 'response', None)
        if response is not None:
            data['response'] = {name: getattr(response, name, None) for name in ('status_code', 'text')}
            headers = getattr(response, 'headers', {})
            data['response']['headers'] = {k: v for k, v in headers.items()
                if k.lower() in ('retry-after', 'x-request-id', 'request-id', 'date', 'content-type')}
        cause = error.__cause__ or error.__context__
        if cause is not None:
            data['cause'] = describe(cause)
        return data
    return sanitize(describe(exc), secrets)
