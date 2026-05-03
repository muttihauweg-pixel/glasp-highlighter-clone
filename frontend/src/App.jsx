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

  const handleSubmit = async (input, imageData) => {
    setLoading(true);
    setError(null);
    try {
      const res = await processInput(input, imageData);
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

      {loading && <p>Processing with Gemini 1.5 Pro...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}

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
