export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case "unacceptable": return "#ff4d4d";
      case "high": return "#ffa500";
      case "limited": return "#ffff00";
      case "minimal": return "#00ff00";
      default: return "#aaa";
    }
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>

      <div className="risk-badge-container" style={{ marginBottom: "20px" }}>
        <span
          className="risk-badge"
          style={{
            backgroundColor: getRiskColor(result.risk),
            color: result.risk.toLowerCase() === 'limited' ? 'black' : 'white',
            padding: "5px 15px",
            borderRadius: "20px",
            fontWeight: "bold",
            textTransform: "uppercase"
          }}
        >
          {result.risk} Risk
        </span>
      </div>

      <div className="rationale-box" style={{ marginBottom: "20px", fontStyle: "italic", color: "#ccc" }}>
        <strong>Rationale:</strong> {result.rationale}
      </div>

      <div className="flow-steps-container">
        <h3>Governance Steps</h3>
        <div className="steps-list" style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {result.steps.map((step, index) => (
            <div key={index} className="step-item" style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div className="step-number" style={{
                width: "24px",
                height: "24px",
                borderRadius: "50%",
                border: "2px solid #4f46e5",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "12px"
              }}>
                {index + 1}
              </div>
              <div className="step-text">{step}</div>
              {index < result.steps.length - 1 && <div className="step-line" style={{ height: "20px", borderLeft: "2px dashed #444", position: "absolute", left: "11px", marginTop: "35px" }}></div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
