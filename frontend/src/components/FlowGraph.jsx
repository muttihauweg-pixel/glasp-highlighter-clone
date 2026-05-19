export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    const r = risk.toLowerCase();
    if (r.includes("unacceptable")) return "#ff4d4d";
    if (r.includes("high")) return "#ffa500";
    if (r.includes("limited")) return "#ffff00";
    if (r.includes("minimal")) return "#00ff00";
    return "#4facfe";
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>
      <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
        Risk Level: {result.risk}
      </div>

      <div className="rationale-box">
        <strong>Rationale:</strong>
        <p>{result.rationale}</p>
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step">
            <div className="step-number">{index + 1}</div>
            <div className="step-text">{step}</div>
            {index < result.steps.length - 1 && <div className="flow-arrow">↓</div>}
          </div>
        ))}
      </div>

      {result.tool_calls && result.tool_calls.length > 0 && (
        <div className="tool-calls-section">
          <h3>Autonomous Actions Taken:</h3>
          <ul>
            {result.tool_calls.map((call, idx) => (
              <li key={idx} className="tool-call-item">
                <code>{call.action}</code>
                <pre>{JSON.stringify(call.parameters, null, 2)}</pre>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
