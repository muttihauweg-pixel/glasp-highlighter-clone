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
        report_data = analyze_compliance(user_input, image_data)
        full_text = report_data["text"]

        # 2. Extract Risk Level and Rationale using regex
        risk_match = re.search(r"Risk Level:\s*(Unacceptable|High|Limited|Minimal)", full_text, re.IGNORECASE)
        risk_level = risk_match.group(1).capitalize() if risk_match else "Limited"

        rationale_match = re.search(r"Rationale:\s*(.*)", full_text, re.IGNORECASE | re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else "Standard compliance review performed."

        result = {
            "risk": risk_level,
            "steps": report_data["steps"],
            "processed_output": rationale[:500] + ("..." if len(rationale) > 500 else "")
        }

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        # Include image in hash if present
        hash_input = f"{user_input}{image_data or ''}{timestamp}"
        audit_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "compliance_report": full_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
