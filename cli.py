from typing import Any, Callable, Generator, Self
import unicurses as curses


class CLI:
    def __init__(self):
        self.stdscr = curses.initscr()
        self._gen = self._generator()
        next(self._gen)

    def __enter__(self) -> Self:
        curses.noecho()
        curses.cbreak()
        curses.keypad(self.stdscr, True)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        global stdscr
        curses.echo()
        curses.nocbreak()
        curses.keypad(self.stdscr, True)
        return False

    def _generator(self) -> Generator[str, str, None]:
        output: str | None = ""
        while True:
            curses.clear()
            curses.addstr(output)
            curses.refresh()
            output = yield (curses.getkey() if output != "" else "")

    def write_and_read(self, write: str) -> str:
        self._gen.send(write)
        return next(self._gen)

    def close(self):
        curses.clear()
        curses.refresh()
        self._gen.throw(GeneratorExit())
