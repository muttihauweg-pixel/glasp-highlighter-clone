export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toUpperCase()) {
      case 'UNACCEPTABLE': return '#ff4d4d';
      case 'HIGH': return '#ffa333';
      case 'LIMITED': return '#ffcc00';
      case 'MINIMAL': return '#00e676';
      default: return '#4facfe';
    }
  };

  return (
    <div className="panel glass">
      <div className="panel-header">
        <h2>Agentic Execution Flow</h2>
        <span
          className="risk-badge"
          style={{ backgroundColor: getRiskColor(result.risk) }}
        >
          {result.risk} RISK
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-item">
            <div className="step-number">{index + 1}</div>
            <div className="step-text">{step}</div>
            {index < result.steps.length - 1 && <div className="step-arrow">↓</div>}
          </div>
        ))}
      </div>

      <div className="output-preview">
        <h3>Primary Determination</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
