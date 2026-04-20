from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.appointment import Appointment
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/appointments", tags=["Appointments"])

class AppointmentCreate(BaseModel):
    doctorId: str
    doctorName: str
    spec: str
    patientName: str
    symptoms: str
    type: str
    date: str
    time: str

class AppointmentResponse(BaseModel):
    id: int
    doctor: str
    spec: str
    date: str
    time: str
    status: str
    type: str

    class Config:
        from_attributes = True

@router.post("/book")
def book_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        doctor=data.doctorName,
        spec=data.spec,
        date=data.date,
        time=data.time,
        status="scheduled",
        type=data.type
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "Appointment booked successfully", "id": new_appointment.id}

@router.get("/upcoming", response_model=List[AppointmentResponse])
def get_upcoming_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.status == "scheduled").all()

@router.get("/history", response_model=List[AppointmentResponse])
def get_appointment_history(db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.status != "scheduled").all()

@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()
