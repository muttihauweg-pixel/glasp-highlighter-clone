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
        <div className="logo">🛡️ AG-OS</div>
        <h1>AI Governance Operating System</h1>
        <p className="subtitle">Real-time Compliance & Safety Layer for Enterprise AI</p>
      </header>

      <main className="main-content">
        <InputPanel onSubmit={handleSubmit} disabled={loading} />

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Gemini 1.5 Pro is analyzing compliance...</p>
          </div>
        )}

        {error && <div className="error-message">⚠️ Error: {error}</div>}

        {data && (
          <div className="dashboard">
            <div className="dashboard-grid">
              <FlowGraph result={data.result} />
              <div className="side-panels">
                <AuditTimeline audit={data.audit} />
                <div className="panel glass compliance-report">
                  <h2>Compliance Analysis Report</h2>
                  <div className="report-content">
                    {data.compliance_report}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer>
        Built with Gemini 1.5 Pro on Google Cloud
      </footer>
    </div>
  );
}
