from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .user import User


class Manager(User):
    __tablename__ = "managers"

    username = Column(String, ForeignKey(
        column="uesrs.username"), primary_key=True)
    clinic_id = Column(String, ForeignKey(column="clinics.id"))

    user = relationship(argument="User", back_populates="manager")
    clinic = relationship(argument="Clinic", back_populates="managers")

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
