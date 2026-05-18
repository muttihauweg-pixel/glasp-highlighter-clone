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

  const handleSubmit = async (text, image) => {
    setLoading(true);
    setError(null);
    try {
      const res = await processInput(text, image);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end'}}>
        <div>
          <h1>AG-OS</h1>
          <p style={{color: '#64748b', fontSize: '1.2rem', margin: '0.5rem 0 0 0'}}>AI Governance Operating System</p>
        </div>
        <div style={{textAlign: 'right', color: '#475569', fontSize: '0.9rem'}}>
          Powered by Gemini 1.5 Pro<br/>
          v1.0.0-Hackathon
        </div>
      </div>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <span>Gemini is autonomously evaluating compliance policies...</span>
        </div>
      )}

      {error && (
        <div className="panel" style={{borderColor: '#ef4444', background: 'rgba(239, 68, 68, 0.1)'}}>
          <h2 style={{color: '#ef4444'}}>Analysis Failed</h2>
          <p>{error}</p>
        </div>
      )}

      {data && (
        <div className="dashboard">
          <div className="full-width">
             <FlowGraph result={data.result} />
          </div>

          <AuditTimeline audit={data.audit} />

          <div className="panel compliance-report">
            <h2>Detailed Report</h2>
            <pre>{data.compliance_report}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
