#from unittest import TestCase
import pytest
import numpy as np

from connect4 import Board, WinState, Piece
from tests.fixtures import (
    nearly_full_board, p1_winner_board, drawn_board
    )

@pytest.mark.parametrize("col", list(range(7)))
@pytest.mark.parametrize("piece", [Piece.P1, Piece.P2])
def test_board_add_piece(col: int, piece: Piece):
    b = Board()

    b.add_piece(col, piece)

    assert b.input_idx[col] == 1
    assert b.grid[b.input_idx[col]-1, col] == piece

    b.input_idx[col] = b.n_r
    with pytest.raises(ValueError) as e:
        b.add_piece(col, piece)

    assert str(e.value) == f"Can't put piece in column {col}."


@pytest.mark.parametrize("col", [-1,10])
@pytest.mark.parametrize("piece", [Piece.P1, Piece.P2])
def test_board_add_piece_out_of_range(col: int, piece: Piece):
    b = Board()
    with pytest.raises(IndexError) as e:
        b.add_piece(col, piece)
    
    assert str(e.value) == f"Can't put piece in column {col}."


def test_valid_moves(nearly_full_board, drawn_board):
    b = nearly_full_board
    assert all(b.valid_moves == np.array([0, 0, 1, 0, 0, 0, 0]).astype(bool))
    assert b.valid_inputs.item() == 2

    b = drawn_board
    assert all(b.valid_moves == np.array([0, 0, 0, 0, 0, 0, 0]).astype(bool))
    assert len(b.valid_inputs) == 0


def test_board_update(nearly_full_board):
    b1 = nearly_full_board
    assert b1.update(2, Piece.P1) == WinState(True, Piece.P1)

    b2 = nearly_full_board
    print(b2.grid)
    assert b2.update(2, Piece.P2) == WinState(True, Piece.P2)

    b3 = nearly_full_board
    with pytest.raises(ValueError) as e:
        b3.update(0, Piece.P1)
    assert str(e.value) == f"Can't put piece in column {0}."


def test_winner(nearly_full_board, p1_winner_board, drawn_board):
    b = nearly_full_board
    assert b.get_win_state(Piece.P1) == WinState(False, Piece.EMPTY)
    b = p1_winner_board
    assert b.get_win_state(Piece.P1) == WinState(True, Piece.P1)
    b = drawn_board
    assert b.get_win_state(Piece.P1) == WinState(True, Piece.EMPTY)
