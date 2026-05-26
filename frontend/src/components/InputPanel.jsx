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
      <h2>Governance Control Center</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the AI system or request for governance analysis..."
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-actions">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            disabled={disabled}
            ref={fileInputRef}
            id="file-upload"
            hidden
          />
          <label htmlFor="file-upload" className="btn secondary-btn">
            {preview ? "Change Image" : "Attach System Specs (Image)"}
          </label>

          {preview && (
            <button type="button" className="btn danger-btn" onClick={clearImage} disabled={disabled}>
              Remove
            </button>
          )}
        </div>

        {preview && (
          <div className="image-preview">
            <img src={preview} alt="Preview" />
          </div>
        )}

        <button type="submit" className="btn primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing System..." : "Execute Governance Check"}
        </button>
      </form>
    </div>
  );
}
