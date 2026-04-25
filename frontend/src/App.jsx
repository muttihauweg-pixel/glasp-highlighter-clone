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
  const [currentImage, setCurrentImage] = useState(null);

  const handleSubmit = async (input, image) => {
    setLoading(true);
    setError(null);
    setCurrentImage(image);
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
        <div className="logo-container">
          <span className="logo-icon">🛡️</span>
          <h1>AI Governance OS</h1>
        </div>
        <p className="subtitle">Autonomous Compliance & Safety Layer powered by Gemini 1.5 Pro</p>
      </header>

      <main className="main-content">
        <div className="left-column">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />
          {currentImage && (
            <div className="panel image-preview">
              <h3>Input Image</h3>
              <img
                src={`data:image/png;base64,${currentImage}`}
                alt="Uploaded for analysis"
                style={{ maxWidth: "100%", borderRadius: "8px" }}
              />
            </div>
          )}
        </div>

        <div className="right-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Gemini 1.5 Pro is analyzing compliance...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <h3>⚠️ Error</h3>
              <p>{error}</p>
            </div>
          )}

          {data && (
            <div className="dashboard">
              <FlowGraph result={data.result} />
              <div className="panel compliance-report">
                <h2>🛡️ Governance Analysis Report</h2>
                <div className="report-content">
                  {data.compliance_report}
                </div>
              </div>
              <AuditTimeline audit={data.audit} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
