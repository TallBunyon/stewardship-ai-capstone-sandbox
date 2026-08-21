"""Stewardship AI — Capstone Sandbox engine (public, mock).

Public, non-proprietary stand-in for the Stewardship AI interpretation engine.
Build your capstone project against the contract exported here; the real engine
implements the same names and shapes.

    from sandbox_engine import read_dataset, interpret
    report = interpret(read_dataset("data/sample_sensor_stream.csv"))
    print(report.summary_text)
    for note in report.integrity_notes:
        print("integrity:", note)
"""
from .schema import (
    ColumnStats,
    DatasetSummary,
    Observation,
    InterpretationReport,
)
from .reader import read_dataset
from .interpreter import interpret, MOCK_SOURCE

__all__ = [
    "ColumnStats",
    "DatasetSummary",
    "Observation",
    "InterpretationReport",
    "read_dataset",
    "interpret",
    "MOCK_SOURCE",
]
