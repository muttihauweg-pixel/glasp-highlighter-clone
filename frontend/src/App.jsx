import { useState } from "react";
import { processInput } from "./api";
import InputPanel from "./components/InputPanel";
import FlowGraph from "./components/FlowGraph";
import "./App.css";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (input) => {
    setLoading(true);
    setError(null);
    try {
      const res = await processInput(input);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Happy eBay Assi 🌈</h1>
      <p className="subtitle">"Dein fröhlicher persönlicher Shopper für eBay"</p>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && <div className="loading-text">✨ Gemini 1.5 Pro sucht nach Freude... ✨</div>}
      {error && <div className="error-msg">Hoppla! Sogar Assistenten haben mal einen schlechten Tag: {error}</div>}

      {data && (
        <div className="dashboard">
          <FlowGraph result={data.result} />

          <div className="panel">
            <h2>✨ Empfehlungen</h2>
            <div className="compliance-report">
              {data.result.processed_output}
            </div>
          </div>

          <div className="audit-info">
            Fröhliche Audit-ID: {data.audit.hash.substring(0, 12)}... | {new Date(data.audit.timestamp).toLocaleString("de-DE")}
          </div>
        </div>
      )}
    </div>
  );
}
