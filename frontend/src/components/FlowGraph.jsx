export default function FlowGraph({ result }) {
  const getRiskClass = (risk) => {
    const r = risk?.toLowerCase() || "";
    if (r.includes("unacceptable")) return "risk-unacceptable";
    if (r.includes("high")) return "risk-high";
    if (r.includes("limited")) return "risk-limited";
    return "risk-minimal";
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>
      <div style={{ marginBottom: "20px" }}>
        <strong>System Risk Level:</strong>{" "}
        <span className={`risk-badge ${getRiskClass(result.risk)}`}>
          {result.risk}
        </span>
      </div>

      <div className="flow-steps">
        {result.steps.map((step, index) => (
          <div key={index} className="step-item">
            <div className="step-badge"></div>
            <span>{step}</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: "20px" }}>
        <strong>Current Status:</strong>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
          {result.processed_output}
        </p>
      </div>
    </div>
  );
}
