export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return 'risk-unacceptable';
      case 'high': return 'risk-high';
      case 'limited': return 'risk-limited';
      case 'minimal': return 'risk-minimal';
      default: return '';
    }
  };

  return (
    <div className="panel flow-graph">
      <h2>Governance Intelligence</h2>

      <div className={`risk-badge ${getRiskClass(result.risk)}`}>
        {result.risk} Risk Identified
      </div>

      <div className="rationale-box">
        {result.rationale}
      </div>

      <div className="flow-steps">
        <h3>Autonomous Agent Execution Flow</h3>
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            {step}
          </div>
        ))}
      </div>

      <div className="processed-summary">
        <h3>Final Output Summary</h3>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
