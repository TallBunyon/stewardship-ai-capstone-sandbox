"""read_dataset(): turn a CSV file into a DatasetSummary.

Standard library only (csv, statistics). Handles the two shapes you'll see in
the sample data: grab-sample water-quality tables and high-frequency sensor
streams. If you want a richer reader (XLSX, type inference, etc.), that's fair
game for your project — just keep returning a DatasetSummary.
"""
from __future__ import annotations

import csv
import statistics
from pathlib import Path

from .schema import DatasetSummary, ColumnStats

# Column names that look like dates/timestamps (case-insensitive substring match).
_DATE_HINTS = ("date", "time", "timestamp")


def _looks_like_date(column: str) -> bool:
    c = column.lower()
    return any(h in c for h in _DATE_HINTS)


def _to_float(value: str) -> float | None:
    if value is None:
        return None
    v = value.strip()
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def read_dataset(path: str | Path, preview: int = 5) -> DatasetSummary:
    """Read a CSV and return the input contract (a DatasetSummary)."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    columns = list(rows[0].keys()) if rows else []
    date_columns = [c for c in columns if _looks_like_date(c)]

    numeric_columns: dict[str, ColumnStats] = {}
    missing_counts: dict[str, int] = {}

    for col in columns:
        raw = [r.get(col, "") for r in rows]
        missing_counts[col] = sum(1 for v in raw if (v is None or str(v).strip() == ""))
        if col in date_columns:
            continue
        nums = [f for f in (_to_float(v) for v in raw) if f is not None]
        # Treat a column as numeric only if most present values parse as numbers.
        present = len(raw) - missing_counts[col]
        if present and len(nums) >= max(1, present // 2):
            numeric_columns[col] = ColumnStats(
                count=len(nums),
                mean=round(statistics.fmean(nums), 4) if nums else None,
                minimum=min(nums) if nums else None,
                maximum=max(nums) if nums else None,
            )

    preview_rows = [dict(r) for r in rows[:preview]]

    return DatasetSummary(
        filename=path.name,
        row_count=len(rows),
        columns=columns,
        numeric_columns=numeric_columns,
        missing_counts=missing_counts,
        date_columns=date_columns,
        preview_rows=preview_rows,
    )
