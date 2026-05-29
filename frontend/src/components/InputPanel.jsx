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

  const clearImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() || image) {
      onSubmit({ text: input, image });
    }
  };

  return (
    <div className="panel">
      <h2>Governance Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>AI Prompt / Use Case Description</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., 'Analyze this system architecture for GDPR compliance'"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="input-group" style={{ marginTop: '1rem' }}>
          <label>Upload Context (Image/Diagram)</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            disabled={disabled}
          />
          {imagePreview && (
            <div className="image-preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
              <button type="button" onClick={clearImage} className="clear-btn">Remove Image</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || (!input.trim() && !image)}>
          Run Governance Analysis
        </button>
      </form>
    </div>
  );
}
