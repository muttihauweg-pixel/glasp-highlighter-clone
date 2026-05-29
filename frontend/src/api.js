export async function processListing(input, image, video) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ input, image, video })
  });
  if (!res.ok) {
    throw new Error("Fehler beim Verarbeiten des Inserats");
  }
  return res.json();
}
