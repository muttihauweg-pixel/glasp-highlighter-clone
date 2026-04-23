from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

from typing import Optional

class ProcessRequest(BaseModel):
    input: str
    image: Optional[str] = None  # Base64 encoded image

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image

    try:
        # 1. AI Analysis (Governance Layer)
        compliance_report = analyze_compliance(user_input, image_data)

        # 2. Mock Logic for Demo (Mapping LLM output to UI structure)
        # In a real app, you'd parse the LLM output properly
        risk_level = "High" if "high" in compliance_report.lower() else "Low"

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Compliance Check", "Policy Enforcement", "Output Generated"],
            "processed_output": f"Safe execution of: {user_input[:50]}..."
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_hash = hashlib.sha256(f"{user_input}{timestamp}".encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": compliance_report # Added for extra detail
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
