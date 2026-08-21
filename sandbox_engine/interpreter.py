"""interpret(): the MOCK interpreter for the sandbox.

⚠️ THIS IS A STAND-IN. It is a few dozen lines of transparent if/else rules — NOT
a language model, NOT the real Stewardship AI engine, and NOT a source of real
scientific conclusions. Its only job is to return a well-formed
InterpretationReport so you can build and test the UI, connectors, and offline app
against a stable, non-proprietary contract. When your team is granted access to
the real engine, it implements interpret(summary) with the same signature and your
code keeps working unchanged.

The thresholds below are textbook, illustrative values (e.g. dissolved oxygen
below ~4 mg/L stresses most fish). They are here to make the mock produce
believable-shaped output — treat them as placeholders, not as the platform's
science.
"""
from __future__ import annotations

from .schema import DatasetSummary, InterpretationReport, Observation

MOCK_SOURCE = "sandbox-mock"

# Illustrative-only thresholds, keyed by a substring of the column name.
# (column-name substring, low_watch, low_concern, high_watch, high_concern, unit, subject)
_RULES = [
    ("dissolved_oxygen", 5.0, 4.0, None, None, "mg/L", "dissolved oxygen"),
    ("pH", 6.5, 6.0, 9.0, 9.5, "", "pH"),
    ("water_temp", None, None, 25.0, 30.0, "C", "water temperature"),
    ("temperature", None, None, 25.0, 30.0, "C", "water temperature"),
    ("turbidity", None, None, 25.0, 50.0, "NTU", "turbidity"),
]


def _match_rule(column: str):
    c = column.lower()
    for rule in _RULES:
        if rule[0].lower() in c:
            return rule
    return None


def interpret(summary: DatasetSummary) -> InterpretationReport:
    """Return a grounded-looking InterpretationReport for a DatasetSummary.

    Deterministic: the same input always yields the same output.
    """
    observations: list[Observation] = []
    integrity_notes: list[str] = []

    # Rule-based observations over numeric columns.
    for col, stats in summary.numeric_columns.items():
        rule = _match_rule(col)
        if not rule or stats.minimum is None or stats.maximum is None:
            continue
        _, low_w, low_c, high_w, high_c, unit, subject = rule
        u = f" {unit}".rstrip()

        if low_c is not None and stats.minimum <= low_c:
            observations.append(Observation(
                "concern",
                f"Low {subject} present in this dataset.",
                f"min {col} = {stats.minimum}{u} (at or below {low_c}{u}).",
            ))
        elif low_w is not None and stats.minimum <= low_w:
            observations.append(Observation(
                "watch",
                f"{subject.capitalize()} dips into a range worth watching.",
                f"min {col} = {stats.minimum}{u} (at or below {low_w}{u}).",
            ))

        if high_c is not None and stats.maximum >= high_c:
            observations.append(Observation(
                "concern",
                f"High {subject} present in this dataset.",
                f"max {col} = {stats.maximum}{u} (at or above {high_c}{u}).",
            ))
        elif high_w is not None and stats.maximum >= high_w:
            observations.append(Observation(
                "watch",
                f"{subject.capitalize()} reaches a range worth watching.",
                f"max {col} = {stats.maximum}{u} (at or above {high_w}{u}).",
            ))

    if not observations:
        observations.append(Observation(
            "info",
            "No sandbox rule flagged this dataset; the numeric ranges sit inside "
            "the mock's illustrative bounds.",
            f"{len(summary.numeric_columns)} numeric column(s) checked.",
        ))

    # Integrity layer: state plainly what the mock did NOT do or could not stand behind.
    integrity_notes.append(
        "Output produced by the SANDBOX MOCK (transparent if/else rules), not by a "
        "trained model or the real Stewardship AI engine. Do not treat as scientific fact."
    )
    heavy_missing = {c: n for c, n in summary.missing_counts.items()
                     if summary.row_count and n > summary.row_count // 2}
    if heavy_missing:
        cols = ", ".join(sorted(heavy_missing))
        integrity_notes.append(
            f"More than half the cells are blank in: {cols}. Any read of these columns "
            f"is low-confidence."
        )
    if not summary.numeric_columns:
        integrity_notes.append("No numeric columns were detected, so no quantitative read was attempted.")

    subject_bits = ", ".join(list(summary.numeric_columns)[:6]) or "no numeric parameters"
    summary_text = (
        f"Sandbox mock read of {summary.filename}: {summary.row_count} row(s), "
        f"{len(summary.columns)} column(s). Numeric parameters examined: {subject_bits}. "
        f"{len(observations)} observation(s) generated. See integrity notes for limits."
    )

    return InterpretationReport(
        source=MOCK_SOURCE,
        dataset_filename=summary.filename,
        summary_text=summary_text,
        observations=observations,
        sources_consulted=[],   # the mock cites nothing; the real engine populates this
        integrity_notes=integrity_notes,
    )
