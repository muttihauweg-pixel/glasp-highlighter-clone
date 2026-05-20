export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return '#ff4d4d';
      case 'high': return '#ffa500';
      case 'limited': return '#ffff00';
      case 'minimal': return '#00ff00';
      default: return '#fff';
    }
  };

  return (
    <div className="panel flow-panel">
      <h2>Agentic Execution Flow</h2>

      <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
        RISK: {result.risk.toUpperCase()}
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step">
            <div className="step-node">
              <span className="step-number">{index + 1}</span>
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="step-connector"></div>}
          </div>
        ))}
      </div>

      <div className="rationale-box">
        <h3>Governance Rationale</h3>
        <p>{result.rationale}</p>
      </div>

      <div className="output-status">
        <strong>System Status:</strong> {result.processed_output}
      </div>
    </div>
  );
}
