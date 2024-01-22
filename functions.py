from math import e
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

def new_appointment(user: User, clinic: Clinic) -> Appointment:
    

# MANAGER

# ADMIN
