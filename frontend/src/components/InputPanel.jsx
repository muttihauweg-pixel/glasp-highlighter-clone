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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input, image);
    }
  };

  return (
    <div className="panel">
      <h2>Governance Input Control</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your AI use case or paste a prompt..."
          rows={5}
          disabled={disabled}
        />

        <div className="image-upload">
          <label style={{color: '#94a3b8', fontSize: '0.9rem'}}>Optional: Upload Screenshot/System Architecture</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            style={{display: 'none'}}
          />
          <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
            <button
              type="button"
              onClick={() => fileInputRef.current.click()}
              style={{background: '#334155', padding: '0.5rem 1rem'}}
              disabled={disabled}
            >
              Select Image
            </button>
            {preview && (
              <div style={{position: 'relative'}}>
                <img src={preview} alt="Preview" className="preview-img" />
                <button
                  type="button"
                  onClick={() => {setImage(null); setPreview(null);}}
                  style={{
                    position: 'absolute', top: -5, right: -5,
                    background: '#ef4444', padding: '2px 8px', borderRadius: '50%'
                  }}
                >
                  ×
                </button>
              </div>
            )}
          </div>
        </div>

        <button type="submit" disabled={disabled || !input.trim()} style={{marginTop: '2rem', width: '100%'}}>
          Execute Governance Analysis
        </button>
      </form>
    </div>
  );
}
