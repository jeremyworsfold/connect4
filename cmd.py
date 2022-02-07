from connect4.board import Board, Piece, WinState
from connect4.terminal import ColorTerminal, BWTerminal, Terminal
from connect4.players import Human, Rand, Opponents

import numpy as np

if __name__ == "__main__":
    b = Board()
    display = ColorTerminal()
    winstate = WinState(False, Piece(Piece.EMPTY))
    display.update(b)
    players = Opponents(Human(Piece(Piece.P1)), Rand(Piece(Piece.P2)))
    while not winstate.is_ended:
        print(np.array(b.grid,dtype=int))
        column = players.current.get_action(b.valid_inputs)
        winstate = b.update(column, players.current.color)
        display.update(b)
        players.swap()
    display.end_game(b, winstate)
