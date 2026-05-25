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
          style={{ width: "100%", marginBottom: "10px", padding: "10px" }}
          disabled={disabled}
        />

        <div className="multimodal-input" style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "5px" }}>
            Attach Evidence/Document (Optional):
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            disabled={disabled}
            ref={fileInputRef}
          />
          {imagePreview && (
            <div style={{ marginTop: "10px", position: "relative", display: "inline-block" }}>
              <img
                src={imagePreview}
                alt="Preview"
                style={{ maxHeight: "150px", borderRadius: "8px", border: "1px solid #444" }}
              />
              <button
                type="button"
                onClick={clearImage}
                style={{
                  position: "absolute",
                  top: "-10px",
                  right: "-10px",
                  background: "red",
                  color: "white",
                  borderRadius: "50%",
                  border: "none",
                  width: "25px",
                  height: "25px",
                  cursor: "pointer"
                }}
              >
                ✕
              </button>
            </div>
          )}
        </div>

        <button type="submit" disabled={disabled || !input.trim()}>
          {disabled ? "Analyzing..." : "Process Request"}
        </button>
      </form>
    </div>
  );
}
