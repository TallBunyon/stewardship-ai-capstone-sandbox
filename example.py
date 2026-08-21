"""Runnable end-to-end example for the capstone sandbox.

    python example.py                       # uses data/sample_sensor_stream.csv
    python example.py data/green_river_rockport_wq.csv

Shows the whole contract in one pass:

    read a dataset  ->  interpret it (mock)  ->  read observations + integrity notes  ->  emit JSON

Everything is offline and standard-library only. No Ollama, no API key, no cost.
The JSON printed at the end is exactly what the Console UI consumes
(see sandbox_engine/fixtures/sample_report.json).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from sandbox_engine import read_dataset, interpret

DEFAULT = Path(__file__).parent / "data" / "sample_sensor_stream.csv"


def main(path: str) -> None:
    print(f"\n[1] read_dataset({Path(path).name!r})")
    summary = read_dataset(path)
    print(f"    rows={summary.row_count}  columns={len(summary.columns)}")
    print(f"    numeric parameters: {', '.join(list(summary.numeric_columns)) or '(none)'}")

    print("\n[2] interpret(summary)   # SANDBOX MOCK")
    report = interpret(summary)
    print(f"    source={report.source}")
    print(f"    {report.summary_text}")

    print("\n[3] observations")
    for o in report.observations:
        print(f"    [{o.severity:>7}] {o.statement}")
        print(f"              evidence: {o.evidence}")

    print("\n[4] integrity notes (always show these in a UI)")
    for note in report.integrity_notes:
        print(f"    - {note}")

    print("\n[5] the report as JSON — this is the UI's input contract:\n")
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    dataset = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT)
    if not Path(dataset).exists():
        print(f"Dataset not found: {dataset}\nPass a CSV path, or run from the repo root.")
        sys.exit(1)
    main(dataset)
