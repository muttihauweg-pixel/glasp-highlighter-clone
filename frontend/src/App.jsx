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
      <h1 className="main-title">AI Governance OS</h1>
      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && <p className="loading-state">Processing with Gemini 1.5 Pro...</p>}
      {error && <div className="error-panel">Error: {error}</div>}

      {data && (
        <div className="dashboard">
          <FlowGraph result={data.result} />
          <AuditTimeline audit={data.audit} />
          <div className="compliance-report panel">
            <h2>Compliance Rationale</h2>
            <p className="rationale-text">{data.result.rationale}</p>
            <div className="raw-output">
               <h3>Raw Agent Analysis</h3>
               <pre>{data.compliance_report}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
