import { useState } from "react";
import { processListing } from "./api";
import InputPanel from "./components/InputPanel";
import Login from "./components/Login";
import FlowGraph from "./components/FlowGraph";
import "./App.css";

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState("Vorschau");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} />;
  }

  const handleSubmit = async (text, image, video) => {
    setLoading(true);
    setError(null);
    try {
      const res = await processListing(text, image, video);
      setData(res);
      setActiveTab("Agenten"); // Switch to results
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const agents = [
    { name: "Foto-Regisseur", icon: "📸", color: "#ec4899", status: "Fertig", score: 92, checks: ["Hintergrund entfernt", "Beleuchtung optimiert", "Fokus auf Details"] },
    { name: "Preis-Psychologe", icon: "💰", color: "#8b5cf6", status: "Fertig", score: 88, checks: ["Konkurrenz-Analyse", "Schwellenpreis gewählt", "Zustand berücksichtigt"] },
    { name: "Copywriting-Profi", icon: "✍️", color: "#3b82f6", status: "Fertig", score: 95, checks: ["Keywords integriert", "Vorteile hervorgehoben", "CTA hinzugefügt"] },
    { name: "Rechtsschutz-Agent", icon: "⚖️", color: "#10b981", status: "Fertig", score: 100, checks: ["AGB-konform", "Haftungsausschluss", "Versandinfos korrekt"] }
  ];

  return (
    <div className="app-container fade-in">
      <div className="hero-card glass-panel" onClick={() => setActiveTab("Bearbeiten")}>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <div style={{maxWidth: '70%'}}>
            <h2 style={{margin: '0 0 10px 0', fontSize: '1.5rem'}}>Foto/Video machen →<br/>Fertige eBay-Anzeige!</h2>
            <p style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>5 KI-Agenten erstellen automatisch<br/>Titel, Preis & Rechtsklausel</p>
            <button className="btn-primary" style={{marginTop: '15px', padding: '8px 20px', borderRadius: '10px'}}>🚀 Jetzt starten</button>
          </div>
          <img src="/hippy_mascot.jpg" alt="Hippy" className="float" style={{width: '120px', height: '120px', borderRadius: '20px', objectFit: 'cover'}} />
        </div>
      </div>

      <header className="header-bar">
        <div className="logo-section">
          <img src="/hippy_mascot.jpg" alt="Logo" style={{width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover'}} className="shake" />
          <div style={{fontWeight: 'bold', fontSize: '1.2rem', marginLeft: '12px'}}>HIPPY <span style={{color: 'var(--accent-purple)', fontSize: '0.8rem', display: 'block', fontWeight: '500'}}>eBay Assistent</span></div>
        </div>

        <nav className="tabs-nav">
          {["Vorschau", "Bearbeiten", "Agenten"].map(tab => (
            <button
              key={tab}
              className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>

        <div className="action-btns">
          <button className="tab-btn btn-secondary">Kopieren</button>
          <button className="tab-btn btn-primary">Speichern</button>
        </div>
      </header>

      <main className="main-content">
        {activeTab === "Bearbeiten" && (
          <div className="glass-panel fade-in">
            <InputPanel onSubmit={handleSubmit} disabled={loading} />
          </div>
        )}

        {activeTab === "Vorschau" && (
          <div className="progress-container fade-in">
            {!data && (
              <div style={{textAlign: 'center', marginBottom: '30px'}}>
                <img src="/hippy_mascot.jpg" alt="Hippy" className="float" style={{width: '150px', height: '150px', borderRadius: '50%', marginBottom: '20px', objectFit: 'cover'}} />
                <h2 style={{margin: 0}}>Hallo! Ich bin Hippy! 👋</h2>
                <p style={{color: 'var(--text-secondary)'}}>Noch keine Anzeigen erstellt. Mach ein Foto oder Video von deinem Produkt – ich erledige den Rest!</p>
                <button className="btn-primary" onClick={() => setActiveTab("Bearbeiten")} style={{padding: '12px 30px', borderRadius: '12px', marginTop: '10px'}}>🎬 Erste Anzeige erstellen</button>
              </div>
            )}
            {data && (
              <div style={{width: '100%', textAlign: 'left'}}>
                <div style={{display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px'}}>
                  <div className="circular-progress" style={{flexShrink: 0}}>
                    <span className="progress-value">94%</span>
                  </div>
                  <div>
                    <h2 style={{margin: '0 0 5px 0'}}>Joy Score: Hoch</h2>
                    <p style={{color: 'var(--text-secondary)', margin: 0}}>Deine Anzeige ist bereit für eBay! ✨</p>
                  </div>
                </div>

                <div className="glass-panel" style={{background: 'rgba(255,255,255,0.05)', padding: '25px', borderRadius: '20px'}}>
                  <h3 style={{color: 'var(--accent-purple)', marginTop: 0, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '10px'}}>Optimierte eBay-Anzeige</h3>
                  <div style={{whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '1rem', color: '#e2e8f0'}}>
                    {data.result.processed_output}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "Agenten" && (
          <div className="agent-grid fade-in">
            {data && (
              <div style={{gridColumn: '1 / -1', marginBottom: '20px'}}>
                <FlowGraph result={data.result} />
              </div>
            )}
            {agents.map(agent => (
              <div key={agent.name} className="agent-card">
                <div className="agent-header">
                  <div className="agent-icon" style={{background: `${agent.color}22`, color: agent.color}}>
                    {agent.icon}
                  </div>
                  <div style={{flexGrow: 1}}>
                    <div style={{fontWeight: 'bold'}}>{agent.name}</div>
                    <div className="status-badge" style={{color: agent.color}}>{agent.status}</div>
                  </div>
                  <div style={{fontWeight: 'bold', color: agent.color}}>{agent.score}%</div>
                </div>
                <ul className="checklist">
                  {agent.checks.map(check => (
                    <li key={check} className="checklist-item">
                      <span className="check-icon">✓</span>
                      {check}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {loading && (
          <div className="glass-panel" style={{textAlign: 'center', marginTop: '20px'}}>
            <img src="/hippy_mascot.jpg" alt="Loading" className="shake" style={{width: '80px', height: '80px', borderRadius: '50%', marginBottom: '10px', objectFit: 'cover'}} />
            <div>Hippy analysiert dein Produkt...</div>
          </div>
        )}

        {error && (
          <div className="glass-panel" style={{borderColor: '#ef4444', color: '#ef4444', marginTop: '20px'}}>
            <strong>Fehler:</strong> {error}
          </div>
        )}
      </main>

      <footer style={{marginTop: '40px', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-secondary)'}}>
        Hippy eBay Assistent v1.2 • Powered by Google Gemini 1.5 Pro
      </footer>
    </div>
  );
}
