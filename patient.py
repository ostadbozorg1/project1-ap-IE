from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .user import User


class Patient(User):
    __tablename__ = "patients"

    username: Mapped[str] = mapped_column(String, ForeignKey(
        column="users.name"), primary_key=True)

    user = relationship(argument="User", back_populates="patient")

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }
