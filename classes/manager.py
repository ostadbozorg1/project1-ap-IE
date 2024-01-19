from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import SQLclass
class Manager(SQLclass):
    __tablename__ = "managers"
    
    username = Column(String, ForeignKey(column="uesrs.username"))
    clinic_id = Column(String, ForeignKey(column="clinics.id"))
    
    user = relationship(argument="User",back_populates="manager")
    clinic = relationship(argument="Clinic",back_populates="managers")
    