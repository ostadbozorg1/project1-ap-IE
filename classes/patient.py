from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import SQLclass
class Patient(SQLclass):
    __tablename__ = "patients"
    
    username = Column(String, ForeignKey(column="users.name"))
    
    user = relationship(argument="User",back_populates="patient")