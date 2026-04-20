from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialization = Column(String)
    experience_years = Column(Integer)
    qualification = Column(String)
    clinic_address = Column(Text)
    consultation_fee = Column(Float)
    bio = Column(Text)

    user = relationship("User", backref="doctor_profile")
