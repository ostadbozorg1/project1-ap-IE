from fuzzywuzzy import process
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .classes import Clinic, Appointment, User
from . import api_handler
from . import config
engine = create_engine("sqlite:///main.sqlite3", echo=True)
session = Session(engine)


def login(username: str, password: str) -> bool | User:
    if config.admin_username == username and config.admin_password == password:
        return True
    if (user := session.get(User, username)) == None:
        return False
    if (password != user.password):
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
        session.add(appointment := Appointment(status="ACTIVE", date=None,
                    user_id=user.username, clinic_id=clinic.id))
        session.commit()
        return appointment


def get_clinics() -> list[tuple[str, str]]:
    return [(str(clinic.name), str(clinic.services)) for clinic in session.query(Clinic)]


def search_clinics(query: str) -> list[tuple[str, str]]:
    clinics: list[tuple[str, str]] = get_clinics()
    joined = [clinic[0]+" "+clinic[1] for clinic in clinics]
    matches: list[tuple[str, str]] = [clinics[joined.index(result[0])] for result in process.extract(
        query, joined, limit=5)]
    return matches

# MANAGER

# ADMIN
