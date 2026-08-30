"""Shared structured event log for agent components.

Only the parent agent process writes this log; candidate stdout/stderr stay in
per-attempt artifacts. Appends are serialized across threads in this process,
not across independent agent processes. Use separate log paths for those.
Logging is best-effort: failures return False and never mask the task exception.
Do not pass credentials, environment variables, raw subprocess output, or
unredacted exception messages as event data.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import threading


_LOCK = threading.Lock()


class RunLogger:
    def __init__(self, path='storage/run_log.jsonl'):
        self.path = Path(path).resolve()

    def emit(self, event, *, component, run_id=None, level='info', **data):
        """Append one UTF-8 JSON record; return whether it was written.

        Fields: schema_version, timestamp (UTC), level, component, event,
        run_id, data. Newlines in data are escaped, not additional log records.
        """
        try:
            if not isinstance(event, str) or not event or not isinstance(component, str) or not component:
                raise ValueError('event and component must be nonempty strings')
            if level not in ('debug', 'info', 'warning', 'error'):
                raise ValueError('invalid log level')
            record = dict(schema_version=1, timestamp=datetime.now(timezone.utc).isoformat(),
                          level=level, component=component, event=event, run_id=run_id, data=data)
            encoded = (json.dumps(record, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
            with _LOCK:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open('ab') as stream:
                    stream.write(encoded)
                    stream.flush()
            return True
        except Exception as exc:
            # No recursive logging, raw exception text, or warnings-as-errors.
            try:
                sys.stderr.write(f'Run log append failed ({type(exc).__name__}).\n')
            except Exception:
                pass
            return False
