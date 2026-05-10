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
    if (input.trim()) {
      onSubmit(input, image);
    }
  };

  const clearImage = () => {
    setImage(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel glass">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your AI use case (e.g., 'Deploying an emotional recognition system for HR interview analysis')"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="upload-section">
          <label className="file-label">
            <span>📷 Attach Screenshot (Optional)</span>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              disabled={disabled}
            />
          </label>

          {image && (
            <div className="image-preview">
              <img src={image} alt="Preview" />
              <button type="button" className="clear-btn" onClick={clearImage}>✕</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing Compliance..." : "Assess Risk"}
        </button>
      </form>
    </div>
  );
}
