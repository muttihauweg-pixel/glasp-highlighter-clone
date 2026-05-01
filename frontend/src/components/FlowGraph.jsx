export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'unacceptable': return '#ff4444';
      case 'high': return '#ffbb33';
      case 'limited': return '#00C851';
      case 'minimal': return '#33b5e5';
      default: return '#ffffff';
    }
  };

  return (
    <div className="panel">
      <h2>Autonomous Agent Workflow</h2>
      <div className="risk-badge" style={{
        backgroundColor: getRiskColor(result.risk),
        padding: '5px 15px',
        borderRadius: '20px',
        display: 'inline-block',
        marginBottom: '15px',
        fontWeight: 'bold',
        color: '#000'
      }}>
        RISK: {result.risk.toUpperCase()}
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-item">
            <div className={`step-node ${step.includes('Tool') ? 'tool-node' : ''}`}>
              {index + 1}. {step}
            </div>
            {index < result.steps.length - 1 && <div className="flow-connector">↓</div>}
          </div>
        ))}
      </div>

      <div className="output-summary" style={{ marginTop: '20px', borderTop: '1px solid #444', paddingTop: '10px' }}>
        <strong>Execution Summary:</strong>
        <p>{result.processed_output}</p>
      </div>
    </div>
  );
}
