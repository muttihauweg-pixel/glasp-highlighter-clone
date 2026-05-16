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
        setImage(reader.result); // Base64 string
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
    <div className="panel">
      <h2>Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter AI request or context (e.g., 'Analyze our credit scoring logic for compliance')"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-controls">
          <label className="file-label">
            📸 Attach Screenshot/Document
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              disabled={disabled}
              style={{ display: 'none' }}
            />
          </label>

          {preview && (
            <div className="preview-container">
              <img src={preview} alt="Preview" className="image-preview" />
              <button type="button" onClick={clearImage} className="clear-btn">×</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Analyze Compliance"}
        </button>
      </form>
    </div>
  );
}
