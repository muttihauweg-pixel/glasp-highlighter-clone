import { useState, useRef } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");
  const [image, setImage] = useState(null);
  const [video, setVideo] = useState(null);
  const fileInputRef = useRef(null);
  const videoInputRef = useRef(null);

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

  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 15 * 1024 * 1024) {
        alert("Video ist zu groß! Bitte maximal 15MB (ca. 10 Sek).");
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setVideo(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(input, image, video);
  };

  return (
    <div className="input-form">
      <h2 style={{color: 'white', marginBottom: '20px'}}>📦 Neues Inserat erstellen</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Beschreibe dein Produkt oder antworte der KI (z.B. 'iPhone 13, funktioniert super')"
          rows={6}
          disabled={disabled}
          style={{
            marginBottom: '1.5rem',
            background: 'rgba(0,0,0,0.2)',
            border: '1px solid var(--glass-border)',
            borderRadius: '12px',
            color: 'white',
            fontSize: '1rem'
          }}
        />

        <div className="image-upload-grid">
          <div className="upload-box" onClick={() => fileInputRef.current.click()}>
            {image ? (
              <img src={image} alt="Preview" className="preview-img" />
            ) : (
              <div style={{color: 'var(--text-secondary)'}}>
                <div style={{fontSize: '1.5rem', marginBottom: '0.5rem'}}>📸</div>
                <div style={{fontSize: '0.8rem'}}>Foto hochladen</div>
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              style={{ display: "none" }}
            />
          </div>

          <div className="upload-box" onClick={() => videoInputRef.current.click()}>
            {video ? (
              <div style={{fontSize: '0.8rem', color: 'var(--accent-cyan)'}}>
                <div style={{fontSize: '1.5rem', marginBottom: '0.5rem'}}>✅</div>
                Video bereit ({Math.round(video.length/1024/1024)}MB)
              </div>
            ) : (
              <div style={{color: 'var(--text-secondary)'}}>
                <div style={{fontSize: '1.5rem', marginBottom: '0.5rem'}}>🎥</div>
                <div style={{fontSize: '0.8rem'}}>Video hochladen (max 15MB)</div>
              </div>
            )}
            <input
              type="file"
              accept="video/*"
              onChange={handleVideoChange}
              ref={videoInputRef}
              style={{ display: "none" }}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={disabled || (!input.trim() && !image && !video)}
          style={{
            width: '100%',
            background: 'linear-gradient(90deg, var(--accent-purple), var(--accent-blue))',
            padding: '16px',
            fontSize: '1.1rem',
            borderRadius: '12px'
          }}
        >
          {disabled ? "Experte analysiert..." : "Analyse starten"}
        </button>
      </form>
    </div>
  );
}
