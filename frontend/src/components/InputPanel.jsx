import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(input, image);
    // Optional: Clear after submit if needed, or keep for multi-step
  };

  return (
    <div className="panel">
      <h2>📦 Neues Inserat erstellen</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Beschreibe dein Produkt oder antworte auf die Fragen der KI (z.B. 'iPhone 13, funktioniert super, nur kleine Kratzer')"
          rows={4}
          disabled={disabled}
        />

        <div className="image-upload" onClick={() => fileInputRef.current.click()}>
          {image ? (
            <img src={image} alt="Preview" className="preview-img" />
          ) : (
            <p>📸 Klicke hier, um ein Foto hochzuladen</p>
          )}
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            style={{ display: "none" }}
          />
        </div>

        <button type="submit" disabled={disabled || (!input.trim() && !image)}>
          {disabled ? "Experte analysiert..." : "Analyse starten"}
        </button>
      </form>
    </div>
  );
}
