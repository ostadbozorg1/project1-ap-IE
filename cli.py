from typing import Callable
import unicurses as curses

stdscr = None


def curses_setup():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.keypad(stdscr, True)


def curses_cleanup():
    curses.echo()
    curses.nocbreak()
    curses.keypad(stdscr, True)


class Command:
    name: str
    title: str

    def __init__(self, name: str, title: str):
        self.name = name
        self.title = title

    def __call__(self) -> None:
        raise NotImplementedError


class MenuCommand(Command):
    subcommands: list[Command]

    def __init__(self, name: str, title: str, subcommands: list[Command]):
        super().__init__(name=name, title=title)
        self.subcommands = subcommands

    def __call__(self) -> None:
        curses.clear()
        curses.addstr(stdscr, self.title)
        curses.addstr(stdscr, "Select one of these options:")
        for i, o in enumerate(self.subcommands):
            curses.addstr(stdscr, f"{i}: {o.name}")
        curses.refresh()


class ActionCommand(Command):
    action: Callable[[], None]

    def __init__(self, name: str, title: str, action: Callable[[], None]):
        super().__init__(name, title)
        self.action = action

    def __call__(self) -> None:
        self.action()
