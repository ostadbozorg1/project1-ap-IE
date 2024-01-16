from typing import Self
from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from .base import SQLclass


class User(SQLclass):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    patient = relationship(
        argument="Patient", back_populates="user")
    manager = relationship(
        argument="Manager", back_populates="user")
    appointments = relationship(
        argument="Appointment", back_populates="user")

