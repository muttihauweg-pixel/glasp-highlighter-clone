export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    const r = risk.toLowerCase();
    if (r.includes('unacceptable')) return 'risk-unacceptable';
    if (r.includes('high')) return 'risk-high';
    if (r.includes('limited')) return 'risk-limited';
    if (r.includes('minimal')) return 'risk-minimal';
    return '';
  };

  return (
    <div className="panel glass">
      <h2>
        Agentic Workflow
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk}
        </span>
      </h2>

      <div className="flow-steps">
        {result.steps.map((step, i) => (
          <div key={i} className={`step-chip ${i === result.steps.length - 1 ? 'active' : ''}`}>
            {step}
          </div>
        ))}
      </div>

      <div className="rationale-section">
        <strong>Governance Rationale:</strong>
        <p className="rationale-text">{result.rationale}</p>
      </div>

      <div style={{marginTop: '1.5rem'}}>
        <strong>Final Status:</strong> {result.processed_output}
      </div>
    </div>
  );
}
