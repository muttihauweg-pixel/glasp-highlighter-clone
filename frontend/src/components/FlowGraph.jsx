export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch(risk) {
      case 'Unacceptable': return '#ff4d4d';
      case 'High': return '#ffa500';
      case 'Limited': return '#ffff00';
      case 'Minimal': return '#00ff00';
      default: return '#fff';
    }
  };

  return (
    <div className="panel">
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
              <div className="node-icon"></div>
              <div className="node-label">{step}</div>
            </div>
            {index < result.steps.length - 1 && <div className="step-connector"></div>}
          </div>
        ))}
      </div>

      <div className="processed-output-box">
        <h3>Final Agent Verdict</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
