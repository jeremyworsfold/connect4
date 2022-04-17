from pydantic import BaseModel, validator
from pathlib import Path
from colorama import Fore, init, Back
import yaml

from connect4.board import Piece

init()

FORE = {
    "black": Fore.BLACK,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "green": Fore.GREEN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "red": Fore.RED,
    "blank": Fore.RESET,
    "yellow": Fore.YELLOW,
    "none": "",
}

BACK = {
    "black": Back.BLACK,
    "blue": Back.BLUE,
    "cyan": Back.CYAN,
    "green": Back.GREEN,
    "magenta": Back.MAGENTA,
    "white": Back.WHITE,
    "red": Back.RED,
    "blank": Back.RESET,
    "yellow": Back.YELLOW,
    "none": "",
}


def theme_from_file(file):
    path = Path.cwd() / "conf" / "cli_themes" / f"{file}.yaml"
    with open(path, "r") as f:
        configs = yaml.safe_load(f)
    return TerminalTheme(**configs)


class CliConfig(BaseModel):
    themename: str
    player1: str
    player2: str

    @validator("themename")
    def theme_validation(cls, v: str) -> str:
        path = Path.cwd() / "conf" / "cli_themes" / f"{v}.yaml"
        print(path)
        if not path.exists():
            raise FileNotFoundError(f"{v} is not a preset theme.")
        return v


def valid_fore(color: str) -> str:
    if color not in FORE:
        raise ValueError(
            f"Tuple must contain a colour from the list: {FORE.keys}"
        )
    return color


class TerminalTheme(BaseModel):
    FORE: str = Fore.WHITE
    BACK: str = Back.BLACK
    P1: str = Fore.WHITE
    P2: str = Fore.WHITE
    EMPTY: str = Fore.WHITE

    P1_token: str = "filled"
    P2_token: str = "filled"
    EMPTY_token: str = "filled"

    tokens = dict(filled="⬤", empty="◯", _="_")
    ENDC: str = "\033[0m"

    _fore_check = validator("FORE", "P1", "P2", "EMPTY", allow_reuse=True)(valid_fore)

    @validator("BACK")
    def valid_back(cls, color):
        if color not in BACK:
            raise ValueError(
                f"Tuple must contain a colour from the list: {BACK.keys}"
            )
        return color

    @property
    def back(self):
        return BACK[self.BACK]

    @property
    def fore(self):
        return FORE[self.FORE]

    @property
    def start(self):
        return f"{self.back}{FORE[self.FORE]}| {self.ENDC}"

    @property
    def end(self):
        return f"{self.back}{FORE[self.FORE]}|{self.ENDC}\n"

    def __getitem__(self, piece: Piece):
        if piece == Piece.P1:
            token = self.P1_token
            col = self.P1
        elif piece == Piece.P2:
            token = self.P2_token
            col = self.P2
        else:
            token = self.EMPTY_token
            col = self.EMPTY
        return FORE[col] + self.tokens[token]


class PyGameConfig(BaseModel):
    themename: str
    screenwidth: int
    player1: str
    player2: str

    @validator("themename")
    def theme_validation(cls, v: str) -> str:
        path = Path.cwd() / "conf" / "pg_themes" / f"{v}.yaml"
        print(path)
        if not path.exists():
            raise FileNotFoundError(f"{v} is not a preset theme.")
        return v

    @validator("screenwidth")
    def positive_integer(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"{v} needs to be a positive integer")
        return v
