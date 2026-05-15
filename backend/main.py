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
        compliance_data = analyze_compliance(user_input, image_data)
        report_text = compliance_data["text"]

        # 2. Extract Risk and Rationale using regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", report_text, re.IGNORECASE)
        risk_level = risk_match.group(1) if risk_match else "Unknown"

        rationale_match = re.search(r"RATIONALE:\s*(.*)", report_text, re.IGNORECASE | re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else "No rationale provided."

        result = {
            "risk": risk_level,
            "rationale": rationale,
            "steps": compliance_data["steps"],
            "processed_output": report_text
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Combine input and image hash if image exists
        audit_content = f"{user_input}{image_data if image_data else ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_content.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": report_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
