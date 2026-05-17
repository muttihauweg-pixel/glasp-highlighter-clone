import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setImagePreview(reader.result);
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
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
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
            placeholder="Describe your AI use case or request (e.g., 'Analyze medical images for diagnosis')"
            rows={4}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-controls">
          <label className="file-upload">
            <span>📷 Attach Evidence (Optional)</span>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
              style={{ display: 'none' }}
            />
          </label>

          {imagePreview && (
            <div className="image-preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
              <button type="button" className="clear-btn" onClick={clearImage}>×</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Run Compliance Analysis"}
        </button>
      </form>
    </div>
  );
}
