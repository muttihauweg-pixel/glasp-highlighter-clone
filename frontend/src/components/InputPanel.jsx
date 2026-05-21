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
    <div className="panel">
      <h2>Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter AI request (e.g., 'Analyze customer data for credit scoring')"
            rows={5}
            disabled={disabled}
          />
        </div>

        <div className="multimodal-upload">
          <label className="file-label">
            📸 Add Context Image (Optional)
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              disabled={disabled}
              ref={fileInputRef}
            />
          </label>

          {preview && (
            <div className="image-preview">
              <img src={preview} alt="Context Preview" />
              <button type="button" onClick={clearImage} className="clear-btn">×</button>
            </div>
          )}
        </div>

        <button type="submit" disabled={disabled || !input.trim()} className="primary-btn">
          {disabled ? "Analyzing..." : "Process with Gemini 1.5 Pro"}
        </button>
      </form>
    </div>
  );
}
