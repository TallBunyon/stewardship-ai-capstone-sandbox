# The three capstone tracks

Each track is a full-semester project for one team. All three build on the same
contract (`CONTRACT.md`) and the same sandbox. You never need the proprietary
engine to do excellent work here — the mock gives you a stable target, and strong
work on the mock is strong work on the real thing.

---

## Track 1 — Interpretation Console (web UI)

**Build a console a researcher would actually want to use.** Start from
`console-ui/` (Vite + React + TypeScript). It already renders one report from the
mock. Grow it into a real tool:

- Let the user choose or upload a dataset and see the summary + observations +
  integrity notes.
- Make severity legible at a glance; make the integrity notes impossible to miss.
- Handle the unglamorous states well: empty data, all-missing columns, a dataset
  with no numeric parameters, a very wide table (the Green River file has ~40).

**Ships against:** `InterpretationReport` JSON. No engine access needed.
**Good stretch:** a small local server that calls `interpret()` live instead of a
static fixture.

---

## Track 2 — Public-data harness

**Bring in real public data and measure interpretation quality.** Two halves:

1. **Connectors** — pull water-quality data from public sources (USGS, EPA, the
   Water Quality Portal) into the `DatasetSummary` shape. Handle their real-world
   messiness: units, gaps, station metadata.
2. **Scoring harness** — run many datasets through `interpret()` and score the
   results. Because the mock is deterministic and its `integrity_notes` are
   explicit, you can build objective checks: does it flag known-bad values? does it
   stay silent when it should? does it ever state something the data doesn't support?

**Ships against:** `read_dataset` in / `InterpretationReport` out. No engine access
needed. **Note:** the *federal* data connector on the real platform touches
non-public material — that part lives behind the signed agreement, not in this
sandbox. Everything you need for a complete, gradeable Track 2 is public.

---

## Track 3 — Offline field application

**An interpreter that runs on a laptop in the field with no signal.** Package the
`read_dataset -> interpret` flow into an app that works fully offline: capture or
load a dataset on-site, get a report, store it, sync later. University hardware is
well-suited to this. This is the track with the most strategic upside for the
platform — a genuinely useful offline tool.

**Ships against:** the whole contract, running locally. No network, no key.

---

## Which teams sign the IP agreement?

- **Open exploration on this sandbox → no signature needed.** You can start today.
- **Going deeper than the sandbox** (the real engine, the private repo, or the
  non-public federal data) **→ every member of that team signs** before access is
  granted.
- **If Stewardship Compute intends to fold your team's work into the platform**
  (for example, adopting a Track 1 console), **that team signs too** — the signature
  is what gives the company a license to use your work. You keep ownership of your
  own standalone work and may put it in your portfolio.

Your faculty mentor coordinates signatures. Nothing about the open sandbox is
gated on them.
