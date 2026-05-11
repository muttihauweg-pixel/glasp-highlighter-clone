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
    <div className="panel glass">
      <div className="flow-header">
        <h2>Execution Flow</h2>
        <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} Risk
        </div>
      </div>

      <div className="steps-container">
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            <div className="step-dot"></div>
            <div className="step-text">{step}</div>
            {index < result.steps.length - 1 && <div className="step-line"></div>}
          </div>
        ))}
      </div>

      <div className="rationale-box">
        <h3>Governance Rationale</h3>
        <p>{result.rationale}</p>
      </div>

      <div className="output-box">
        <h3>Final Decision</h3>
        <code>{result.processed_output}</code>
      </div>
    </div>
  );
}
