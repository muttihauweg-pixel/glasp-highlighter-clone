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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ margin: 0 }}>Agentic Workflow</h2>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-graph">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-node">
            <div className="node-number">{index + 1}</div>
            <div className="node-label">{step}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(56, 189, 248, 0.05)', borderRadius: '8px', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#38bdf8' }}>
          <strong>System Action:</strong> {result.processed_output}
        </p>
      </div>
    </div>
  );
}
