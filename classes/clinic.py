from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from .base import SQLclass


class Clinic(SQLclass):
    __tablename__ = "clinics"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    services: Mapped[str] = mapped_column(String)
    is_available: Mapped[str] = mapped_column(Boolean)

    appointments: Relationship = relationship(
        argument="Appointment", back_populates="clinic")
    managers: Relationship = relationship(
        argument="Manager", back_populates="clinic")
