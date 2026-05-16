from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import datetime
import re
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
    image_data: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image_data

    try:
        # 1. AI Analysis (Governance Layer)
        report_data = analyze_compliance(user_input, image_data)
        full_text = report_data["text"]
        agent_steps = report_data["steps"]

        # 2. Extract Risk and Rationale using regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal|Low)", full_text, re.IGNORECASE)
        risk_level = risk_match.group(1) if risk_match else "Minimal"

        # Normalize risk levels for UI
        if risk_level.lower() == "low":
            risk_level = "Minimal"

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Hash including image data if present for integrity
        input_to_hash = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(input_to_hash.encode()).hexdigest()

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Gemini Analysis"] + agent_steps + ["Policy Enforcement", "Audit Logged"],
            "processed_output": full_text
        }

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": full_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
