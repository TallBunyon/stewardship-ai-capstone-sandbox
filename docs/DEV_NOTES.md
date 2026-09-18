# Dev notes — from the production engine team

A running log of what's changing on the **real** Stewardship AI engine, written for
the capstone teams building against this sandbox. The sandbox contract
(`CONTRACT.md`) does not change — `read_dataset -> DatasetSummary` and
`interpret -> InterpretationReport` stay exactly as documented. These notes tell you
what the production engine now *does* inside those two functions, so you can decide
how much of it to mirror in your mock, your UI, or your harness. Nothing here
requires access to the private engine.

Newest entry first.

---

## 2026-09-18 — Structure-aware reading + a stronger honesty layer

We put the engine through a real dataset this week: a live water-quality profile
from a research partner (Dr. Flinn, Murray State) — a multi-depth cast from a flooded
quarry. Fixing what it got wrong produced a batch of changes that sit right on top of
the two contract functions you already build against. Here is what changed and why,
and how each piece maps to a shape you already have.

### 1. `read_dataset` now detects *structure*, not just columns

The sandbox `DatasetSummary` is deliberately flat: columns, per-column stats, missing
counts, date columns, preview rows. That is the right starting contract. But the
biggest single quality win came from computing **structure** at read time —
deterministically, before any model or rule sees the data — and handing the
interpreter facts instead of a raw table.

Concretely, the production `read_dataset` now recognizes:

- **Vertical profile vs. time series.** A file with a depth column and repeated
  casts is a *depth profile sampled at ~one instant*, **not** a time series. This one
  distinction matters enormously: reading a profile as a time series manufactures
  fake "trends over time" (we literally saw an early version report "DO rising 1800%"
  by splitting a single depth cast into "early" and "late" halves). If a profile is
  detected, time-trend logic is switched **off**.
- **Per-site separation.** One file held two sites (a deep station and a channel
  station). They are different water columns and must be read and compared
  separately — never averaged into one. The reader now splits by a detected site
  column.
- **Computed profile features**, treated as established fact by the interpreter:
  thermocline depth, oxycline, hypolimnion bounds/thickness, surface-vs-bottom deltas
  for temperature / DO / conductivity / pH, and a redox (ORP) read.
- **Sensor-zero artifact rows dropped.** A sonde logs a `0.000 / 0.000` row before it
  is in the water; left in, it drags every column's minimum to zero and invents an
  outlier. The reader detects and removes those rows (and records that it did).

**How this maps to your contract:** all of this is *additive*. On the real engine the
`DatasetSummary` carries a few extra structure fields alongside the ones in
`CONTRACT.md`; the documented fields are unchanged, so your code still works. If you
want to mirror the *pattern* — compute structure in `read_dataset`, so `interpret`
argues from facts rather than re-deriving them — that is the single highest-leverage
thing you can do, and it stays inside the "deterministic, standard-library" spirit of
the reader.

### 2. Stratification typing: thermocline vs. chemocline (and the meromixis question)

Dr. Flinn's key scientific note: this quarry is likely stratified by **dissolved
solids**, not just temperature — a **chemocline**, which can make a basin
*meromictic* (permanently stratified, never fully mixing) rather than a normal lake
that turns over every fall. These are different systems with different stewardship
implications, and the engine now distinguishes them:

- It separates the **thermal** density contribution from the **chemical**
  (conductivity) one, from the profile.
- Where a chemocline co-occurs with a thermocline, it flags the meromixis question as
  **open** and states that a cold-season / turnover-period cast is the decisive test —
  it does **not** assert that the lake turns over.

The lesson for any interpreter: name the *mechanism*, and where one warm-season
snapshot cannot settle which mechanism dominates, say so instead of guessing.

### 3. The honesty layer got sharper — this is your `integrity_notes` rule in action

`CONTRACT.md` already states the one design rule: *never present a guess as a fact*,
and always surface `integrity_notes`. This week was that rule under load. Real
examples now enforced:

- **No eutrophication call without nutrient data.** The dataset had no nutrient or
  chlorophyll columns (all blank). The engine must *not* diagnose nutrient enrichment
  or blame the low-oxygen bottom water on "nutrient loading." It explains the anoxia
  by physics and basin shape instead, and marks trophic state **"not assessable from
  this dataset."** (Contrast: a *different* dataset in the same area — Lake Barkley —
  **does** carry phosphorus and chlorophyll-a, so there eutrophication is a supported
  read. Same engine, opposite call, driven entirely by what the data contains.)
- **A real gradient is not an outlier.** A monotonic rise in specific conductance
  toward the bottom is the chemocline — real vertical structure — not a sensor spike.
  An earlier version flagged the deepest, highest reading as a "MAD spike"; that is a
  false integrity note and was removed.
- **Recommendations must match the system and the data.** For a deep stratified basin
  with no nutrient data, prescribing watershed nutrient controls (riparian buffers,
  ag BMPs, wastewater upgrades) is unsupported. The engine recommends what the data
  supports: a turnover-season cast, nutrient sampling before any trophic claim, and —
  only where low bottom-oxygen is the concern — oxygenation that adds oxygen *without*
  breaking stratification.

If you are building the Console UI (Track 1): these are exactly the notes that must
never be swallowed. A UI that renders the confident summary and hides "trophic state
not assessable" is the failure mode `CONTRACT.md` warns about.

### 4. Cross-dataset synthesis: keep distinct waterbodies distinct

Above the per-file read, the platform also synthesizes across many datasets. Two
rules we had to enforce there, in case your harness or app does anything similar:

- **Entity separation.** Each dataset may be a *different* waterbody. Do not invent a
  hydrologic connection between them, and do not attribute a cause measured in dataset
  A (e.g. phosphorus in a lake) to an effect measured in dataset B (e.g. anoxia in a
  quarry). At most, note both were observed and that confirming a link needs paired,
  same-site data.
- **Deduplicate by source, newest-wins.** Re-interpreting the same file should
  *supersede* its older interpretation, not add a second copy. We key dedup on the
  filename and keep the newest, and we refer to each dataset by its **waterbody/site
  name**, never by an index number.

### 5. Presentation + retrieval (context, not contract)

Two more changes, for completeness — neither touches the sandbox contract:

- **A water-column profile visualization** (temp / DO / ORP / conductivity down a
  shared depth axis, with the clines marked) now renders beside the written report.
  If Track 1 wants a reference for "what a good rendering of a profile looks like,"
  this is it: the chart is a second view of the *same* grounded facts, not a new
  claim.
- **Retrieval diversity.** When the engine grounds a report in reference sources, it
  now spreads citations across multiple documents (a per-source cap) instead of
  quoting one guide five times — so `sources_consulted` reflects a real span of
  evidence.

### The one-line takeaway

The quality jump this week came almost entirely from **architecture, not a bigger
model**: read the data's *structure* deterministically up front, hand the interpreter
facts, and make the honesty layer refuse the specific over-claims the data can't
support. That is the same bet the sandbox contract is built on — `read_dataset` does
real work, and `integrity_notes` is never optional.

Questions welcome — open an issue on this repo.
