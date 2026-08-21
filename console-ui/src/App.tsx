import type { InterpretationReport } from "./contract";
import { InterpretationConsole } from "./components/InterpretationConsole";
import sampleReport from "./sample_report.json";

// The scaffold loads one static report (produced by the sandbox mock) so you have
// something real on screen from minute one. Your Track 1 job is to grow this into a
// usable console: let a researcher pick or upload a dataset, call the engine, and
// render the result well. Swap this import for a fetch()/upload flow when you're ready
// — the shape you receive is InterpretationReport either way (see ../CONTRACT.md).
const report = sampleReport as InterpretationReport;

export default function App() {
  return (
    <main className="page">
      <header className="page__header">
        <h1>Interpretation Console</h1>
        <p className="page__subtitle">Capstone sandbox &middot; Track 1 starting point</p>
      </header>
      <InterpretationConsole report={report} />
      <footer className="page__footer">
        Data and interpretation shown here come from the public <strong>sandbox mock</strong>,
        not the real Stewardship AI engine. Build to the contract; the real engine slots in behind it.
      </footer>
    </main>
  );
}
