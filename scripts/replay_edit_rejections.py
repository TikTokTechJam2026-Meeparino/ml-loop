"""Replay saved rejected patches without model calls or workspace mutation.

Usage: python scripts/replay_edit_rejections.py storage/<run>
Reads local diagnostics only; prints counts, never source or credentials.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.mutation.parser import _BLOCK, apply_edits, EditError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path)
    args = parser.parse_args()
    requests, responses = {}, {}
    counts = Counter()
    for line in (args.run_dir / 'events.jsonl').read_text(encoding='utf-8').splitlines():
        event = json.loads(line)
        data = event['data']
        kind = event['event']
        if kind not in ('model.request', 'model.response', 'output.rejected'):
            continue
        if data.get('stage') not in ('mutate', 'repair'):
            continue
        key = data['call_id']
        artifact = json.loads(Path(data['artifact']).read_text(encoding='utf-8'))
        if kind == 'model.request':
            requests[key] = artifact
        elif kind == 'model.response':
            responses[key] = artifact
        else:
            request, response = requests[key], responses[key]
            prompt = request['messages'][1]['content'].split('SOURCE FILES\n', 1)[1]
            files = {m.group('filename'): m.group('body') for m in _BLOCK.finditer(prompt)}
            if not files:
                raise ValueError('No source files extracted from request')
            original = dict(files)
            try:
                apply_edits(files, response['response']['text'])
            except EditError as exc:
                counts['rejected'] += 1
                if 'SOURCE HINTS' in str(exc):
                    counts['with_source_hints'] += 1
                old = artifact['exception']['message'].split('\n', 1)[0]
                if not str(exc).startswith(old):
                    raise AssertionError(f'Rejection changed for call {key}')
            else:
                raise AssertionError(f'Previously rejected patch accepted: {key}')
            assert files == original, 'Replay mutated input source'
    print(json.dumps(dict(counts), indent=2))


if __name__ == '__main__':
    main()
