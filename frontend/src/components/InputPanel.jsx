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
      reader.read_as_DataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit({ input, image });
    }
  };

  const clearImage = () => {
    setImage(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel">
      <h2>Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter AI request (e.g., 'Analyze customer data for credit scoring')"
          rows={5}
          disabled={disabled}
        />

        {preview && (
          <div style={{ position: 'relative', display: 'inline-block' }}>
            <img src={preview} alt="Preview" className="image-preview" />
            <button
              type="button"
              onClick={clearImage}
              style={{
                position: 'absolute', top: 5, right: 5, padding: '2px 8px',
                background: 'red', fontSize: '12px', borderRadius: '50%'
              }}
            >
              ×
            </button>
          </div>
        )}

        <div className="button-group">
          <button type="submit" disabled={disabled || !input.trim()}>
            {disabled ? "Processing..." : "Process Request"}
          </button>

          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="secondary-button"
            onClick={() => fileInputRef.current.click()}
            disabled={disabled}
          >
            📎 Add Image
          </button>
        </div>
        <p className="upload-hint">Gemini 1.5 Pro analyzes both text and visual context for compliance.</p>
      </form>
    </div>
  );
}
