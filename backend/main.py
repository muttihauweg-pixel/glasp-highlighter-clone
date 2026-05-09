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
        steps = analysis_result["steps"]

        # 2. Extract Risk Level from AI response
        risk_match = re.search(r"Risk Level:\s*(Unacceptable|High|Limited|Minimal)", compliance_report, re.IGNORECASE)
        risk_level = risk_match.group(1).capitalize() if risk_match else "Limited"

        # 3. Dynamic output generation
        result = {
            "risk": risk_level,
            "steps": steps,
            "processed_output": compliance_report[:200] + "..." if len(compliance_report) > 200 else compliance_report
        }

        # 4. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Hash includes image data if present for full traceability
        data_to_hash = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()

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
