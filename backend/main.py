from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import datetime
import base64
import re
import json
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
    mime_type: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = None

    if request.image:
        try:
            # Handle data URL prefix if present
            header = "base64,"
            if header in request.image:
                image_data_str = request.image.split(header)[1]
            else:
                image_data_str = request.image
            image_data = base64.b64decode(image_data_str)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data, request.mime_type)
        report_text = analysis_result["text"]
        agent_steps = analysis_result["steps"]

        # 2. Parse Risk Level from structured JSON in text
        risk_level = "Minimal" # Default
        risk_match = re.search(r'```json\s*(.*?)\s*```', report_text, re.DOTALL)
        if risk_match:
            try:
                risk_data = json.loads(risk_match.group(1))
                risk_level = risk_data.get("risk_level", "Minimal")
            except:
                pass
        elif "Unacceptable" in report_text:
            risk_level = "Unacceptable"
        elif "High" in report_text:
            risk_level = "High"
        elif "Limited" in report_text:
            risk_level = "Limited"

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_content = f"{user_input}{timestamp}"
        if image_data:
            audit_content += hashlib.md5(image_data).hexdigest()

        audit_hash = hashlib.sha256(audit_content.encode()).hexdigest()

        result = {
            "risk": risk_level,
            "steps": ["Input Received", "Compliance Check", "Policy Enforcement"] + [step["action"] for step in agent_steps] + ["Audit Logged"],
            "processed_output": report_text[:500] + ("..." if len(report_text) > 500 else "")
        }

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
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
