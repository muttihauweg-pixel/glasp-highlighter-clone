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
    setData(null);
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
      <header>
        <div className="logo">🛡️ AG-OS</div>
        <h1>AI Governance Operating System</h1>
        <p className="subtitle">Powered by Gemini 1.5 Pro</p>
      </header>

      <main className="dashboard-grid">
        <section className="input-section">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />

          {error && (
            <div className="error-panel">
              <h3>⚠️ Analysis Error</h3>
              <p>{error}</p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Gemini is performing autonomous governance analysis...</p>
            </div>
          )}
        </section>

        {data && (
          <>
            <div className="main-viz">
              <FlowGraph result={data.result} />
            </div>

            <div className="side-viz">
              <AuditTimeline audit={data.audit} />
              <div className="panel report-panel">
                <h2>Full Agent Output</h2>
                <div className="report-content">
                  <pre>{data.compliance_report}</pre>
                </div>
              </div>
            </div>
          </>
        )}
      </main>

      <footer>
        <p>© 2024 AI Governance OS - Strategic Google AI Hackathon Entry</p>
      </footer>
    </div>
  );
}
