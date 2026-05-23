from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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

        # 2. Extract structured data from AI analysis
        result = {
            "risk": analysis_result.get("risk", "Unknown"),
            "steps": analysis_result.get("steps", ["Input Received", "Compliance Check"]),
            "processed_output": compliance_report[:200] + "..." if len(compliance_report) > 200 else compliance_report
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_input = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_input.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": compliance_report # Added for extra detail
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
