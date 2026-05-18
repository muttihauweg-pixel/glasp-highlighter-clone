from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
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
        tool_steps = analysis_result["steps"]

        # 2. Extract Risk and Rationale using Regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        rationale_match = re.search(r"RATIONALE:\s*(.*)", compliance_report, re.IGNORECASE | re.DOTALL)

        risk_level = risk_match.group(1) if risk_match else "Limited"
        rationale = rationale_match.group(1).strip() if rationale_match else "Analysis completed by AG-OS."

        # 3. Construct Result
        # Map tool steps to displayable steps
        display_steps = ["Input Received", "Multimodal Analysis", "Policy Verification"]
        for step in tool_steps:
            display_steps.append(f"Tool: {step['function']}")
        display_steps.append("Audit Trail Generated")

        result = {
            "risk": risk_level,
            "rationale": rationale,
            "steps": display_steps,
            "tool_details": tool_steps,
            "processed_output": compliance_report.split("RISK:")[0].strip()
        }

        # 4. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Hash text + image (if exists) + timestamp
        hash_input = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(hash_input.encode()).hexdigest()

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
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
