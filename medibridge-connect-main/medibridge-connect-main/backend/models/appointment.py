from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime)
    status = Column(String, default="scheduled") # scheduled, completed, cancelled
    reason = Column(Text)
    notes = Column(Text)

    patient = relationship("Patient", backref="appointments")
    doctor = relationship("Doctor", backref="appointments")
