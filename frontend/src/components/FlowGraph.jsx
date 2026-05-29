export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    const r = risk?.toLowerCase() || "";
    if (r.includes("unacceptable")) return "risk-unacceptable";
    if (r.includes("high")) return "risk-high";
    if (r.includes("limited")) return "risk-limited";
    return "risk-minimal";
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Trail</h2>
      <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <strong>Assessed Risk:</strong>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk}
        </span>
      </div>

      {result.rationale && (
        <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
          <strong>Rationale:</strong>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.95rem', color: '#94a3b8' }}>{result.rationale}</p>
        </div>
      )}

      <div className="flow-container">
        <strong>Execution Path:</strong>
        <div style={{ marginTop: '1.5rem' }}>
          {result.steps.map((step, index) => (
            <div key={index} className="flow-step">
              <div className="step-icon"></div>
              <div className="step-label">{step}</div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem' }}>
        <p><strong>Final Status:</strong> {result.processed_output}</p>
      </div>
    </div>
  );
}
