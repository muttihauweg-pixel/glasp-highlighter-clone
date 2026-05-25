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
        <p className="subtitle">Autonomous EU AI Act Compliance & Risk Orchestration</p>
      </header>

      <main>
        <div className="input-section">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />
        </div>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Gemini 1.5 Pro is analyzing compliance vectors...</p>
          </div>
        )}

        {error && (
          <div className="error-panel">
            <strong>Analysis Failed:</strong> {error}
          </div>
        )}

        {data && (
          <div className="dashboard fade-in">
            <div className="dashboard-grid">
              <FlowGraph result={data.result} />
              <AuditTimeline audit={data.audit} />
            </div>

            <div className="compliance-report panel">
              <h2>Full Governance Report</h2>
              <div className="report-content">
                <pre>{data.compliance_report}</pre>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>Built with Gemini 1.5 Pro & Vertex AI | Google for Startups AI Agents Challenge</p>
      </footer>
    </div>
  );
}
