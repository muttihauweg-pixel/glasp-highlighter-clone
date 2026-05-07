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
      <h2>Agentic Execution Flow</h2>
      <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
        Risk Level: {result.risk}
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className="step-content">
              <span className="step-number">{index + 1}</span>
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="flow-connector">↓</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
