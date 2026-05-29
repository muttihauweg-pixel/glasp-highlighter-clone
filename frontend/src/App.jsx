import { useState } from "react";
import { processListing } from "./api";
import InputPanel from "./components/InputPanel";
import FlowGraph from "./components/FlowGraph";
import "./App.css";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (text, image) => {
    setLoading(true);
    setError(null);
    try {
      const res = await processListing(text, image);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>eBay Verkaufs-Experte 🚀</h1>
      <p className="subtitle">Verkaufe wie ein Profi mit psychologischer Preisstrategie & Foto-Regie</p>

      <InputPanel onSubmit={handleSubmit} disabled={loading} />

      {loading && <div className="loading-spinner">🧠 Die KI-Agenten arbeiten für dich...</div>}

      {error && <div style={{color: 'red', textAlign: 'center', marginBottom: '1rem'}}>
        Fehler: {error}
      </div>}

      {data && (
        <div className="dashboard">
          <FlowGraph result={data.result} />

          <p style={{fontSize: '0.8rem', textAlign: 'center', color: '#999'}}>
            ID: {data.audit.hash.substring(0, 10)} | {new Date(data.audit.timestamp).toLocaleString("de-DE")}
          </p>
        </div>
      )}
    </div>
  );
}
