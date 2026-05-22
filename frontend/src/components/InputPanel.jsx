import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setImage(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input, image);
    }
  };

  return (
    <div className="panel input-panel">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the AI workload or paste a prompt (e.g., 'Deploy credit scoring model for SME lending')"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-upload">
          <label className="file-label">
            <span>📷 Attach System Architecture / Context (Optional)</span>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
          </label>

          {preview && (
            <div className="image-preview">
              <img src={preview} alt="Upload preview" />
              <button type="button" onClick={clearImage} className="clear-btn">×</button>
            </div>
          )}
        </div>

        <button type="submit" className="primary-button" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Run Governance Check"}
        </button>
      </form>
    </div>
  );
}
