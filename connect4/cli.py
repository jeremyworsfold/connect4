import numpy as np
from abc import ABC, abstractmethod
from colorama import Fore, init, Back
import yaml
from pathlib import Path
from pydantic import BaseModel, validator

from connect4.board import Board, Piece, WinState
from connect4.theme import TerminalTheme


init()

fore_colors = {
    "black": Fore.BLACK,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "green": Fore.GREEN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "red": Fore.RED,
    "blank": Fore.RESET,
    "yellow": Fore.YELLOW,
    "none": ""
}

back_colors = {
    "black": Back.BLACK,
    "blue": Back.BLUE,
    "cyan": Back.CYAN,
    "green": Back.GREEN,
    "magenta": Back.MAGENTA,
    "white": Back.WHITE,
    "red": Back.RED,
    "blank": Back.RESET,
    "yellow": Back.YELLOW,
    "none": ""
}


def valid_fore(color: str) -> str:
    if color not in fore_colors:
        raise ValueError(f"Tuple must contain a colour from the list: {fore_colors.keys}")
    return color


def theme_from_file(file):
    path = Path.cwd() / 'conf' / 'cli_themes' / f'{file}.yaml'
    with open(path, 'r') as f:
        configs = yaml.safe_load(f)
    return TerminalTheme(**configs)


class Terminal:
    def __init__(self, theme: TerminalTheme) -> None:
        super().__init__()
        self.theme = theme
        self._ENDC = "\033[0m"
        self._start = theme.start
        self._end = theme.end

    def __getitem__(self, piece: Piece) -> str:
        return self._piece_as_str(piece)

    def _slots(self, valid_moves: np.ndarray) -> str:
        """Returns string of the valid columns and blank spaces in place of invalid columns"""
        vals = np.arange(1, len(valid_moves) + 1)
        line = list(
            np.where(valid_moves, vals, " ")
        )  # if not valid move, put " " in place.
        line.insert(0, " ")  # align with the printed board
        line.append("\n")
        return " ".join(line)

    def _piece_as_str(self, piece: Piece) -> str:
        return f"{self.theme.back}{self.theme[piece]} {self._ENDC}"

    def update(self, board: Board) -> None:
        strings = [self._slots(board.valid_moves)]
        flip = np.flipud(board.grid)
        for row in flip:
            strings.append(self._start)
            for item in row:
                strings.append(self[item])
            strings.append(self._end)
        print("".join(strings))

    def end_game(self, board: Board, winstate: WinState) -> None:
        self.update(board)
        if winstate.is_ended:
            print(f"Player {self.theme[winstate.winner]}{self._ENDC} has just won.")
        else:
            print("The Game is a draw.")


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

    _fore_check = validator(
        "FORE", "P1", "P2", "EMPTY", allow_reuse=True
    )(valid_fore)

    @validator("BACK")
    def valid_back(cls, color):
        if color not in back_colors:
            raise ValueError(f"Tuple must contain a colour from the list: {fore_colors.keys}")
        return color

    @property
    def back(self):
        return back_colors[self.BACK]
    
    @property
    def fore(self):
        return fore_colors[self.FORE]

    @property
    def start(self):
        return f"{self.back}{fore_colors[self.FORE]}| {self.ENDC}"

    @property
    def end(self):
        return f"{self.back}{fore_colors[self.FORE]}|{self.ENDC}\n"

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
        return fore_colors[col] + self.tokens[token]
