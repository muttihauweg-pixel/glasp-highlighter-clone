import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
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
    if (input.trim()) {
      onSubmit(input, image);
    }
  };

  const clearImage = () => {
    setImage(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel">
      <h2>Governance Input Terminal</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the AI system or paste a prompt for compliance check..."
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-actions">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            ref={fileInputRef}
            style={{ display: "none" }}
          />
          <button
            type="button"
            className="secondary-btn"
            onClick={() => fileInputRef.current.click()}
            disabled={disabled}
          >
            📷 Upload Screenshot/Context
          </button>

          {image && (
            <div className="image-preview">
              <img src={image} alt="Preview" />
              <button type="button" onClick={clearImage} className="clear-btn">×</button>
            </div>
          )}
        </div>

        <button type="submit" className="primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing with Gemini..." : "Run Compliance Check"}
        </button>
      </form>
    </div>
  );
}
