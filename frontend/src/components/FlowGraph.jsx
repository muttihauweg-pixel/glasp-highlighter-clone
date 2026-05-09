export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    switch (risk?.toLowerCase()) {
      case "unacceptable": return "risk-unacceptable";
      case "high": return "risk-high";
      case "limited": return "risk-limited";
      case "minimal": return "risk-minimal";
      default: return "";
    }
  };

  return (
    <div className="panel">
      <h2>
        Governance Execution Flow
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk} Risk
        </span>
      </h2>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
            <div className="step-item">{step}</div>
            {index < result.steps.length - 1 && (
              <span className="step-arrow" style={{ margin: '0 10px' }}>→</span>
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <strong>Model Output Preview:</strong>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem', fontStyle: 'italic', marginTop: '0.5rem' }}>
          "{result.processed_output}"
        </p>
      </div>
    </div>
  );
}
