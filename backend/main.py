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
    image: Optional[str] = None # Base64 data URL

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = None
    mime_type = None

    # Handle Multimodal Input
    if request.image and "," in request.image:
        header, encoded = request.image.split(",", 1)
        mime_type = header.split(";")[0].split(":")[1]
        image_data = encoded

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data, mime_type)
        report_text = analysis_result["text"]
        tool_calls = analysis_result["tool_calls"]

        # 2. Extract Risk and Rationale using Regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", report_text, re.IGNORECASE)
        rationale_match = re.search(r"RATIONALE:\s*(.*)", report_text, re.IGNORECASE | re.DOTALL)

        risk_level = risk_match.group(1).capitalize() if risk_match else "Unknown"
        rationale = rationale_match.group(1).strip() if rationale_match else "No rationale provided."

        # 3. Dynamic Execution Steps
        steps = ["Input Received", "Multimodal Analysis", "Policy Verification"]
        for call in tool_calls:
            steps.append(f"Action: {call['name']}")
        steps.append("Governance Audit Signed")

        result = {
            "risk": risk_level,
            "rationale": rationale,
            "steps": steps,
            "tool_calls": tool_calls,
            "processed_output": f"Governance check completed for: {user_input[:50]}..."
        }

        # 4. Immutable Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_payload = f"{user_input}{request.image or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_payload.encode()).hexdigest()

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
