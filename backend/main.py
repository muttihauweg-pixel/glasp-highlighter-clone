from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import datetime
import re
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
    image: Optional[str] = None # Base64 data URL

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image

    image_bytes = None
    mime_type = None

    if image_data and "base64," in image_data:
        try:
            header, encoded = image_data.split("base64,")
            mime_type = header.replace("data:", "").replace(";", "")
            image_bytes = base64.b64decode(encoded)
        except Exception as e:
            print(f"Error decoding image: {e}")

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_bytes, mime_type)
        compliance_report = analysis_result["text"]
        steps = analysis_result["steps"]

        # 2. Risk Parsing using Regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        rationale_match = re.search(r"RATIONALE:\s*(.*)", compliance_report, re.IGNORECASE | re.DOTALL)

        risk_level = risk_match.group(1) if risk_match else "Unknown"
        rationale = rationale_match.group(1).strip() if rationale_match else "No rationale provided."

        result = {
            "risk": risk_level,
            "rationale": rationale,
            "steps": steps,
            "processed_output": f"Safe execution of request. [Audit Trail Hash: {hashlib.sha256(user_input.encode()).hexdigest()[:10]}]"
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Hash includes image if present
        hash_input = f"{user_input}{image_data if image_data else ''}{timestamp}"
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
