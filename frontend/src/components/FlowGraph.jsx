export default function FlowGraph({ result }) {
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case "unacceptable": return "#ff4d4d";
      case "high": return "#ffa64d";
      case "limited": return "#ffff4d";
      case "minimal": return "#4dff4d";
      default: return "#ffffff";
    }
  };

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>
      <div className="risk-badge" style={{
        backgroundColor: getRiskColor(result.risk),
        padding: "10px",
        borderRadius: "4px",
        color: "#000",
        fontWeight: "bold",
        textAlign: "center",
        marginBottom: "20px"
      }}>
        RISK LEVEL: {result.risk.toUpperCase()}
      </div>

      <div className="flow-container">
        {result.steps.map((step, index) => (
          <div key={index} className="flow-step-wrapper">
            <div className="flow-step">
              <span className="step-number">{index + 1}</span>
              <span className="step-text">{step}</span>
            </div>
            {index < result.steps.length - 1 && <div className="flow-arrow">↓</div>}
          </div>
        ))}
      </div>

      <div className="processed-output" style={{ marginTop: "20px", padding: "10px", backgroundColor: "#1e1e1e", borderRadius: "4px" }}>
        <strong>Action taken:</strong> {result.processed_output}
      </div>
    </div>
  );
}
