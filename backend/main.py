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
        execution_steps = analysis_result["steps"]

        # 2. Parse Risk Level and Rationale using Regex
        # Expected format: RISK: [Level]
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        risk_level = risk_match.group(1).capitalize() if risk_match else "Limited"

        rationale_match = re.search(r"RATIONALE:\s*(.*)", compliance_report, re.IGNORECASE | re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else "Risk assessment completed by Gemini."

        result = {
            "risk": risk_level,
            "steps": execution_steps,
            "processed_output": rationale,
            "full_report": compliance_report
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Hash input + image + timestamp for audit trail
        audit_payload = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_payload.encode()).hexdigest()

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
        print(f"Error in /process: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
