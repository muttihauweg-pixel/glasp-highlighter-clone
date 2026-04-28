export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk) {
      case "Unacceptable": return "#ff4d4d";
      case "High": return "#ffa500";
      case "Limited": return "#ffff00";
      case "Minimal": return "#00ff00";
      default: return "#ffffff";
    }
  };

  return (
    <div className="panel flow-panel">
      <h2>Execution Flow</h2>
      <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
        Risk: {result.risk}
      </div>

      <div className="flow-visual">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-container">
            <div className="flow-step">
              <span className="step-number">{index + 1}</span>
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="flow-arrow">↓</div>}
          </div>
        ))}
      </div>

      <div className="final-output">
        <strong>Action:</strong> {result.processed_output}
      </div>
    </div>
  );
}
