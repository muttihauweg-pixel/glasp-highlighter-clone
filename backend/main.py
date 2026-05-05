from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import datetime
import base64
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
    image: Optional[str] = None # Base64 encoded image

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = None
    mime_type = None

    if request.image:
        try:
            # Extract mime type and base64 data
            if "," in request.image:
                header, encoded = request.image.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
                image_data = base64.b64decode(encoded)
            else:
                image_data = base64.b64decode(request.image)
                mime_type = "image/jpeg" # Default
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data, mime_type)
        compliance_report = analysis_result["text"]
        history = analysis_result["history"]

        # 2. Risk Level Extraction
        # Try to extract risk level from the report
        risk_match = re.search(r"(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        risk_level = risk_match.group(0).capitalize() if risk_match else "Limited"

        # Construct steps for the UI
        steps = ["Input Received", "Multimodal Analysis", "Policy Verification"]
        for action in history:
            steps.append(f"Action: {action['action']}")
        steps.append("Audit Logged")

        result = {
            "risk": risk_level,
            "steps": steps,
            "processed_output": compliance_report[:200] + "..." if len(compliance_report) > 200 else compliance_report,
            "agent_history": history
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_content = f"{user_input}{timestamp}"
        audit_hash = hashlib.sha256(audit_content.encode()).hexdigest()

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
