"""Data contract for the capstone sandbox.

These are the ONLY shapes you need to build against. Every track — the
Interpretation Console UI, the public-data harness, the offline app — reads and
writes these same objects. The real Stewardship AI engine implements this exact
contract behind the scenes; in this public sandbox a small rule-based *mock*
implements it instead (see interpreter.py). Build to the contract, not to the
mock, and your work drops straight onto the real engine later.

Everything here is plain Python standard library. No external packages, no model,
no API key.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class ColumnStats:
    """Numeric summary for one column of a dataset."""
    count: int
    mean: float | None
    minimum: float | None
    maximum: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DatasetSummary:
    """The input contract: what a dataset looks like after it is read.

    Produced by read_dataset(). Consumed by the interpreter and by anything that
    renders or scores a dataset. Deliberately simple and self-describing.
    """
    filename: str
    row_count: int
    columns: list[str]
    numeric_columns: dict[str, ColumnStats]      # column name -> stats
    missing_counts: dict[str, int]               # column name -> # of blank cells
    date_columns: list[str]
    preview_rows: list[dict[str, str]]           # first few rows, as-read strings

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["numeric_columns"] = {k: v.to_dict() for k, v in self.numeric_columns.items()}
        return d


@dataclass
class Observation:
    """One grounded statement the interpreter can defend from the data.

    `severity` is a plain word — "info", "watch", or "concern" — so a UI can
    color it without importing any logic. `evidence` names the column(s) and
    value(s) the statement rests on, so a reader can check it.
    """
    severity: str          # "info" | "watch" | "concern"
    statement: str
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InterpretationReport:
    """The output contract: a grounded, checkable read of a dataset.

    `integrity_notes` is the honesty layer surfaced at the interface level: a
    plain list of what the interpreter could NOT stand behind (missing data,
    out-of-range values, anything it declined to conclude). The real engine fills
    this from its own checks; the sandbox mock fills it with a few simple rules.
    A UI should always show it — never hide it.
    """
    source: str                                  # "sandbox-mock" here; real engine sets its own
    dataset_filename: str
    summary_text: str
    observations: list[Observation] = field(default_factory=list)
    sources_consulted: list[str] = field(default_factory=list)
    integrity_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["observations"] = [o.to_dict() for o in self.observations]
        return d
