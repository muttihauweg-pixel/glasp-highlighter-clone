import { useState } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);

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

        <div className="image-upload">
          <label htmlFor="image-input" className="file-label">
            {preview ? "Change Image" : "📷 Attach Image (Optional)"}
          </label>
          <input
            id="image-input"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            disabled={disabled}
            style={{ display: 'none' }}
          />
          {preview && (
            <div className="image-preview">
              <img src={preview} alt="Preview" style={{ maxWidth: '100px', maxHeight: '100px', marginTop: '10px' }} />
              <button type="button" className="remove-image" onClick={() => {setImage(null); setPreview(null);}}>×</button>
            </div>
          )}
        </div>

        <button type="submit" className="submit-btn" disabled={disabled || !input.trim()}>
          Process with Multimodal Gemini 1.5 Pro
        </button>
      </form>
    </div>
  );
}
