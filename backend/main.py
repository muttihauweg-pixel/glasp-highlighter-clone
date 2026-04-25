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
        compliance_report = analyze_compliance(user_input, image_data)

        # 2. Logic for Demo (Mapping LLM output to UI structure)
        risk_lower = compliance_report.lower()
        if "unacceptable" in risk_lower:
            risk_level = "Unacceptable"
        elif "high" in risk_lower:
            risk_level = "High"
        elif "limited" in risk_lower:
            risk_level = "Limited"
        else:
            risk_level = "Minimal"

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Multimodal Analysis", "Policy Enforcement", "Audit Generation"],
            "processed_output": f"Governance check complete for: {user_input[:50]}..."
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        combined_data = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(combined_data.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": compliance_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
