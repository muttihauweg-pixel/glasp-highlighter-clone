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
    image: Optional[str] = None # Base64 encoded image

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = None
    mime_type = "image/jpeg"

    if request.image:
        try:
            # Remove header if present (e.g., data:image/jpeg;base64,)
            if "," in request.image:
                header, encoded = request.image.split(",", 1)
                # Extract mime-type if possible: data:image/png;base64
                if "image/" in header:
                    mime_type = header.split(";")[0].split(":")[1]
            else:
                encoded = request.image
            image_data = base64.b64decode(encoded)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data, mime_type=mime_type)

        # Ensure we have a string for the report
        if isinstance(analysis_result, dict):
            compliance_report = analysis_result.get("text", "No analysis text returned.")
            actions = analysis_result.get("actions", [])
        else:
            compliance_report = str(analysis_result)
            actions = []

        # 2. Map LLM output to UI structure
        # Heuristic for risk level based on report text
        risk_level = "Minimal"
        report_lower = compliance_report.lower()
        if "unacceptable" in report_lower:
            risk_level = "Unacceptable"
        elif "high" in report_lower:
            risk_level = "High"
        elif "limited" in report_lower:
            risk_level = "Limited"

        # Construct execution steps based on agent actions
        steps = ["Input Received", "Gemini Analysis"]
        for action in actions:
            if action["name"] == "save_to_google_docs":
                steps.append("Logged to Google Docs")
            elif action["name"] == "notify_governance_admin":
                steps.append("Admin Notified")

        steps.append("Policy Enforcement Complete")

        result = {
            "risk": risk_level,
            "steps": steps,
            "processed_output": compliance_report[:200] + "..." if len(compliance_report) > 200 else compliance_report,
            "actions": actions
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_payload = f"{user_input}{timestamp}"
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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
