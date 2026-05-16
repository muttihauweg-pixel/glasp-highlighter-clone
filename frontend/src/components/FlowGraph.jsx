export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return '#ff4d4d';
      case 'high': return '#ffa500';
      case 'limited': return '#ffff00';
      case 'minimal': return '#00ff00';
      default: return '#ffffff';
    }
  };

  return (
    <div className="panel flow-panel">
      <div className="panel-header">
        <h2>Autonomous Agent Workflow</h2>
        <div
          className="risk-badge"
          style={{ backgroundColor: getRiskColor(result.risk) }}
        >
          {result.risk} RISK
        </div>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-wrapper">
            <div className={`flow-step ${step.startsWith('Tool') ? 'tool-step' : ''}`}>
              <div className="step-number">{index + 1}</div>
              <div className="step-text">{step}</div>
            </div>
            {index < result.steps.length - 1 && <div className="flow-arrow">↓</div>}
          </div>
        ))}
      </div>

      <div className="agent-thought">
        <h3>Agent Rationale</h3>
        <p>{result.processed_output.split('RATIONALE:')[1] || "Compliance evaluation completed by AG-OS governance engine."}</p>
      </div>
    </div>
  );
}
