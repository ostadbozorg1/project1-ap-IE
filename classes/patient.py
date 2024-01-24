from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from .clinic import Clinic
from .appointment import Appointment
from .user import User
from main.api_handler import make_reservation


class Patient(User):
    __tablename__ = "patients"

    user_name: Mapped[str] = mapped_column(String, ForeignKey(
        column="users.username"), primary_key=True)

    user = relationship(
        argument="User", back_populates="patient")

    __mapper_args__ = {
        "polymorphic_identity": "patient",

    }

    def get_pending_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status == "PENDING")]

    def get_active_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status == "ACTIVE")]

    def get_past_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status != "ACTIVE", Appointment.status != "PENDING")]

    def new_appointment(self, clinic: Clinic, session) -> Optional[Appointment]:
        if (make_reservation(str(clinic.id))):
            session.add(appointment := Appointment(status="PENDING", date=None,
                        user_id=self.username, clinic_id=clinic.id))
            session.commit()
            return appointment

    @classmethod
    def sign_up(cls, username: str, password: str, name: str, email: str, session) -> User | None:
        if session.get(User, username) != None:
            return
        user = Patient(username=username,
                       password=password, name=name, email=email)
        print("add user")
        session.add(user)
        session.commit()
        return user.user
