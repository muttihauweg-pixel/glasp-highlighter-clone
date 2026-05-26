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

class ProcessRequest(BaseModel):
    input: str
    image: str = None  # Base64 encoded image data

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

        # 2. Extract results from agent analysis
        compliance_report = analysis_result.get("response", "No report generated.")
        risk_level = analysis_result.get("risk_level", "Unknown")
        execution_steps = analysis_result.get("steps", ["Input Received", "Compliance Analysis"])

        result = {
            "risk": risk_level,
            "steps": execution_steps,
            "processed_output": compliance_report
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Include image data in hash if present for full traceability
        data_to_hash = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()

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
