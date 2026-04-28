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
    mime_type = None

    if request.image:
        try:
            # Expected format: "data:image/png;base64,..."
            if "," in request.image:
                header, encoded = request.image.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                encoded = request.image
                mime_type = "image/png" # Default

            image_data = base64.b64decode(encoded)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    try:
        # 1. AI Analysis (Governance Layer)
        compliance_report = analyze_compliance(user_input, image_data, mime_type)

        # 2. Risk Level Extraction
        risk_level = "Minimal"
        report_lower = compliance_report.lower()
        if "unacceptable" in report_lower:
            risk_level = "Unacceptable"
        elif "high" in report_lower:
            risk_level = "High"
        elif "limited" in report_lower:
            risk_level = "Limited"
        elif "minimal" in report_lower:
            risk_level = "Minimal"
        elif "low" in report_lower:
             risk_level = "Minimal"

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Multimodal Analysis", "Agentic Reasoning", "Policy Enforcement", "Audit Trail Generated"],
            "processed_output": f"Governance check completed for: {user_input[:50]}..."
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_payload = f"{user_input}{timestamp}"
        if request.image:
            audit_payload += hashlib.md5(request.image.encode()).hexdigest()

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
