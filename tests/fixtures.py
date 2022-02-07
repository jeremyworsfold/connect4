import pytest
import numpy as np
from connect4 import Board, Piece

@pytest.fixture
def nearly_full_board():
    board = Board()

    a, b, c = Piece.EMPTY, Piece.P1, Piece.P2

    board.grid = np.array(
        [[b, b, c, b, c, b, c],
        [c, c, b, c, c, b, c],
        [b, c, b, c, b, c, b],
        [c, b, a, b, b, b, c],
        [c, b, a, c, c, c, b],
        [b, b, a, b, c, c, c]]
    , dtype=Piece)

    board.input_idx = np.array([6, 6, 3, 6, 6, 6, 6])
    board.last_pos = (5,0)
    
    return board

@pytest.fixture
def p1_winner_board():
    b = Board()

    b.grid = np.array(
        [[2, 2, 3, 2, 3, 2, 3],
        [3, 3, 2, 3, 3, 2, 3],
        [2, 3, 2, 3, 2, 3, 2],
        [3, 2, 2, 2, 2, 2, 3],
        [3, 2, 1, 3, 3, 3, 2],
        [2, 2, 1, 2, 3, 3, 3]]
    ).astype(type(Piece))
    b.input_idx = np.array([6, 6, 3, 6, 6, 6, 6])
    b.last_pos = (3,2)

    return b

@pytest.fixture
def drawn_board():
    b = Board()

    b.grid = np.array(
        [[2, 2, 3, 2, 3, 2, 3],
        [3, 3, 2, 3, 2, 2, 3],
        [2, 2, 2, 3, 3, 3, 2],
        [3, 3, 3, 2, 2, 2, 3],
        [3, 2, 2, 3, 3, 3, 2],
        [2, 3, 3, 2, 3, 3, 3]]
    ).astype(Piece)
    b.input_idx = np.array([6, 6, 6, 6, 6, 6, 6])
    b.last_pos = (5,2)

    return b