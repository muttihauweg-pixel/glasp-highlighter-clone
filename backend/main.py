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
        actions = analysis_result["actions"]

        # 2. Extract Risk Level using structured prefix
        risk_level = "Minimal"
        match = re.search(r"RISK_ASSESSMENT:\s*(\w+)", compliance_report, re.IGNORECASE)
        if match:
            extracted = match.group(1).capitalize()
            if extracted in ["Minimal", "Limited", "High", "Unacceptable"]:
                risk_level = extracted
        elif "unacceptable" in compliance_report.lower():
            risk_level = "Unacceptable"
        elif "high" in compliance_report.lower():
            risk_level = "High"

        # 3. Dynamic Steps based on actions
        steps = ["Input Received", "Multimodal Analysis"]
        if actions:
            steps.append("Policy Enforcement")
            for action in actions:
                steps.append(action.replace("_", " ").title())
        else:
            steps.append("Compliance Check")

        steps.append("Audit Generated")

        result = {
            "risk": risk_level,
            "steps": steps,
            "processed_output": f"Audit complete. {'Tools used: ' + ', '.join(actions) if actions else 'No issues found.'}"
        }

        # 4. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_hash = hashlib.sha256(f"{user_input}{timestamp}".encode()).hexdigest()

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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
