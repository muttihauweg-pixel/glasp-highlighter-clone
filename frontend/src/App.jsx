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
        <p className="subtitle">Autonomous EU AI Act Compliance Layer</p>
      </header>

      <main className="main-content">
        <InputPanel onSubmit={handleSubmit} disabled={loading} />

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Gemini 1.5 Pro is analyzing your request...</p>
          </div>
        )}

        {error && <div className="error-message">Error: {error}</div>}

        {data && (
          <div className="dashboard-grid">
            <div className="left-col">
              <FlowGraph result={data.result} />
              <AuditTimeline audit={data.audit} />
            </div>
            <div className="right-col">
              <div className="panel compliance-report">
                <h2>Compliance Analysis</h2>
                <div className="report-content">
                  {data.compliance_report}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
