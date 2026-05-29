export async function processInput(data) {
  // Use relative URL to support different environments (local vs cloud)
  const baseUrl = window.location.hostname === "localhost" ? "http://localhost:8000" : "";
  const res = await fetch(`${baseUrl}/process`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to process input");
  }
  return res.json();
}
