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
      <header>
        <h1>AI Governance OS</h1>
        <p className="subtitle">Autonomous EU AI Act Compliance & Guardrails</p>
      </header>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Gemini 1.5 Pro is analyzing autonomous workflows...</p>
        </div>
      )}

      {error && <div className="error-panel">Error: {error}</div>}

      {data && (
        <div className="dashboard">
          <div className="full-width">
            <FlowGraph result={data.result} />
          </div>

          <div className="compliance-report">
            <h2>Detailed Audit Report</h2>
            <pre>{data.compliance_report}</pre>
          </div>

          <AuditTimeline audit={data.audit} />
        </div>
      )}
    </div>
  );
}
