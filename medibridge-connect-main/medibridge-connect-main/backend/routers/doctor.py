from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.get("/dashboard")
def get_doctor_dashboard(db: Session = Depends(get_db)):
    return {
        "stats": {
            "today_appointments": 0,
            "total_patients": 0,
            "pending_reviews": 0
        },
        "appointments": []
    }
