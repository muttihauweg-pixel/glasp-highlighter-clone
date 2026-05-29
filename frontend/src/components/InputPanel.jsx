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
    <div className="panel">
      <h2>📦 Neues Inserat erstellen</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Beschreibe dein Produkt oder antworte der KI (z.B. 'iPhone 13, funktioniert super')"
          rows={4}
          disabled={disabled}
        />

        <div style={{display: 'flex', gap: '1rem', marginBottom: '1rem'}}>
          <div className="image-upload" style={{flex: 1}} onClick={() => fileInputRef.current.click()}>
            {image ? (
              <img src={image} alt="Preview" className="preview-img" style={{maxHeight: '100px'}} />
            ) : (
              <p>📸 Foto hochladen</p>
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              style={{ display: "none" }}
            />
          </div>

          <div className="image-upload" style={{flex: 1}} onClick={() => videoInputRef.current.click()}>
            {video ? (
              <div style={{fontSize: '0.8rem'}}>📹 Video bereit ({Math.round(video.length/1024/1024)}MB)</div>
            ) : (
              <p>🎥 Video hochladen (5-10s)</p>
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

        <button type="submit" disabled={disabled || (!input.trim() && !image && !video)}>
          {disabled ? "Experte analysiert..." : "Analyse starten"}
        </button>
      </form>
    </div>
  );
}
