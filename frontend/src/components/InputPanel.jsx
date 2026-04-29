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

  const clearImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="panel glass">
      <h2>Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>AI Request Instruction</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the AI system or request (e.g., 'Analyze this recruitment algorithm for bias')"
            rows={4}
            disabled={disabled}
          />
        </div>

        <div className="input-group">
          <label>Supporting Image (Optional)</label>
          <div className="file-upload">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              disabled={disabled}
            />
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="Preview" />
                <button type="button" onClick={clearImage} className="btn-clear">×</button>
              </div>
            )}
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={disabled || !input.trim()}>
          {disabled ? "Processing..." : "Initiate Governance Audit"}
        </button>
      </form>
    </div>
  );
}
