from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(Date)
    gender = Column(String)
    blood_group = Column(String)
    address = Column(Text)
    medical_history = Column(Text)

    user = relationship("User", backref="patient_profile")
