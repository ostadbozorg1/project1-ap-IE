from datetime import datetime
from fuzzywuzzy import process
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .classes import Clinic, Appointment, User, Manager
from . import api_handler
from . import config
engine = create_engine("sqlite:///main.sqlite3", echo=True)
session = Session(engine)


def login(username: str, password: str) -> bool | User:
    if config.admin_username == username and config.admin_password == password:
        return True
    if (user := session.get(User, username)) == None:
        return False
    if (user.password != password):
        return False
    return user

# USER


def get_active_appointments(user: User) -> list[Appointment]:
    return [appointment for appointment in session.query(Appointment)
            .filter(Appointment.user_id == User.username, Appointment.status == "ACTIVE")]


def get_past_appointments(user: User) -> list[Appointment]:
    return [appointment for appointment in session.query(Appointment)
            .filter(Appointment.user_id == User.username, Appointment.status != "ACTIVE")]


def new_appointment(user: User, clinic: Clinic) -> Optional[Appointment]:
    if (api_handler.make_reservation(str(clinic.id))):
        session.add(appointment := Appointment(status="PENDING", date=None,
                    user_id=user.username, clinic_id=clinic.id))
        session.commit()
        return appointment


def get_clinics() -> list[tuple[str, str]]:
    return [(clinic.name, clinic.services) for clinic in session.query(Clinic)]


def search_clinics(query: str) -> list[tuple[str, str]]:
    clinics: list[tuple[str, str]] = get_clinics()
    joined = [clinic[0]+" "+clinic[1] for clinic in clinics]
    matches: list[tuple[str, str]] = [clinics[joined.index(result[0])] for result in process.extract(
        query, joined, limit=5)]
    return matches

# MANAGER


def get_clinic_active_appointments(manager: Manager) -> list[Appointment]:
    return [appointment for appointment in session.query(Appointment)
            .filter(Appointment.clinic_id == manager.clinic.id)]


def get_pending_appointments(user: User) -> list[Appointment]:
    return [appointment for appointment in session.query(Appointment)
            .filter(Appointment.user_id == User.username, Appointment.status == "PENDING")]


def cancel_appointment(appointment: Appointment):
    appointment.status = "CANCELLED"
    session.commit()


def accept_appointment(appointment: Appointment, date: datetime):
    appointment.status = "ACTIVE"
    appointment.date = int(date.timestamp())
    session.commit()


def get_available_appointments(manager: Manager) -> int:
    return api_handler.get_reservation_amount(id=manager.clinic.id)


def add_appointments(manager: Manager, amount: int):
    api_handler.add_reservation_amount(id=manager.clinic.id, amount=amount)


# ADMIN
