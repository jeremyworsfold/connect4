from enum import Enum, auto
from typing import NamedTuple
import numpy as np


class Piece(Enum):
    EMPTY = auto()
    P1 = auto()
    P2 = auto()


class WinState(NamedTuple):
    is_ended: bool
    winner: Piece


class Board:
    # number of rows and columns
    n_c = 7
    n_r = 6
    # required length to win
    four = 4

    def __init__(self) -> None:
        self.grid = np.full((self.n_r, self.n_c), Piece.EMPTY, dtype=Piece)
        self.input_idx = np.zeros(self.n_c, dtype=int)
        self.last_pos = (-1, -1)

    def add_piece(self, col, piece: Piece) -> None:
        """Adds a piece to the board in the selected column. Updates the column height."""
        if self.input_idx[col] >= self.n_r:
            raise ValueError(f"Can't put piece in column {col}.")
        else:
            self.grid[self.input_idx[col], col] = piece
            self.last_pos = (self.input_idx[col], col)
            self.input_idx[col] += 1

    def update(self, col, piece: Piece) -> WinState:
        """Adds a piece to the board and does a check on the winstate given the new piece added.
        Returns: Winstate"""
        self.add_piece(col, piece)
        return self.get_win_state(piece)

    @property
    def valid_moves(self) -> np.ndarray:
        """Returns boolean numpy array of whether a piece can be placed in each column in the range (0,n_c-1)"""
        return self.input_idx < self.n_r  # type: ignore

    @property
    def valid_inputs(self) -> np.ndarray:
        """Returns numpy array of the allowed columns for piece placement in the range (0,n_c-1) inclusive."""
        return np.arange(0, self.n_c)[np.flatnonzero(self.valid_moves)]  # type: ignore

    def _is_winner(self, grid: np.ndarray) -> bool:
        """Checks if there is a new winner given the location of the current player's pieces."""
        r, c = self.last_pos
        L = self.four
        C, R = self.n_c - 1, self.n_r - 1

        # check diagonals first, return if win is found
        bottomright = min(R - r, C - c)
        topright = min(r, C - c)
        for i in range(
            max(0, L - bottomright - 1), min(L - 1, r, c) + 1
        ):  # topleft = min(r,c)
            if all(grid[r - i + x][c - i + x] for x in range(L)):
                return True

        for i in range(
            max(0, L - topright - 1), min(L - 1, R - r, c) + 1
        ):  # bottomleft = min(R-r,c)
            if all(grid[r + i - x][c - i + x] for x in range(L)):
                return True

        # otherwise check columns and rows
        mincol, minrow = max(0, c - L + 1), max(0, r - L + 1)
        lr = max(grid[r, i : min(i + L, C)].sum() for i in range(mincol, c + 1))
        ud = max(grid[i : min(i + L, R), c].sum() for i in range(minrow, r + 1))
        return lr >= L or ud >= L  # type: ignore

    def get_win_state(self, player: Piece) -> WinState:
        """Checks if someone has won and returns Winstate declaring if it has ended and who won."""
        player_pieces = self.grid == player
        if self._is_winner(player_pieces):
            return WinState(True, player)
        # Draw
        if not self.valid_moves.any():
            return WinState(True, Piece.EMPTY)
        # Game is not ended yet.
        return WinState(False, Piece.EMPTY)
