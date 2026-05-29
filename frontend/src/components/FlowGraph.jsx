export default function FlowGraph({ result }) {
  return (
    <div className="panel">
      <div className="status-badge">Aktueller Schritt: {result.current_step}</div>
      <div className="output-content">
        {result.processed_output}
      </div>
      <div className="steps-trail">
        Prozess: {result.steps.join(" ➔ ")}
      </div>
    </div>
  );
}
