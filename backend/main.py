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
        compliance_report = analysis_result["text"]
        tool_steps = analysis_result["steps"]

        # 2. Risk Level Parsing (improved)
        risk_level = "Minimal"
        if "RISK: Unacceptable" in compliance_report:
            risk_level = "Unacceptable"
        elif "RISK: High" in compliance_report:
            risk_level = "High"
        elif "RISK: Limited" in compliance_report:
            risk_level = "Limited"
        elif "RISK: Minimal" in compliance_report:
            risk_level = "Minimal"
        elif "high" in compliance_report.lower():
            risk_level = "High"

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Compliance Analysis"] + tool_steps + ["Policy Enforcement", "Output Generated"],
            "processed_output": compliance_report[:500] + "..." if len(compliance_report) > 500 else compliance_report
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_input = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_input.encode()).hexdigest()

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
