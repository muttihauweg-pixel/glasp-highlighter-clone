import { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 1000);
  };

  return (
    <div className="login-container fade-in">
      <div className="login-hero">
        <img src="/hippy_mascot.jpg" alt="Hippy" className="hippy-hero-img pulse" />
      </div>

      <h1 className="login-title">HIPPY</h1>
      <p className="login-subtitle">eBay Verkaufs-Assistent</p>
      <p className="login-desc">Dein KI-gestützter Multi-Agenten Assistent 🤖</p>

      <div className="agent-chips">
        {["📸 Foto", "💰 Preis", "✍️ Text", "⚖️ Recht", "🤖 Master"].map((chip) => (
          <span key={chip} className="agent-chip">
            {chip}
          </span>
        ))}
      </div>

      <div className="glass-panel login-card">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>E-Mail</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@beispiel.de"
              required
            />
          </div>
          <div className="input-group">
            <label>Passwort</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <button type="submit" className="btn-primary login-btn" disabled={loading}>
            {loading ? "Anmelden..." : "Anmelden"}
          </button>
        </form>

        <div className="divider"><span>ODER</span></div>

        <button
            className="btn-secondary demo-btn"
            onClick={onLogin}
            style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'}}
        >
          <img src="/hippy_mascot.jpg" alt="Hippy" style={{width: '24px', borderRadius: '50%'}} />
          Demo-Modus starten
        </button>
      </div>

      <p className="login-footer">
        Hippy hilft dir – einfach Foto machen,<br />
        fertige eBay-Anzeige erhalten! 🚀
      </p>
    </div>
  );
}
