from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from fuzzywuzzy import process
from .clinic import Clinic
from .appointment import Appointment
from .user import User
from main.api_handler import make_reservation


class Patient(User):
    __tablename__ = "patients"

    user_name: Mapped[str] = mapped_column(String, ForeignKey(
        column="users.name"), primary_key=True)

    user = relationship(
        argument="User", back_populates="patient")

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }

    def get_active_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status == "ACTIVE")]

    def get_past_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status != "ACTIVE")]

    def new_appointment(self, clinic: Clinic, session) -> Optional[Appointment]:
        if (make_reservation(str(clinic.id))):
            session.add(appointment := Appointment(status="PENDING", date=None,
                        user_id=self.username, clinic_id=clinic.id))
            session.commit()
            return appointment

    @staticmethod
    def get_clinics(session) -> list[tuple[str, str]]:
        return [(clinic.name, clinic.services) for clinic in session.query(Clinic)]

    @staticmethod
    def search_clinics(query: str, session) -> list[tuple[str, str]]:
        clinics: list[tuple[str, str]] = Patient.get_clinics(session)
        joined = [clinic[0]+" "+clinic[1] for clinic in clinics]
        matches: list[tuple[str, str]] = [clinics[joined.index(result[0])] for result in process.extract(
            query, joined, limit=5)]
        return matches
