import { useState } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
    }
  };

  return (
    <div className="panel">
      <h2>🎁 Wonach suchst du heute?</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ich suche eine Vintage-Kamera, die funktioniert! Oder vielleicht ein paar bunte Socken?"
          rows={4}
          disabled={disabled}
        />
        <button type="submit" disabled={disabled || !input.trim()}>
          {disabled ? "Freude verbreiten..." : "Finde mein Glücks-Angebot!"}
        </button>
      </form>
    </div>
  );
}
