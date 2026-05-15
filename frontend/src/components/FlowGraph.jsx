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
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Governance Execution Flow</h2>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk} Risk
        </span>
      </div>

      <div className="rationale-text">
        {result.rationale}
      </div>

      <div className="flow-container" style={{ marginTop: '1.5rem' }}>
        <h4 style={{ color: '#94a3b8', marginBottom: '0.75rem', fontSize: '0.9rem', textTransform: 'uppercase' }}>
          Agent Execution Steps
        </h4>
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            <div style={{ width: '20px', height: '20px', background: '#3b82f6', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', fontWeight: 'bold' }}>
              {index + 1}
            </div>
            <span>{step}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
