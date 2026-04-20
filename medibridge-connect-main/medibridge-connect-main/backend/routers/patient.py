from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.get("/dashboard")
def get_patient_dashboard(db: Session = Depends(get_db)):
    # Returning mock data that the frontend likely expects
    return {
        "stats": {
            "appointments": 0,
            "prescriptions": 0,
            "reports": 0
        },
        "upcoming_appointments": [],
        "recent_activity": []
    }
