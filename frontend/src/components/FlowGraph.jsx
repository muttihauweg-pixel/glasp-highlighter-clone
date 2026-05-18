export default function FlowGraph({ result }) {
  return (
    <div className="panel">
      <h2>
        Execution Flow
        <span className={`risk-badge risk-${result.risk}`}>
          {result.risk} RISK
        </span>
      </h2>

      <div className="rationale-text">
        {result.rationale}
      </div>

      <div className="flow-steps">
        {result.steps.map((step, i) => (
          <span key={i} style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <span className="step">{step}</span>
            {i < result.steps.length - 1 && <span className="step-arrow">→</span>}
          </span>
        ))}
      </div>

      <div style={{marginTop: '1.5rem'}}>
        <label style={{color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase'}}>Sanitized Output</label>
        <p style={{marginTop: '0.5rem', color: '#e2e8f0'}}>{result.processed_output}</p>
      </div>
    </div>
  );
}
