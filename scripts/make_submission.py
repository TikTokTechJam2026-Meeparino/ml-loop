"""Write a starter-kit submission CSV from a finished run's predictions.

The orchestrator stores raw scores as executions/<id>/predictions.npy, one
float per evaluated row. The benchmark expects the CSV schema defined in
data/kuairand-pure/starter-kit/submit.py:

    row_id,user_id,video_id,score

Row identity comes from the starter kit's own data.load(), not from the agent,
so the file is aligned against the same loader submit.py --check uses. The
agent evaluates the identical row order, which `--score` confirms by
reproducing the run's reported metrics.

Usage:
    python scripts/make_submission.py --run-dir storage/live-50-001 \
        --data-dir data/kuairand-pure/KuaiRand-Pure/data \
        --out submission-test.csv

Then validate with the starter kit itself:
    cd data/kuairand-pure/starter-kit
    python submit.py --check ../../../submission-test.csv --data_dir ../KuaiRand-Pure/data
    python submit.py --score ../../../submission-test.csv --data_dir ../KuaiRand-Pure/data
"""

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
STARTER_KIT = ROOT / "data" / "kuairand-pure" / "starter-kit"

HEADER = ["row_id", "user_id", "video_id", "score"]


def final_test_predictions(run_dir: Path) -> tuple[Path, dict]:
    """Locate the predictions the run's own report attributes to its final test."""
    report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    final = report.get("final_test") or {}
    if final.get("status") != "success":
        raise SystemExit(f"{run_dir}: final test did not succeed ({final.get('status')})")
    path = Path(final["artifact_dir"]) / "predictions.npy"
    if not path.exists():
        raise SystemExit(f"Missing predictions: {path}")
    return path, final


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--split", default="test", choices=["valid", "test"])
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    predictions_path, final = final_test_predictions(args.run_dir)
    scores = np.load(predictions_path)

    sys.path.insert(0, str(STARTER_KIT))
    from data import load  # noqa: E402  starter kit is the authority on row order

    rows = load(args.data_dir)[args.split]
    if len(rows) != len(scores):
        raise SystemExit(f"{len(scores)} predictions but {len(rows)} rows in split "
                         f"{args.split}; the run evaluated a different split")

    with open(args.out, "w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(HEADER)
        for index, (row, score) in enumerate(zip(rows, scores)):
            writer.writerow([index, row[1], row[2], f"{float(score):.6g}"])

    reported = final.get("scores", {})
    print(f"Wrote {args.out}: {len(rows):,d} rows (split={args.split})")
    print(f"  source     : {predictions_path}")
    print(f"  node       : {final.get('node_id')}")
    print(f"  run metrics: GAUC {reported.get('GAUC'):.6f} | "
          f"nDCG@5 {reported.get('nDCG@5'):.6f} | primary {reported.get('primary'):.6f}")
    print("  Validate with submit.py --check, then --score to confirm alignment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
