import numpy as np
from collections import namedtuple

from connect4.board import Piece


class BoardOld: 
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
 
    def _is_straight_winner(self, player_pieces: np.ndarray) -> bool: 
        """Checks if player_pieces contains a vertical or horizontal win.""" 
        run_lengths = [player_pieces[:, i:i+self.WIN_L].sum(axis=1) 
                       for i in range(len(player_pieces) - self.WIN_L + 1)] 
        return any(x.max() >= self.WIN_L for x in run_lengths) 

    def _is_diagonal_winner(self, player_pieces: np.ndarray) -> bool: 
        """Checks if player_pieces contains a diagonal win.""" 
        L = len(player_pieces) 
        for i in range(L - self.WIN_L + 1): 
            for j in range(L - self.WIN_L + 1): 
                if all(player_pieces[i + x][j + x] for x in range(self.WIN_L)): 
                    return True 
            for j in range(self.WIN_L - 1, L): 
                if all(player_pieces[i + x][j - x] for x in range(self.WIN_L)): 
                    return True 
        return False 
 
    def get_win_state(self, player:Piece) -> WinState: 
        player_pieces = self.grid == player 
        # Check rows & columns for win 
        if (self._is_straight_winner(player_pieces) or 
            self._is_straight_winner(player_pieces.T) or 
            self._is_diagonal_winner(player_pieces)): 
            return self.WinState(True, player) 
 
        # Draw 
        if not self.valid_moves.any(): 
            return self.WinState(True, Piece.EMPTY) 
 
        # Game is not ended yet. 
        return self.WinState(False, Piece.EMPTY)