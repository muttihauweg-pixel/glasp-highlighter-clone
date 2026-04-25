import { useState } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const [base64Image, setBase64Image] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        // Remove prefix (e.g., "data:image/png;base64,")
        const base64String = reader.result.split(",")[1];
        setBase64Image(base64String);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input, base64Image);
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
        <div style={{ marginBottom: "10px" }}>
          <label htmlFor="image-upload" style={{ display: "block", marginBottom: "5px" }}>
            Upload Image (Optional Multimodal Analysis):
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
            <p>Selected image: {image.name}</p>
          </div>
        )}
        <button type="submit" disabled={disabled || !input.trim()}>
          Process Request
        </button>
      </form>
    </div>
  );
}
