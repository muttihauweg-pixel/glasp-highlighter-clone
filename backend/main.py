from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import datetime
from gemini import analyze_compliance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    input: str
    image: Optional[str] = None # Base64 encoded image

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data)

        # 2. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Include image data hash if present
        image_hash = hashlib.sha256(image_data.encode()).hexdigest() if image_data else ""
        audit_content = f"{user_input}{image_hash}{timestamp}"
        audit_hash = hashlib.sha256(audit_content.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": {
                "risk": analysis_result["risk"],
                "steps": analysis_result["steps"],
                "processed_output": analysis_result["rationale"] # Use rationale as processed output
            },
            "audit": audit,
            "compliance_report": analysis_result["full_response"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
