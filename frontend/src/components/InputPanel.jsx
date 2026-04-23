import { useState } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);

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

  return (
    <div className="panel">
      <h2>Input Panel</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter AI request (e.g., 'Analyze customer data for credit scoring')"
          rows={5}
          style={{ width: "100%", marginBottom: "10px" }}
          disabled={disabled}
        />
        <div style={{ marginBottom: "10px" }}>
          <label htmlFor="image-upload" style={{ display: "block", marginBottom: "5px" }}>
            Upload Image/Screenshot (Optional):
          </label>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            disabled={disabled}
          />
        </div>
        {image && (
          <div style={{ marginBottom: "10px" }}>
            <img src={image} alt="Preview" style={{ maxWidth: "200px", borderRadius: "4px" }} />
          </div>
        )}
        <button type="submit" disabled={disabled || !input.trim()}>
          Process Request with Gemini 1.5 Pro
        </button>
      </form>
    </div>
  );
}
