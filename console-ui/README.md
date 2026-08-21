# Console UI scaffold (Track 1 starting point)

Minimal Vite + React + TypeScript app that renders one `InterpretationReport` from
the sandbox mock. It's a starting point, not a finished console — that's your project.

## Run it

```
cd console-ui
npm install
npm run dev
```

Open the URL Vite prints (usually http://localhost:5173).

## What's here

| File | Role |
|---|---|
| `src/App.tsx` | Loads the sample report; where you'll add dataset selection/upload |
| `src/components/InterpretationConsole.tsx` | Renders summary, observations, integrity notes |
| `src/contract.ts` | TypeScript types mirroring `../CONTRACT.md` |
| `src/sample_report.json` | A real mock output to render (regenerate with `python example.py`) |
| `src/styles.css` | Plain starter styling — restyle freely |

## Where to go

Replace the static `sample_report.json` import with a real flow: pick or upload a
dataset, get a report, render it. The shape you receive is always
`InterpretationReport` (see `../CONTRACT.md`), so nothing you build here changes
when the real engine replaces the mock.
