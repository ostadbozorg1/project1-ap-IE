from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship

from .user import User


class Manager(User):
    __tablename__ = "managers"

    user_username: Mapped[str] = mapped_column(String, ForeignKey(
        column="users.username"), primary_key=True)
    clinic_id: Mapped[str] = mapped_column(
        String, ForeignKey(column="clinics.id"))

    user: Relationship = relationship(
        argument="User", back_populates="manager")
    clinic: Relationship = relationship(
        argument="Clinic", back_populates="managers")

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
