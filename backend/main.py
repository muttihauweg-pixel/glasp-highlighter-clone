from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import datetime
from gemini import analyze_compliance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional

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
        # 1. AI Analysis (Governance Layer) - Multimodal & Agentic
        analysis_result = analyze_compliance(user_input, image_data)

        compliance_report = analysis_result["report"]
        steps = analysis_result["steps"]

        # 2. Extract Risk Level (Using markers from System Instruction)
        import re
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        risk_level = risk_match.group(1) if risk_match else "Limited"

        result = {
            "risk": risk_level,
            "steps": steps,
            "processed_output": f"Analyzed: {user_input[:50]}..."
        }

        # 3. Audit Trail (Immutable Hash)
        timestamp = datetime.datetime.now().isoformat()
        content_to_hash = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(content_to_hash.encode()).hexdigest()

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
