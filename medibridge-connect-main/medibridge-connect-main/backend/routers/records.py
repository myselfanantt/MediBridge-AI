from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/records", tags=["Records"])

@router.get("/patient/{patient_id}")
def get_patient_records(patient_id: int):
    # Mock health records
    return [
        {
            "id": 1,
            "type": "Prescription",
            "date": "2024-04-10",
            "doctor": "Dr. Rahul Sharma",
            "details": "Paracetamol 500mg, twice a day for 3 days.",
            "file_url": "#"
        },
        {
            "id": 2,
            "type": "Lab Report",
            "date": "2024-03-15",
            "doctor": "Dr. Anita Desai",
            "details": "Blood test results - All parameters normal.",
            "file_url": "#"
        }
    ]

@router.post("/upload")
def upload_record():
    return {"message": "File uploaded successfully", "status": "success"}
