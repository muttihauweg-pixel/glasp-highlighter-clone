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
        agent_steps = analysis_result["steps"]

        # 2. Parse Risk and Rationale
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        rationale_match = re.search(r"RATIONALE:\s*(.*)", compliance_report, re.IGNORECASE | re.DOTALL)

        risk_level = risk_match.group(1).title() if risk_match else "High (Uncertain)"
        rationale = rationale_match.group(1).strip() if rationale_match else "Rationale not provided by agent."

        result = {
            "risk": risk_level,
            "rationale": rationale,
            "steps": agent_steps,
            "processed_output": f"Governance protocol enforced. Risk categorized as {risk_level}."
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
