export async function processInput(input) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ input })
  });
  if (!res.ok) {
    throw new Error("Failed to process input");
  }
  return res.json();
}
