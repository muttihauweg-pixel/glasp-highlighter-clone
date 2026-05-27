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
      <h2>Agentic Execution Flow</h2>

      <div className="risk-header">
        <span className="badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk} Risk
        </span>
      </div>

      <div className="rationale-box">
        <h3>Governance Rationale</h3>
        <p>{result.rationale}</p>
      </div>

      <div className="execution-steps">
        <h3>Execution Trail</h3>
        <ul>
          {result.steps.map((step, i) => (
            <li key={i} className="step-item">
              <span className="step-number">{i + 1}</span>
              <span className="step-text">{step}</span>
            </li>
          ))}
        </ul>
      </div>

      {result.tool_calls && result.tool_calls.length > 0 && (
        <div className="tools-executed">
          <h3>Autonomous Actions</h3>
          {result.tool_calls.map((call, i) => (
            <div key={i} className="tool-call">
              <code>{call.name}({JSON.stringify(call.params)})</code>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
