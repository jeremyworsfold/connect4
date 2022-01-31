import numpy as np
from abc import ABC, abstractmethod
from colorama import Fore, init

from connect4.board import Board, Piece, WinState

class Display(ABC):

    @abstractmethod
    def update(self, board: Board) -> None:
        """Update the display with the latest version of the board"""
        pass 

    @abstractmethod
    def end_game(self, board: Board, winstate: WinState) -> None:
        """Update the display with the final board state and statement of the game result."""
        pass 


class Terminal(Display):
    def __init__(self) -> None:
        super().__init__()
        self._start = "| "
        self._end = "|\n"

    @abstractmethod
    def _piece_as_str(self, piece:Piece) -> str:
        """Return representation of a piece to be printed to the terminal"""
        pass

    def __getitem__(self, piece: Piece) -> str:
        return self._piece_as_str(piece)

    def _slots(self, valid_moves: np.ndarray) -> str:
        """Returns string of the valid columns and blank spaces in place of invalid columns"""
        vals = np.arange(1,len(valid_moves)+1)
        line = list(np.where(valid_moves,vals," "))  # if not valid move, put " " in place.
        line.insert(0," ")  # align with the printed board
        line.append("\n")
        return " ".join(line)

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
            print(f"Player {self[winstate.winner]} has just won.")
        else:
            print(f"The Game is a draw.")


class ColorTerminal(Terminal):
    def __init__(self) -> None:
        super().__init__()
        init()
        self._char = {
            Piece.RED : '⬤',
            Piece.YELLOW : '⬤',
            Piece.EMPTY : '◯'
        }
        self._col = {
            Piece.RED : Fore.RED,
            Piece.YELLOW : Fore.YELLOW,
            Piece.EMPTY : Fore.BLUE,
        }
        self._ENDC = '\033[0m'
        self._start = f"{Fore.BLUE}| {self._ENDC}"
        self._end = f"{Fore.BLUE}|{self._ENDC}\n"

    def _piece_as_str(self, piece: Piece) -> str:
        return f"{self._col[piece]}{self._char[piece]} {self._ENDC}"


class BWTerminal(Terminal):
    def __init__(self) -> None:
        super().__init__()
        self._char = {
            Piece.RED : '⬤',
            Piece.YELLOW : '◯',
            Piece.EMPTY : '_'
        }

    def _piece_as_str(self, piece: Piece) -> str:
        return f"{self._char[piece]} "