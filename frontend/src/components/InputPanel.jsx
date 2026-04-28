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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input, image);
    }
  };

  const clearImage = () => {
    setImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="panel">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe the AI use case or system (e.g., 'A credit scoring model for SMEs')..."
          rows={5}
          disabled={disabled}
        />

        <div className="upload-section">
          <label className="file-label">
            📸 Attach Architecture / Screenshot (Optional)
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              disabled={disabled}
            />
          </label>

          {image && (
            <div className="image-preview">
              <img src={image} alt="Preview" style={{ maxWidth: "200px", marginTop: "10px", borderRadius: "8px" }} />
              <button type="button" onClick={clearImage} className="clear-btn">Remove Image</button>
            </div>
          )}
        </div>

        <button type="submit" disabled={disabled || !input.trim()} className="submit-btn">
          Analyze Compliance
        </button>
      </form>
    </div>
  );
}
