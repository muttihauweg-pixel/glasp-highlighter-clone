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
    <div className="container app-wrapper">
      <header>
        <h1 className="main-title">AI Governance OS</h1>
        <p className="subtitle">Autonomous Compliance & Ethical Guardrails for the Agentic Era</p>
      </header>

      <main className="content">
        <section className="left-panel">
          <InputPanel onSubmit={handleSubmit} disabled={loading} />
          {error && <div className="error-panel">Error: {error}</div>}
          {data && <AuditTimeline audit={data.audit} />}
        </section>

        <section className="right-panel">
          {!data && !loading && (
            <div className="placeholder-state">
              <p>Ready to analyze. Submit a request to see the governance flow.</p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Gemini 1.5 Pro is analyzing compliance requirements...</p>
            </div>
          )}

          {data && (
            <div className="dashboard-results">
              <FlowGraph result={data.result} />
              <div className="panel raw-report-panel">
                <h2>Full Governance Report</h2>
                <pre className="report-text">{data.compliance_report}</pre>
              </div>
            </div>
          )}
        </section>
      </main>

      <footer>
        <p>Built with Gemini 1.5 Pro & Vertex AI</p>
      </footer>
    </div>
  );
}
