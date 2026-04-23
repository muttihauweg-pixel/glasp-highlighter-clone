export default function FlowGraph({ result }) {
  return (
    <div className="panel">
      <h2>Execution Flow</h2>
      <p><strong>Risk Level:</strong> {result.risk}</p>
      <div className="flow-steps">
        <strong>Steps:</strong> {result.steps.join(" → ")}
      </div>
      <p><strong>Output:</strong> {result.processed_output}</p>
    </div>
  );
}
