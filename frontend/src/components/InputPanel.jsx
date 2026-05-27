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
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
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
          <label>Policy Request / AI Prompt</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., 'Review this medical diagnosis prompt for EU AI Act compliance'"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="input-group">
          <label>Multimodal Context (Optional Screenshot/Image)</label>
          <div className="file-upload">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
            {preview && (
              <div className="preview-container">
                <img src={preview} alt="Preview" className="image-preview" />
                <button type="button" onClick={clearImage} className="clear-btn">✕</button>
              </div>
            )}
          </div>
        </div>

        <button type="submit" className="primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Analyze Compliance"}
        </button>
      </form>
    </div>
  );
}
