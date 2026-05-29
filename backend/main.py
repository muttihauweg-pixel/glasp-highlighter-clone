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
    text: str
    image: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "AI Governance OS API"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    try:
        # 1. AI Analysis (Governance Layer)
        analysis_result = analyze_compliance(request.text, request.image)

        # 3. Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_input = f"{request.text}{request.image or ''}{timestamp}"
        audit_hash = hashlib.sha256(audit_input.encode()).hexdigest()

        return {
            "result": analysis_result["data"],
            "audit": {
                "hash": audit_hash,
                "timestamp": timestamp
            },
            "compliance_report": analysis_result["full_response"]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
