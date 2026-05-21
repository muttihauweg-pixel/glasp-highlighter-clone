export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    const r = risk?.toLowerCase() || "";
    if (r.includes("unacceptable")) return "risk-unacceptable";
    if (r.includes("high")) return "risk-high";
    if (r.includes("limited")) return "risk-limited";
    if (r.includes("minimal")) return "risk-minimal";
    return "risk-limited";
  };

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Agentic Execution Flow</h2>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, idx) => (
          <div key={idx} className="step-pill">
            <span style={{ opacity: 0.5, marginRight: '10px' }}>0{idx + 1}</span>
            {step}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h2>Governance Rationale</h2>
        <p style={{ color: '#cbd5e1', lineHeight: '1.6' }}>{result.processed_output}</p>
      </div>
    </div>
  );
}
