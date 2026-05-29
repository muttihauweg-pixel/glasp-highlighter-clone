export default function FlowGraph({ result }) {
  return (
    <div className="panel">
      <h2>🌈 Überlegungen des Assistenten</h2>
      <div className="joy-meter">
        <strong>Glücksfaktor:</strong>
        <span className="joy-badge">{result.joy_score}%</span>
      </div>
      <p><strong>BEGRÜNDUNG:</strong> {result.rationale}</p>
      <div className="flow-steps">
        <strong>Ausführungspfad:</strong> {result.steps.join(" ✨ ")}
      </div>
    </div>
  );
}
