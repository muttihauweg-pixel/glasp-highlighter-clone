export default function FlowGraph({ result }) {
  const isHighRisk = result.risk.toLowerCase() === "high";

  return (
    <div className="panel full-width">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Agent Execution Logic</h2>
        <span className={`risk-badge ${isHighRisk ? 'risk-high' : 'risk-low'}`}>
          {result.risk} Risk Detected
        </span>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className={`step-card ${step.includes('Tool') ? 'tool' : ''}`}>
            {index + 1}. {step}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <h3>Final Governance Output</h3>
        <p style={{ background: '#020617', padding: '1rem', borderRadius: '8px', border: '1px solid #1e293b' }}>
          {result.processed_output}
        </p>
      </div>
    </div>
  );
}
