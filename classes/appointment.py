from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from .base import SQLclass


class Appointment(SQLclass):
    __tablename__ = "appointments"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey(column="uesrs.username"))
    clinic_id: Mapped[str] = mapped_column(
        String, ForeignKey(column="clinics.id"))

    user: Relationship = relationship(
        argument="User", back_populates="appointments")
    clinic: Relationship = relationship(
        argument="Clinic", back_populates="appointments")
