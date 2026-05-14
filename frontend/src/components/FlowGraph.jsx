export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case "unacceptable": return "#ff4d4d";
      case "high": return "#ffa500";
      case "limited": return "#ffff00";
      case "minimal": return "#00ff00";
      default: return "#4facfe";
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Autonomous Agent Flow</h2>
        <span className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step">
            <div className="step-number">{index + 1}</div>
            <div className="step-text">{step}</div>
            {index < result.steps.length - 1 && <div className="step-arrow">↓</div>}
          </div>
        ))}
      </div>

      <div className="rationale-section">
        <h3>AI Rationale</h3>
        <p>{result.rationale}</p>
      </div>
    </div>
  );
}
