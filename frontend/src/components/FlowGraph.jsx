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
    <div className="panel glass flow-panel">
      <div className="panel-header">
        <h2>Autonomous Agent Flow</h2>
        <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} RISK
        </div>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className="step-number">{index + 1}</div>
            <div className="step-content">
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="step-connector"></div>}
          </div>
        ))}
      </div>

      <div className="processed-output">
        <label>System Output Prediction</label>
        <code>{result.processed_output}</code>
      </div>
    </div>
  );
}
