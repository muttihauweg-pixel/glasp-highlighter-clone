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

  const handleSubmit = async (inputData) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const res = await processInput(inputData);
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
        <p className="subtitle">Autonomous EU AI Act Compliance & Orchestration</p>
      </header>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          Proactively Analyzing Governance Policies with Gemini 1.5 Pro...
        </div>
      )}

      {error && (
        <div className="panel" style={{ borderColor: '#ef4444' }}>
          <p style={{ color: '#ef4444', margin: 0 }}><strong>Error:</strong> {error}</p>
        </div>
      )}

      {data && (
        <div className="dashboard">
          <div className="main-content">
            <FlowGraph result={data.result} />
            <div className="panel compliance-report" style={{ marginTop: '2rem' }}>
              <h2>Full Governance Report</h2>
              <pre>{data.compliance_report}</pre>
            </div>
          </div>
          <aside>
            <AuditTimeline audit={data.audit} />
          </aside>
        </div>
      )}
    </div>
  );
}
