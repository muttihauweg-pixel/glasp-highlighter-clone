export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'unacceptable': return '#ff4d4d';
      case 'high': return '#ffa500';
      case 'limited': return '#ffff00';
      case 'minimal': return '#00ff00';
      default: return '#94a3b8';
    }
  };

  const riskColor = getRiskColor(result.risk);

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ margin: 0 }}>Agentic Execution Flow</h2>
        <span className="risk-badge" style={{ backgroundColor: `${riskColor}22`, color: riskColor, border: `1px solid ${riskColor}` }}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-steps">
        {result.steps.map((step, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
            <span className="step-badge">{step}</span>
            {index < result.steps.length - 1 && <span style={{ margin: '0 0.5rem', color: '#475569' }}>→</span>}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', borderLeft: `4px solid ${riskColor}` }}>
        <strong style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Governance Rationale</strong>
        <p style={{ margin: '0.5rem 0 0 0', lineHeight: 1.6 }}>{result.processed_output}</p>
      </div>
    </div>
  );
}
