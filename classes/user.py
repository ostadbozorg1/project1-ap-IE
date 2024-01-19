from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import SQLclass
class User(SQLclass):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    
    patient = relationship(argument="Patient",back_populates="user")
    manager = relationship(argument="Manager",back_populates="user")
    appointments = relationship(argument="Appointment",back_populates="user_id")