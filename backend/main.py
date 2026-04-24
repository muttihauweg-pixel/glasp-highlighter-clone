from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import datetime
import base64
from typing import Optional
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
    image: Optional[str] = None  # Base64 encoded image

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image

    try:
        image_bytes = None
        if image_data:
            # Decode base64 image if present
            try:
                if "," in image_data:
                    image_data = image_data.split(",")[1]
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                print(f"Error decoding image: {e}")

        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_bytes)
        compliance_report = analysis_result["report"]
        thought_log = analysis_result["thought_log"]

        # 2. Extract risk level from report or logs
        # Heuristic: if any 'High' or 'Unacceptable' is mentioned, or if admin was notified
        risk_level = "Minimal"
        report_lower = compliance_report.lower()

        if "unacceptable" in report_lower:
            risk_level = "Unacceptable"
        elif "high" in report_lower or any("notify_governance_admin" in log for log in thought_log):
            risk_level = "High"
        elif "limited" in report_lower:
            risk_level = "Limited"

        # Construct execution steps from agent logs
        execution_steps = ["Request Received"]
        if image_bytes:
            execution_steps.append("Multimodal Analysis")
        else:
            execution_steps.append("Text Analysis")

        for log in thought_log:
            # Clean up log for UI
            step = log.replace("Action: ", "")
            execution_steps.append(step)

        execution_steps.append("Final Compliance Report Generated")

        result = {
            "risk": risk_level,
            "steps": execution_steps,
            "processed_output": compliance_report[:500] + ("..." if len(compliance_report) > 500 else "")
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
            "compliance_report": compliance_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
