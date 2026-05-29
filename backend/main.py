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
    image: Optional[str] = None

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

        # 2. Map Result to UI Structure
        result = {
            "risk": analysis_result["risk"],
            "steps": analysis_result["steps"],
            "processed_output": analysis_result["text"],
            "rationale": analysis_result["rationale"]
        }

        # 3. Immutable Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Create hash from input, image (if present), and timestamp
        audit_source = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_source.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": analysis_result["text"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
