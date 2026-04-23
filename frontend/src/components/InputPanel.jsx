import { useState } from "react";

export default function InputPanel({ onSubmit, disabled }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
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
          cols={50}
          disabled={disabled}
        />
        <br />
        <button type="submit" disabled={disabled || !input.trim()}>
          Process Request
        </button>
      </form>
    </div>
  );
}
