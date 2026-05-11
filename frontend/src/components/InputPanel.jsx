import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
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

  return (
    <div className="panel glass">
      <h2>Governance Input</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter AI request or compliance query..."
            rows={4}
            disabled={disabled}
          />
        </div>

        <div className="upload-section">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            ref={fileInputRef}
            style={{ display: "none" }}
          />
          <button
            type="button"
            className="secondary-btn"
            onClick={() => fileInputRef.current.click()}
            disabled={disabled}
          >
            {image ? "Change Image" : "📷 Attach Evidence"}
          </button>
          {image && (
            <div className="image-preview">
              <img src={image} alt="Preview" />
              <button type="button" className="remove-img" onClick={() => setImage(null)}>×</button>
            </div>
          )}
        </div>

        <button type="submit" className="primary-btn" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Run Compliance Check"}
        </button>
      </form>
    </div>
  );
}
