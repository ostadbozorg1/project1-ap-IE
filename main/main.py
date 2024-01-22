from collections.abc import Generator
from classes import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import cli as cli_lib

engine = create_engine("sqlite:///main.sqlite3", echo=True)
session = Session(engine)


def main(cli: cli_lib.CLI):
    cli.set_title("WELCOME!")
    while True:
        match cli.get_option(["login", "exit"]):
            case 1:
                break
            case 0:
                cli.set_title("LOGIN")
                while True:
                    username = cli.write_and_read("enter your username:")
                    password = cli.write_and_read("enter your password:")
                    user = User.login(username, password, session)
                    if (user != None):
                        cli.set_title("LOGIN SUCCESSFUL")
                        if user.patient != None:
                            ...
                        if user.manager != None:
                            ...
                    else:
                        cli.set_title("LOGIN FAILED")
                        break


with cli_lib.CLI() as cli:
    main(cli)
