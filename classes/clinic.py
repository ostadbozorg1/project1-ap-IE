from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from .base import SQLclass
class Clinic(SQLclass):
    __tablename__ = "clinics"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
    services = Column(String)
    is_available = Column(Boolean)
    
    appointments = relationship(argument="Appointment",back_populates="clinic")
    managers = relationship(argument="Manager",back_populates="clinic")