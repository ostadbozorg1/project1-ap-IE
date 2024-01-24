from typing import Self
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from fuzzywuzzy import process
from .base import SQLclass


class Clinic(SQLclass):
    __tablename__ = "clinics"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    services: Mapped[str] = mapped_column(String)
    is_available: Mapped[str] = mapped_column(Boolean)

    appointments = relationship(
        argument="Appointment", back_populates="clinic")
    managers = relationship(
        argument="Manager", back_populates="clinic")

    @classmethod
    def get_clinics(cls, session) -> list[Self]:
        return [clinic for clinic in session.query(Clinic)]

    @classmethod
    def search_clinics(cls, query: str, session) -> list[Self]:
        clinics: list[Clinic] = Clinic.get_clinics(session)
        joined = [clinic.name+" "+clinic.services for clinic in clinics]
        matches: list[Clinic] = [clinics[joined.index(result[0])] for result in process.extract(
            query, joined, limit=5)]
        return matches  # type: ignore
