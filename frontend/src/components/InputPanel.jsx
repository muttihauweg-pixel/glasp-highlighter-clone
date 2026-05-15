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
          <label htmlFor="file-upload" className="custom-file-upload">
            📷 Attach Screenshot / Evidence
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            style={{display: 'none'}}
          />
          {imagePreview && (
            <div className="preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
              <button type="button" onClick={() => {setImage(null); setImagePreview(null);}} className="remove-img">×</button>
            </div>
          )}
        </div>

        <button type="submit" disabled={disabled || !input.trim()}>
          {disabled ? "Processing..." : "Process Request"}
        </button>
      </form>
    </div>
  );
}
