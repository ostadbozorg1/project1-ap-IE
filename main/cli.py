from typing import Any, Callable, Generator, Self
import unicurses as curses


class CLI:
    def __init__(self):
        self.stdscr = curses.initscr()
        self._gen = self._generator()
        self.title = ""
        next(self._gen)

    def __enter__(self) -> Self:
        curses.noecho()
        curses.cbreak()
        self.noecho = True
        curses.keypad(self.stdscr, True)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        global stdscr
        curses.echo()
        curses.nocbreak()
        self.noecho = False
        curses.keypad(self.stdscr, True)
        return False

    def _generator(self) -> Generator[str, tuple[str, bool], None]:
        output: str | None = ""
        single_char: bool = False
        while True:
            curses.clear()
            curses.addstr(self.title + "\n")
            curses.addstr(output)
            curses.refresh()
            output, single_char = yield ((curses.getkey().decode("utf-8") if single_char else self.read_str()) if output != "" else "")

    def write_and_read(self, write: str, single_char: bool = False) -> str:
        return self._gen.send((write, single_char))

    def read_str(self) -> str:
        s = ""
        while (char := curses.getkey().decode("utf-8")) != "^J":
            if char == "^[":
                return ""
            if char == "^H":
                s = s[:-1]
                char = ""
                curses.move((pos := curses.getyx(self.stdscr))
                            [0], max(pos[1]-1, 0))
                curses.clrtoeol()
            s += char
            curses.addstr(char)
        return s

    def get_option(self, options: list[str]) -> int:
        pages: list[list[str]] = []
        page = 0
        i = -1
        for i in range(len(options)//7):
            pages += [options[i*7:(i+1)*7]]
        if len(options) % 7 != 0:
            pages += [options[(i+1)*7:]]
        while True:
            result = self.write_and_read(
                write="Select one of these options: \n"
                + "\n".join([f"{i+1} :{o}" for i, o in enumerate(
                    pages[page]
                    + (["previous page"] if page != 0 else [])
                    + (["next page"] if page != len(pages)-1 else []))])
                + "\n0: back", single_char=True)
            if result.isdecimal():
                if (option := int(result)) <= len(options):
                    if option == 8:
                        page -= 1
                    elif option == 9:
                        page += 1
                    else:
                        return page*7 + option - 1
            self.set_title("INVALID INPUT")

    def set_title(self, title: str):
        self.title = title

    def close(self):
        curses.clear()
        curses.refresh()
        self._gen.throw(GeneratorExit())
