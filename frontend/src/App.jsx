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
      <header className="header">
        <h1>🚀 AI Governance OS</h1>
        <p className="subtitle">Real-time EU AI Act Compliance Engine</p>
      </header>

      <div className="main-layout">
        <div className="left-panel">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />
          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Gemini 1.5 Pro is analyzing multimodal content...</p>
            </div>
          )}
          {error && <div className="error-message">❌ Error: {error}</div>}
        </div>

        <div className="right-panel">
          {data ? (
            <div className="dashboard fade-in">
              <FlowGraph result={data.result} />
              <AuditTimeline audit={data.audit} />
              <div className="compliance-report panel">
                <h2>📜 Detailed Compliance Report</h2>
                <div className="report-content">
                  {data.compliance_report}
                </div>
              </div>
            </div>
          ) : !loading && (
            <div className="empty-state">
              <p>Enter a request to begin autonomous governance analysis.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
