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
      onSubmit(input, image);
    }
  };

  const clearImage = () => {
    setImage(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel">
      <h2>Governance Control Center</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter AI request (e.g., 'Analyze customer data for credit scoring')"
          rows={5}
          disabled={disabled}
        />

        <div className="multimodal-input">
          <label className="file-upload">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
            <span>📷 Add Visual Context (Optional)</span>
          </label>

          {preview && (
            <div className="image-preview">
              <img src={preview} alt="Preview" />
              <button type="button" className="clear-btn" onClick={clearImage}>✕</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Processing..." : "Execute Compliance Check"}
        </button>
      </form>
    </div>
  );
}
