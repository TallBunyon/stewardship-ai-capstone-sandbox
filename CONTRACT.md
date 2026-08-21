# The data contract

This is the whole interface. Two functions and three shapes. Everything you build
reads or writes these — the Console UI renders a report, the harness scores
reports, the offline app produces a summary and a report on a laptop with no
network. The real Stewardship AI engine implements the *same* two functions with
the *same* shapes, so anything you build here moves onto it without changes.

## Two functions

```python
from sandbox_engine import read_dataset, interpret

summary = read_dataset("data/sample_sensor_stream.csv")   # file  -> DatasetSummary
report  = interpret(summary)                              # summary -> InterpretationReport
```

- `read_dataset(path)` reads a CSV and returns a **DatasetSummary**. Deterministic,
  standard-library only.
- `interpret(summary)` returns an **InterpretationReport**. In this sandbox it is a
  transparent rule-based **mock** (see `sandbox_engine/interpreter.py`); on the real
  platform it is the trained engine. Same signature either way.

## Three shapes

### DatasetSummary — the input contract
| field | type | meaning |
|---|---|---|
| `filename` | str | source file name |
| `row_count` | int | number of data rows |
| `columns` | list[str] | column headers, in order |
| `numeric_columns` | dict[str, ColumnStats] | per-column `count / mean / minimum / maximum` |
| `missing_counts` | dict[str, int] | blank cells per column |
| `date_columns` | list[str] | columns that look like dates/timestamps |
| `preview_rows` | list[dict] | first few rows, as read |

### InterpretationReport — the output contract
| field | type | meaning |
|---|---|---|
| `source` | str | who produced it (`"sandbox-mock"` here) |
| `dataset_filename` | str | which dataset it read |
| `summary_text` | str | one-paragraph plain-language read |
| `observations` | list[Observation] | the grounded statements |
| `sources_consulted` | list[str] | citations (empty from the mock) |
| `integrity_notes` | list[str] | **what it could NOT stand behind — always show this** |

### Observation
| field | type | meaning |
|---|---|---|
| `severity` | str | `"info"` \| `"watch"` \| `"concern"` |
| `statement` | str | the claim |
| `evidence` | str | the column(s) and value(s) it rests on |

## JSON

`report.to_dict()` gives plain JSON — that's the file the Console UI loads
(`sandbox_engine/fixtures/sample_report.json`). `summary.to_dict()` does the same
for the input side. Nothing else crosses the boundary between the engine and your UI.

## The one design rule: never hide the integrity notes

The point of the platform is an interpreter that won't present a guess as a fact.
Whatever you build, `integrity_notes` gets shown to the user, not swallowed. A UI
that renders a confident summary and drops the caveats is the one failure mode to
avoid.
