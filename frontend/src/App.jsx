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
      <div style={{ textAlign: 'center' }}>
        <h1>AI Governance OS</h1>
        <p className="subtitle">Autonomous EU AI Act Compliance Layer</p>
      </div>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Gemini 1.5 Pro is analyzing compliance...</p>
        </div>
      )}

      {error && (
        <div className="panel" style={{ borderLeft: '4px solid #ef4444' }}>
          <p style={{ color: '#ef4444', margin: 0 }}><strong>Error:</strong> {error}</p>
        </div>
      )}

      {data && (
        <div className="dashboard">
          <FlowGraph result={data.result} />
          <AuditTimeline audit={data.audit} />
          <div className="compliance-report">
            <h2>Compliance Analysis</h2>
            <pre>{data.compliance_report}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
