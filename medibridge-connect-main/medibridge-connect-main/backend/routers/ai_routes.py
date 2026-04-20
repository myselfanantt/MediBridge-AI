from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/ai", tags=["AI"])

class SymptomRequest(BaseModel):
    symptoms: str

class SymptomResponse(BaseModel):
    possible_illness: str
    severity: str
    recommendation: str
    precautions: Optional[List[str]] = []

@router.post("/symptom-checker")
def analyze_symptoms(request: SymptomRequest):
    symptoms = request.symptoms.lower()
    
    if "fever" in symptoms:
        return {
            "possible_illness": "Common Flu or Viral Infection",
            "severity": "Moderate",
            "recommendation": "Rest, stay hydrated, and take paracetamol if needed. Consult a doctor if fever persists for more than 3 days.",
            "precautions": ["Rest", "Hydration", "Monitor temperature"]
        }
    elif "cough" in symptoms:
        return {
            "possible_illness": "Common Cold or Bronchitis",
            "severity": "Low",
            "recommendation": "Use cough syrup and avoid cold drinks. If breathing is difficult, seek medical help.",
            "precautions": ["Warm liquids", "Steam inhalation"]
        }
    else:
        return {
            "possible_illness": "General Fatigue / Undetermined",
            "severity": "Low",
            "recommendation": "Monitor your symptoms. If you feel worse, please book an appointment with a doctor.",
            "precautions": ["Rest", "Observation"]
        }

@router.post("/chat")
def chat(request: dict):
    message = request.get("message", "").lower()
    
    if "fever" in message or "sick" in message:
        return {"response": "I'm sorry you're feeling unwell. You can use our Symptom Checker for a more detailed analysis or book an appointment with a doctor."}
    elif "appointment" in message:
        return {"response": "You can book an appointment by clicking the 'Book Appointment' button on your dashboard."}
    elif "hello" in message or "hi" in message:
        return {"response": "Hello! I am MediBridge AI, your personal healthcare assistant. How can I help you today?"}
    
    return {
        "response": "I am MediBridge AI. I am currently in demo mode, but I can help you with basic health questions.",
        "status": "success"
    }
