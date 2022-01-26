from dataclasses import dataclass
import numpy as np
from abc import ABC, abstractmethod
from colorama import Fore, init

from connect4.board import Board, Piece

class Display(ABC):

    @abstractmethod
    def update(self, board: Board) -> None:
        pass 


class Terminal(Display):
    def __init__(self) -> None:
        super().__init__()
        self._start = "| "
        self._end = "|\n"

    def _slots(self, valid_moves):
        vals = np.arange(1,len(valid_moves)+1)
        line = list(np.where(valid_moves,vals," "))
        line.insert(0," ")
        line.append("\n")
        return " ".join(line)

    @abstractmethod
    def _item_as_str(self, item:Piece) -> str:
        pass

    def update(self, board: Board):
        strings = [self._slots(board.valid_moves)]
        flip = np.flipud(board.grid)

        for row in flip:
            strings.append(self._start)
            for item in row:
                strings.append(self._item_as_str(item))
            strings.append(self._end)
        print("".join(strings))



class ColorTerminal(Terminal):
    def __init__(self) -> None:
        super().__init__()
        init()
        self._char = {
            Piece.RED : (Fore.RED, '⬤'),
            Piece.YELLOW : (Fore.YELLOW, '⬤'),
            Piece.EMPTY : (Fore.BLUE, '◯')
        }
        self._ENDC = '\033[0m'
        self._start = f"{Fore.BLUE}| {self._ENDC}"
        self._end = f"{Fore.BLUE}|{self._ENDC}\n"

    def _item_as_str(self, item: Piece) -> str:
        c = self._char[item]
        return f"{c[0]}{c[1]} {self._ENDC}"

class BWTerminal(Terminal):
    def __init__(self) -> None:
        super().__init__()
        self._char = {
            Piece.RED : '⬤',
            Piece.YELLOW : '◯',
            Piece.EMPTY : '_'
        }

    def _item_as_str(self, item: Piece) -> str:
        return f"{self._char[item]} "