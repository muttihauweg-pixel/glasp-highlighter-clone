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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit({ text: input, image });
    }
  };

  const clearImage = () => {
    setImage(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel input-panel">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your AI use case or upload a system prompt/screenshot..."
          rows={5}
          disabled={disabled}
        />

        <div className="multimodal-actions">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="secondary-btn"
            onClick={() => fileInputRef.current.click()}
            disabled={disabled}
          >
            📷 Add Image Analysis
          </button>

          {preview && (
            <div className="image-preview-container">
              <img src={preview} alt="Preview" className="image-preview" />
              <button type="button" className="close-btn" onClick={clearImage}>×</button>
            </div>
          )}
        </div>

        <button type="submit" className="primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Analyze with Gemini 1.5 Pro"}
        </button>
      </form>
    </div>
  );
}
