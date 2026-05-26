export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'unacceptable': return 'risk-unacceptable';
      case 'high': return 'risk-high';
      case 'limited': return 'risk-limited';
      case 'minimal': return 'risk-minimal';
      default: return '';
    }
  };

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ margin: 0 }}>Agentic Execution Flow</h2>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk} Risk
        </span>
      </div>

      <div className="flow-steps">
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            {step}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <h3 style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Final Policy Decision</h3>
        <div style={{
          padding: '1rem',
          background: 'rgba(255,255,255,0.03)',
          borderLeft: `4px solid var(--risk-${result.risk?.toLowerCase() || 'minimal'})`,
          borderRadius: '0 0.5rem 0.5rem 0'
        }}>
          <p style={{ margin: 0, fontSize: '0.95rem' }}>
            {result.processed_output.split('\n')[0]}...
          </p>
        </div>
      </div>
    </div>
  );
}
