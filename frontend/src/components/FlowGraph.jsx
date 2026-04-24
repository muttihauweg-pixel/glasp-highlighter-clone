export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return '#ff4d4f';
      case 'high': return '#faad14';
      case 'limited': return '#1890ff';
      default: return '#52c41a';
    }
  };

  return (
    <div className="panel flow-panel">
      <h2>Agentic Execution Flow</h2>
      <div className="risk-indicator">
        <strong>Risk Classification:</strong>
        <span className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
          {result.risk}
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className="step-number">{index + 1}</div>
            <div className="step-content">{step}</div>
            {index < result.steps.length - 1 && <div className="step-connector">↓</div>}
          </div>
        ))}
      </div>

      <div className="agent-output">
        <h3>Primary Output Segment</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
