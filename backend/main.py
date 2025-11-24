from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity in this demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DEIInput(BaseModel):
    decision_time: float
    error_rate: float
    robustness_score: float

class DEIResult(BaseModel):
    dei: float
    timestamp: str
    input: DEIInput

history: List[DEIResult] = []

@app.post("/compute", response_model=DEIResult)
def compute_dei(data: DEIInput):
    if data.decision_time <= 0:
        raise HTTPException(status_code=400, detail="Decision time must be greater than 0")
    
    # DEI Formula: (1 / decision_time) * (1 - error_rate) * robustness_score
    dei = (1 / data.decision_time) * (1 - data.error_rate) * data.robustness_score
    
    result = DEIResult(
        dei=dei,
        timestamp=datetime.datetime.now().isoformat(),
        input=data
    )
    history.append(result)
    return result

@app.get("/history", response_model=List[DEIResult])
def get_history():
    return history

@app.post("/reset")
def reset_history():
    global history
    history = []
    return {"message": "History cleared"}
