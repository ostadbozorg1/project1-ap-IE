from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from .appointment import Appointment
from .user import User
from main.api_handler import get_reservation_amount, add_reservation_amount


class Manager(User):
    __tablename__ = "managers"

    user_name: Mapped[str] = mapped_column(String, ForeignKey(
        column="users.username"), primary_key=True)
    clinic_id: Mapped[str] = mapped_column(
        String, ForeignKey(column="clinics.id"))

    user = relationship(
        argument="User", back_populates="manager")
    clinic = relationship(
        argument="Clinic", back_populates="managers")

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def get_clinic_active_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.clinic_id == self.clinic.id)]

    def get_pending_appointments(self, session) -> list[Appointment]:
        return [appointment for appointment in session.query(Appointment)
                .filter(Appointment.user_id == User.username, Appointment.status == "PENDING")]

    def get_available_appointments(self) -> int:
        return get_reservation_amount(id=self.clinic.id)

    def add_appointments(self, amount: int):
        add_reservation_amount(id=self.clinic.id, amount=amount)
