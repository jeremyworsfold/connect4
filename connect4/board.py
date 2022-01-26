from enum import Enum
import numpy as np
from collections import namedtuple

class Piece(Enum):
    EMPTY = ' '
    RED = 'R'
    YELLOW = 'Y'

class Board:
    LENGTH = 7
    HEIGHT = 6
    WIN_L = 4

    WinState = namedtuple('WinState', ['is_ended', 'winner'])

    def __init__(self) -> None:
        self.grid = np.full((self.HEIGHT, self.LENGTH), Piece.EMPTY, dtype=Piece)
        self.input_idx = np.zeros(self.LENGTH, dtype=int)
        self.last_pos = (0,0)

    def add_piece(self, col, piece: Piece) -> None:
        if self.input_idx[col] >= self.HEIGHT:
            raise ValueError(f"Can't put piece in column {col}.")
        else:
            self.grid[self.input_idx[col],col] = piece
            self.last_pos = (self.input_idx[col], col)
            self.input_idx[col] += 1

    @property
    def valid_moves(self) -> np.ndarray:
        return self.input_idx < self.HEIGHT

    def _is_winner(self, player_pieces:np.ndarray) -> bool:
        r, c  = self.last_pos
        L = self.WIN_L
        C, R = self.LENGTH - 1, self.HEIGHT - 1

        # check diagonals first, return if win is found
        bottomright = min(R - r, C - c)
        topright = min(r, C - c)
        for i in range(max(0, L- bottomright - 1), min(L - 1, r, c) + 1):  #  topleft = min(r,c)
            if all(player_pieces[r - i + x][c - i + x] for x in range(L)):
                    return True

        for i in range(max(0, L - topright - 1), min(L - 1, R - r, c) + 1):  #  bottomleft = min(R-r,c)
            if all(player_pieces[r + i - x][c - i + x] for x in range(L)):
                    return True

        # otherwise check columns and rows
        mincol, minrow = max(0, c - L + 1), max(0, r - L + 1)
        lr = max(player_pieces[r, i:min(i + L, C)].sum() for i in range(mincol, c + 1))
        ud = max(player_pieces[i:min(i + L, R), c].sum() for i in range(minrow, r + 1))
        return lr >= L or ud >= L


    def get_win_state(self, player:Piece) -> WinState:
        player_pieces = self.grid == player
        # Win
        if self._is_winner(player_pieces):
            return self.WinState(True, player)
        # Draw
        if not self.valid_moves.any():
            return self.WinState(True, Piece.EMPTY)
        # Game is not ended yet.
        return self.WinState(False, Piece.EMPTY)