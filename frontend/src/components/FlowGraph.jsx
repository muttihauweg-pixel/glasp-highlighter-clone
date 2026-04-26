export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    switch (risk.toLowerCase()) {
      case 'minimal': return 'risk-minimal';
      case 'limited': return 'risk-limited';
      case 'high': return 'risk-high';
      case 'unacceptable': return 'risk-unacceptable';
      default: return '';
    }
  };

  return (
    <div className="panel">
      <h2>Execution Flow</h2>
      <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <strong>Risk Level:</strong>
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk}
        </span>
      </div>

      <div className="flow-steps">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step">
            <div className="flow-step-number">{index + 1}</div>
            <div className="flow-step-text">{step}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <strong>Agent Summary:</strong>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '0.5rem' }}>
          {result.processed_output}
        </p>
      </div>
    </div>
  );
}
