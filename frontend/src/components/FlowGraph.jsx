export default function FlowGraph({ result }) {
  return (
    <div className="glass-panel">
      <div className="status-badge">{result.current_step}</div>
      <div className="output-content">
        {result.processed_output}
      </div>
      <div className="steps-trail">
        <span style={{fontWeight: 600}}>History:</span>
        {result.steps.map((step, index) => (
          <span key={index} className="step-item">{step}</span>
        ))}
      </div>
    </div>
  );
}
