from collections.abc import Generator
from datetime import datetime
from classes import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import cli as cli_lib

engine = create_engine("sqlite:///main.sqlite3", echo=True)
session = Session(engine)


def main(cli: cli_lib.CLI):
    cli.set_title("WELCOME!")
    while True:
        match cli.get_option(["login", "sign up"]):
            case -1:
                cli.set_title("Back")
                break
            case 0:
                cli.set_title("Login")
                while True:
                    username = cli.write_and_read("Enter your username: ")
                    if username == "":
                        cli.set_title("Back")
                        break
                    password = cli.write_and_read("Enter your password: ")
                    if password == "":
                        cli.set_title("Back")
                        break
                    user = User.login(username, password, session)
                    if (user != None):
                        cli.set_title("Login successful")
                        if user.patient != None:
                            patient_main(cli, user.patient)
                        if user.manager != None:
                            manager_main(cli, user.manager)
                        break
                    else:
                        cli.set_title("Login failed")
                        break
            case 1:
                cli.set_title("Sign up")
                while True:
                    username = cli.write_and_read("Enter your username: ")
                    if username == "":
                        cli.set_title("Back")
                        break
                    password = cli.write_and_read("Enter your password: ")
                    if password == "":
                        cli.set_title("Back")
                        break
                    name = cli.write_and_read("Enter your name: ")
                    if name == "":
                        cli.set_title("Back")
                        break
                    email = cli.write_and_read("Enter your email: ")
                    if email == "":
                        cli.set_title("Back")
                        break
                    if Patient.sign_up(username, password, name, email, session) == None:
                        cli.set_title("Username already claimed")
                    cli.set_title("Sign up successful")
                    break


def patient_main(cli: cli_lib.CLI, patient: Patient):
    while True:
        match cli.get_option(["new appointment", "pending appointments", "current appointments", "past appointments"]):
            case -1:
                cli.set_title("Back")
                break
            case 0:
                make_appointment(cli, patient)
            case 1:
                cli.set_title("Pending appointments")
                show_pending_appointments(cli, patient)
            case 2:
                cli.set_title("Active appointments")
                show_active_appointments(cli, patient)
            case 3:
                cli.set_title("Past appointments")
                show_past_appointments(cli, patient)


def make_appointment(cli: cli_lib.CLI, patient: Patient):
    cli.set_title("Search for clinics")
    while True:
        query: str = cli.write_and_read("Enter search query: ")
        if query == "":
            cli.set_title("Back")
            break
        clinics: list[Clinic] = Clinic.search_clinics(
            query, session)
        result = cli.get_option(
            [f"{clinic.name}:{clinic.services}" for clinic in clinics])
        if result == -1:
            cli.set_title("Back")
            break
        if patient.new_appointment(clinics[result], session) == None:
            # THIS SHOULD NEVER HAPPEN!
            cli.set_title("Cannot make an appointment")
        cli.set_title("Successfully made an appointment")
        break


def show_pending_appointments(cli: cli_lib.CLI, patient: Patient):
    appointments = patient.get_pending_appointments(session)
    while True:
        match cli.get_option([f"{appointment.clinic.name}" for appointment in appointments]):
            case -1:
                cli.set_title("Back")
                break
            case x:
                match cli.get_option(["cancel"]):
                    case -1:
                        cli.set_title("Back")
                        break
                    case 0:
                        appointments[x].cancel_appointment(session)


def show_active_appointments(cli: cli_lib.CLI, patient: Patient):
    appointments = patient.get_active_appointments(session)
    while True:
        match cli.get_option([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments]):
            case -1:
                cli.set_title("Back")
                break
            case x:
                match cli.get_option(["cancel"]):
                    case -1:
                        cli.set_title("Back")
                        break
                    case 0:
                        appointments[x].cancel_appointment(session)


def show_past_appointments(cli: cli_lib.CLI, patient: Patient):
    appointments = patient.get_past_appointments(session)
    while True:
        match cli.get_option([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments]):
            case -1:
                cli.set_title("Back")
                break


def manager_main(cli: cli_lib.CLI, manager: Manager):
    while True:
        match cli.get_option(["pending appointments", "current appointments", "increase capacity"]):
            case -1:
                cli.set_title("Back")
                break
            case 0:
                cli.set_title("Pending appointments")
                manager_show_pending_appointments(cli, manager)
            case 1:
                cli.set_title("Active appointments")
                manager_show_active_appointments(cli, manager)
            case 2:
                cli.set_title("Increase capacity")
                increase_capacity(cli, manager)


def manager_show_active_appointments(cli: cli_lib.CLI, manager: Manager):
    apps: list[Appointment] = manager.get_pending_appointments(session)
    while True:
        match cli.get_option([f"{appointment.user.name}" for appointment in apps]):
            case -1:
                cli.set_title("Back")
                break
            case x:
                cli.set_title("Appointment")
                match cli.get_option(["cancel"]):
                    case -1:
                        cli.set_title("Back")
                        break
                    case 0:
                        apps[x].cancel_appointment(session)


def manager_show_pending_appointments(cli: cli_lib.CLI, manager: Manager):
    apps: list[Appointment] = manager.get_active_appointments(session)
    while True:
        match cli.get_option([f"{appointment.user.name}" for appointment in apps]):
            case -1:
                cli.set_title(title="Back")
                break
            case x:
                cli.set_title("Appointment")
                match cli.get_option(["approve", "cancel"]):
                    case -1:
                        cli.set_title("Back")
                        break
                    case 0:
                        while True:
                            cli.set_title("Appointment approval")
                            date = cli.write_and_read(
                                "Enter date (YYYY/MM/DD HH:MM): ")
                            if date == "":
                                cli.set_title("Back")
                                break
                            try:
                                dt = datetime.strptime(date, "%Y/%m/%d %H:%M")
                                apps[x].accept_appointment(dt, session)
                                break
                            except ValueError:
                                cli.set_title(
                                    "Invalid date. pay attention to the format")

                    case 1:
                        apps[x].cancel_appointment(session)


def increase_capacity(cli: cli_lib.CLI, manager: Manager):
    while True:
        cli.set_title("Increase appointment capacity")
        amount = cli.write_and_read(
            "Enter capacity: ")
        if amount == "":
            cli.set_title("Back")
            break
        if amount.isdecimal():
            manager.add_appointments(int(amount))
        else:
            cli.set_title(
                "Invalid number")


with cli_lib.CLI() as cli:
    main(cli)
