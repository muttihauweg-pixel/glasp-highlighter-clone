export async function processInput(inputData) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      input: inputData.text,
      image: inputData.image
    })
  });
  if (!res.ok) {
    throw new Error("Failed to process input");
  }
  return res.json();
}
