export async function processInput(input, imageData = null) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      input,
      image_data: imageData
    })
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Failed to process input");
  }
  return res.json();
}
