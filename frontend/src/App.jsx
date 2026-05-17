import { useState } from "react";
import { processInput } from "./api";
import InputPanel from "./components/InputPanel";
import FlowGraph from "./components/FlowGraph";
import AuditTimeline from "./components/AuditTimeline";
import "./App.css";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (input, image) => {
    setLoading(true);
    setError(null);
    setData(null); // Clear previous results
    try {
      const res = await processInput(input, image);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Governance OS</h1>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          Analyzing with Gemini 1.5 Pro Autonomous Agent...
        </div>
      )}

      {error && (
        <div className="error-panel">
          <strong>Governance Analysis Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="dashboard">
          <FlowGraph result={data.result} />
          <AuditTimeline audit={data.audit} />
          <div className="panel compliance-report-full">
            <h2>Full Compliance Report (LLM Raw)</h2>
            <pre>{data.compliance_report}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
