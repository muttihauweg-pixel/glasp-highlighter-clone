export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'unacceptable': return '#ff4d4d';
      case 'high': return '#ffa500';
      case 'limited': return '#ffff00';
      case 'minimal': return '#00ff00';
      default: return '#4facfe';
    }
  };

  return (
    <div className="panel flow-panel">
      <div className="panel-header">
        <h2>Agentic Execution Flow</h2>
        <span className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className="step-node">
              <div className="node-circle"></div>
              <div className="node-label">{step}</div>
            </div>
            {index < result.steps.length - 1 && <div className="step-connector"></div>}
          </div>
        ))}
      </div>

      <div className="result-rationale">
        <h3>Governance Rationale</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
