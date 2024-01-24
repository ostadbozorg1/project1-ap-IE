from typing import Self
from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship

from .base import SQLclass


class User(SQLclass):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False,  unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String, nullable=False)

    patient = relationship(
        argument="Patient", back_populates="user")
    manager = relationship(
        argument="Manager", back_populates="user")
    appointments = relationship(
        argument="Appointment", back_populates="user")

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }

    @classmethod
    def login(cls, username: str, password: str, session) -> Self | None:
        if (user := session.get(User, username)) == None:
            return
        if (user.password != password):
            return
        return user
