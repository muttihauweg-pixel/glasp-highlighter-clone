export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    switch (risk.toLowerCase()) {
      case "unacceptable": return "risk-unacceptable";
      case "high": return "risk-high";
      case "limited": return "risk-limited";
      default: return "risk-minimal";
    }
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>

      <div className={`risk-badge ${getRiskClass(result.risk)}`}>
        {result.risk} RISK IDENTIFIED
      </div>

      <div className="execution-trail">
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            <div className="step-dot"></div>
            <span className="step-text">{step}</span>
          </div>
        ))}
      </div>

      <div className="agent-action-box">
         <p><strong>Status:</strong> Autonomous governance loop concluded.</p>
      </div>
    </div>
  );
}
