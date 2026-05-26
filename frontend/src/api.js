export async function processInput(input, image = null) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ input, image })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to process input");
  }
  return res.json();
}
