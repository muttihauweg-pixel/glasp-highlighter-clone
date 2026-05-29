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
          placeholder="Describe your AI use case or upload a system architecture diagram..."
          rows={5}
          disabled={disabled}
        />

        <div className="image-upload-section">
          <label>Multimodal Context (Optional):</label>
          <div className="file-input-wrapper">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
            {image && (
              <div className="preview-container">
                <img src={image} alt="Preview" className="preview-image" />
                <button type="button" className="clear-img-btn" onClick={clearImage}>
                  ×
                </button>
              </div>
            )}
          </div>
        </div>

        <button type="submit" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Run Compliance Check"}
        </button>
      </form>
    </div>
  );
}
