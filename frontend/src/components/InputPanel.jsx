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

  const clearImage = () => {
    setImage(null);
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
    <div className="panel">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter AI request (e.g., 'Deploy biometric monitoring for public safety')"
          rows={5}
          disabled={disabled}
        />

        <div className="multimodal-input">
          <label className="file-label">
            📸 Attach Context (Image)
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
          </label>
          {image && (
            <div className="image-preview">
              <img src={image} alt="Preview" />
              <button type="button" onClick={clearImage} className="clear-btn">×</button>
            </div>
          )}
        </div>

        <button type="submit" className="primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Analyze Compliance"}
        </button>
      </form>
    </div>
  );
}
