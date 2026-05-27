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
    <div className="app-container">
      <header>
        <h1>AG-OS <span>Governance Dashboard</span></h1>
        <p className="subtitle">Powered by Gemini 1.5 Pro</p>
      </header>

      <main className="main-content">
        <section className="input-section">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />
          {error && <div className="error-panel">Error: {error}</div>}
        </section>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Analyzing Compliance with Autonomous Agents...</p>
          </div>
        )}

        {data && (
          <section className="dashboard-grid">
            <FlowGraph result={data.result} />
            <div className="side-panels">
              <AuditTimeline audit={data.audit} />
              <div className="panel report-panel">
                <h2>Raw Compliance Report</h2>
                <pre>{data.compliance_report}</pre>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
