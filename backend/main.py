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

@app.get("/")
def read_root():
    return {"message": "Happy eBay Assistent API 🌈"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    user_input = request.input

    try:
        # 1. KI-Analyse (Happy Assistant Ebene)
        analysis = analyze_compliance(user_input)

        # 2. Result Mapping
        result = {
            "joy_score": analysis["joy_score"],
            "rationale": analysis["rationale"],
            "steps": analysis["steps"],
            "processed_output": analysis["text"]
        }

        # 3. Fröhlicher Audit Trail
        timestamp = datetime.datetime.now().isoformat()
        audit_hash = hashlib.sha256(f"{user_input}{timestamp}".encode()).hexdigest()

        audit = {
            "hash": audit_hash,
            "timestamp": timestamp
        }

        return {
            "result": result,
            "audit": audit,
            "full_analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
