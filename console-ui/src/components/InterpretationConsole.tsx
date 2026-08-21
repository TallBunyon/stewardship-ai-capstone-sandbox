import type { InterpretationReport, Severity } from "../contract";

const SEVERITY_LABEL: Record<Severity, string> = {
  info: "Info",
  watch: "Watch",
  concern: "Concern",
};

export function InterpretationConsole({ report }: { report: InterpretationReport }) {
  return (
    <section className="console">
      <div className="console__meta">
        <span className="tag">source: {report.source}</span>
        <span className="tag">dataset: {report.dataset_filename}</span>
      </div>

      <h2>Summary</h2>
      <p className="console__summary">{report.summary_text}</p>

      <h2>Observations</h2>
      {report.observations.length === 0 ? (
        <p className="muted">No observations.</p>
      ) : (
        <ul className="observations">
          {report.observations.map((o, i) => (
            <li key={i} className={`observation observation--${o.severity}`}>
              <span className={`badge badge--${o.severity}`}>{SEVERITY_LABEL[o.severity]}</span>
              <div>
                <p className="observation__statement">{o.statement}</p>
                <p className="observation__evidence">{o.evidence}</p>
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* The integrity notes are the point of the platform: an interpreter that will not
          present a guess as a fact. Always render them; never hide them. */}
      <h2>Integrity notes</h2>
      <ul className="integrity">
        {report.integrity_notes.map((n, i) => (
          <li key={i}>{n}</li>
        ))}
      </ul>

      {report.sources_consulted.length > 0 && (
        <>
          <h2>Sources consulted</h2>
          <ul className="sources">
            {report.sources_consulted.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
