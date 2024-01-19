from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import SQLclass
class Appointment(SQLclass):
    __tablename__ = "appointments"
    id = Column(String, primary_key=True, autoincrement=True)
    status = Column(String, nullable=False)
    date = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey(column="uesrs.username"))
    clinic_id = Column(String, ForeignKey(column="clinics.id"))
    
    user = relationship(argument="User",back_populates="appointments")
    clinic = relationship(argument="Clinic",back_populates="appointments")