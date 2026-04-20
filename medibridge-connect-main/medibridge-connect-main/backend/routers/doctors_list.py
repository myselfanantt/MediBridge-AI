from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.doctor import Doctor
from typing import List

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    if not doctors:
        # Return some mock doctors so the UI isn't empty
        return [
            {
                "id": 1,
                "name": "Dr. Rahul Sharma",
                "specialization": "Cardiologist",
                "experience_years": 12,
                "qualification": "MD, DM",
                "clinic_address": "Vashi, Navi Mumbai",
                "consultation_fee": 800.0,
                "rating": 4.8
            },
            {
                "id": 2,
                "name": "Dr. Anita Desai",
                "specialization": "Pediatrician",
                "experience_years": 8,
                "qualification": "MBBS, DCH",
                "clinic_address": "Seawoods, Navi Mumbai",
                "consultation_fee": 600.0,
                "rating": 4.9
            }
        ]
    return doctors
