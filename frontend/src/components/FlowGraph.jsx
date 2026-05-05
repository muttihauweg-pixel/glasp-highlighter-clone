export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return '#ff4d4d';
      case 'high': return '#ffa500';
      case 'limited': return '#ffff00';
      case 'minimal': return '#00ff00';
      default: return '#4facfe';
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Execution Flow</h2>
        <span className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} RISK
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className="step-dot"></div>
            <div className="step-content">
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="step-line"></div>}
          </div>
        ))}
      </div>

      <div className="agent-output">
        <h3>Primary Analysis Output</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
