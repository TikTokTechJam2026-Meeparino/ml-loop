"""Private subprocess entry point. Process isolation is NOT a security sandbox."""
import importlib
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def main():
    mode, workspace, request_path, checkpoint, output = sys.argv[1:]
    request = json.loads(Path(request_path).read_text(encoding='utf-8'))
    sys.path.insert(0, workspace)
    if mode == 'train':
        importlib.import_module('train').train(
            request['train'], request['valid'], checkpoint,
            request['overrides'], request['context'])
    else:
        predictor = importlib.import_module('model').load_predictor(checkpoint)
        scores = [float(score) for score in predictor.predict(request['rows'])]
        if len(scores) != len(request['rows']) or not all(math.isfinite(score) for score in scores):
            raise ValueError('predict must return exactly one finite score per row')
        Path(output).write_text(json.dumps(scores, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    from agent.sandbox.lease import file_lease
    with file_lease(Path(sys.argv[4]).parent / 'worker.lock'):
        main()
