# Stewardship AI — Capstone Sandbox

A public, self-contained workspace for the Murray State senior capstone teams. It
gives you real sample data, a clean interface to build against, and a working UI
starting point — so you can write code on day one without waiting on anything.

## What this is (and isn't)

Stewardship AI reads environmental field data — sensor streams, water-quality
samples, field notes — and turns it into a grounded, honest, source-cited read.
Its defining property is that it is built **not to present a guess as a fact**.

This repository is a **sandbox**: a public stand-in for that engine. The real
interpretation model is proprietary and lives in a private repository. Here, a
small, transparent **mock** implements the same interface, so everything you build
against the sandbox moves onto the real engine unchanged. You do not need access to
the private engine to do a full, excellent capstone.

## Start here

1. **`CONTRACT.md`** — the whole interface: two functions, three shapes. Read it first.
2. **`docs/TRACKS.md`** — the three projects (Console UI, public-data harness, offline app).
3. Run the example and the tests (below).

## Setup (fully local — no API key, no cost)

**Python side (the engine mock, data, example, tests):**

```
python -m venv .venv
.venv\Scripts\activate            # Windows   (mac/linux: source .venv/bin/activate)
pip install -r requirements-dev.txt

python example.py                 # end-to-end: read a dataset -> interpret -> JSON
python -m pytest                  # offline sanity tests
```

The engine mock uses **only the Python standard library** — `requirements.txt` is
empty on purpose. `requirements-dev.txt` adds `pytest` for the tests.

**UI side (Track 1 starting point):**

```
cd console-ui
npm install
npm run dev
```

## Layout

```
CONTRACT.md              the interface — read this first
example.py               runnable end-to-end demo
sandbox_engine/          the MOCK engine (stdlib only; no model, no key)
  schema.py              the three data shapes
  reader.py              read_dataset(): CSV -> DatasetSummary
  interpreter.py         interpret(): DatasetSummary -> InterpretationReport (mock rules)
  fixtures/              a saved sample report (what the UI renders)
data/                    public + synthetic sample datasets (see data/README.md)
console-ui/              Vite + React + TS Interpretation Console scaffold (Track 1)
tests/                   offline pytest sanity checks
docs/TRACKS.md           the three capstone tracks in detail
```

## The open track vs. deeper access

Everything in this sandbox is **open** — start immediately, no paperwork. Going
past the sandbox (the real engine, the private repo, or non-public federal data)
requires each member of that team to sign the project's IP agreement first, which
your faculty mentor coordinates. If Stewardship Compute plans to use your team's
work in the platform, that team signs too — and in return you keep ownership of
your own standalone work and may portfolio it. See `docs/TRACKS.md` for the plain
version. Nothing about starting on the sandbox waits on any of that.

## The one rule

Whatever you build, **always surface `integrity_notes`** — the interpreter's own
statement of what it could not stand behind. Hiding them defeats the entire point
of the platform. It's also a grading axis.

---

Questions on the engine's contract start with `CONTRACT.md`. Build boldly — the
interface keeps the science honest for you.
