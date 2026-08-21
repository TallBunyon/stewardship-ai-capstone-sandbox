"""Offline sanity tests for the sandbox contract. Run: python -m pytest

These need nothing installed but pytest — no Ollama, no key, no network. They're
also the fastest way to see how each piece is called.
"""
from pathlib import Path

from sandbox_engine import read_dataset, interpret, DatasetSummary, InterpretationReport

DATA = Path(__file__).resolve().parent.parent / "data"


def test_read_dataset_returns_summary():
    s = read_dataset(DATA / "sample_sensor_stream.csv")
    assert isinstance(s, DatasetSummary)
    assert s.row_count == 20
    assert "dissolved_oxygen_mgl" in s.numeric_columns
    # a timestamp column should be recognized as a date, not a numeric
    assert "timestamp" in s.date_columns
    assert "timestamp" not in s.numeric_columns


def test_interpret_returns_report_with_integrity_notes():
    report = interpret(read_dataset(DATA / "sample_sensor_stream.csv"))
    assert isinstance(report, InterpretationReport)
    assert report.source == "sandbox-mock"
    # the honesty layer is never empty — the mock always discloses that it is a mock
    assert report.integrity_notes
    assert any("MOCK" in n for n in report.integrity_notes)


def test_low_dissolved_oxygen_is_flagged_as_concern():
    report = interpret(read_dataset(DATA / "sample_sensor_stream.csv"))
    do_flags = [o for o in report.observations if "dissolved oxygen" in o.statement.lower()]
    assert do_flags, "expected the low-DO row (min 1.4 mg/L) to be flagged"
    assert do_flags[0].severity == "concern"


def test_deterministic():
    a = interpret(read_dataset(DATA / "sample_sensor_stream.csv")).to_dict()
    b = interpret(read_dataset(DATA / "sample_sensor_stream.csv")).to_dict()
    assert a == b, "same input must give the same output"
