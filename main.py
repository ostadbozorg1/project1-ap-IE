from collections.abc import Generator
from .classes import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import cli as cli_lib

engine = create_engine("sqlite:///main.sqlite3", echo=True)
session = Session(engine)
with cli_lib.CLI() as cli:
    while True:
        match cli.write_and_read(
            """Choose one of these options:
            1: login
            0: exit"""):
            case _:
                ...
