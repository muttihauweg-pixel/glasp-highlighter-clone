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
    setData(null);
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
        <p className="subtitle">Autonomous EU AI Act Compliance layer powered by Gemini 1.5 Pro</p>
      </header>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-container">
          <div className="loader"></div>
          <p>Analyzing with Gemini 1.5 Pro Agent...</p>
        </div>
      )}

      {error && <div className="error-message">Error: {error}</div>}

      {data && (
        <div className="dashboard animate-in">
          <FlowGraph result={data.result} />
          <AuditTimeline audit={data.audit} />
          <div className="panel compliance-report">
            <h2>Detailed Compliance Analysis</h2>
            <pre>{data.compliance_report}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
