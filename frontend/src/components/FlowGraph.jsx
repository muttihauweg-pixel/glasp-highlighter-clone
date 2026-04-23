export default function FlowGraph({ result }) {
  const agentRoles = [
    { role: "Manager", status: "Planning & Policy Selection", color: "#4285F4" },
    { role: "Worker", status: "Risk Assessment & Analysis", color: "#34A853" },
    { role: "Reviewer", status: "Final Governance Validation", color: "#FBBC05" }
  ];

  return (
    <div className="panel">
      <h2>Agentic Execution Flow</h2>
      <div className="agent-flow-container" style={{ display: "flex", justifyContent: "space-between", margin: "20px 0" }}>
        {agentRoles.map((agent, index) => (
          <div key={agent.role} className="agent-card" style={{
            border: `2px solid ${agent.color}`,
            borderRadius: "8px",
            padding: "10px",
            width: "30%",
            textAlign: "center"
          }}>
            <h3 style={{ color: agent.color }}>{agent.role}</h3>
            <p style={{ fontSize: "0.8em" }}>{agent.status}</p>
            <div className="status-indicator" style={{
              backgroundColor: agent.color,
              height: "4px",
              width: "100%",
              marginTop: "5px"
            }}></div>
          </div>
        ))}
      </div>

      <p><strong>Risk Level:</strong> <span style={{ color: result.risk === "High" ? "red" : "green" }}>{result.risk}</span></p>
      <div className="flow-steps">
        <strong>Linear Steps:</strong> {result.steps.join(" → ")}
      </div>
      <div className="output-box" style={{ background: "#f0f0f0", padding: "10px", borderRadius: "4px", marginTop: "10px" }}>
        <strong>Output:</strong> {result.processed_output}
      </div>
    </div>
  );
}
