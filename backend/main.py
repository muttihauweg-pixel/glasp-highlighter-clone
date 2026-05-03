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
    image_data: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API is Active"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input
    image_data = request.image_data

    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(user_input, image_data)
        compliance_report = analysis_result["text"]
        execution_steps = analysis_result["steps"]

        # 2. Advanced Risk Parsing (using regex to extract from LLM response)
        risk_match = re.search(r'RISK_ASSESSMENT:\s*(\w+)', compliance_report)
        risk_level = risk_match.group(1) if risk_match else "Unknown"

        result = {
            "risk": risk_level,
            "steps": execution_steps,
            "processed_output": compliance_report[:200] + "..." if len(compliance_report) > 200 else compliance_report
        }

        # 3. Immutable Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Combine input and image hash if exists for full traceability
        data_to_hash = f"{user_input}{image_data[:100] if image_data else ''}{timestamp}"
        audit_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp,
            "policy_version": "EU-AI-ACT-2024-V1",
            "model": "gemini-1.5-pro"
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
