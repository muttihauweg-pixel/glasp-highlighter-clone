from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import datetime
from gemini import process_listing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ListingRequest(BaseModel):
    input: str
    image: Optional[str] = None # Base64 image data
    video: Optional[str] = None # Base64 video data

@app.get("/")
def read_root():
    return {"message": "eBay Verkaufs-Experte API 🚀"}

@app.post("/process")
async def process_input(request: ListingRequest):
    user_input = request.input
    image_data = request.image
    video_data = request.video

    try:
        # 1. KI-Analyse (Multi-Agenten-System)
        analysis = process_listing(user_input, image_data, video_data)

        # 2. Result Mapping
        result = {
            "current_step": analysis["step"],
            "steps": analysis["steps"],
            "processed_output": analysis["text"]
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        content_to_hash = f"{user_input}{image_data or ''}{video_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(content_to_hash.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
