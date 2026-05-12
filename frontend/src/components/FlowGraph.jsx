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
    <div className="panel flow-panel">
      <div className="risk-header">
        <h2>Agentic Execution Flow</h2>
        <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} RISK
        </div>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-node-wrapper">
            <div className="flow-node">
              {step.startsWith("Action:") ? (
                <span className="action-step">⚙️ {step.replace("Action: ", "")}</span>
              ) : (
                <span>{step}</span>
              )}
            </div>
            {index < result.steps.length - 1 && <div className="flow-connector"></div>}
          </div>
        ))}
      </div>

      <div className="output-summary">
        <strong>System Integrity Check:</strong> {result.processed_output}
      </div>
    </div>
  );
}
