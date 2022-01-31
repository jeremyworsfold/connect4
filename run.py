from connect4.board import Board, Piece, WinState
from connect4.terminal import ColorTerminal, BWTerminal
from connect4.players import Human, Rand, Opponents


if __name__ == "__main__":
    b = Board()
    display = BWTerminal()
    winstate = WinState(False, Piece(Piece.EMPTY))
    display.update(b)
    players = Opponents(Human(Piece(Piece.RED)), Rand(Piece(Piece.YELLOW)))
    while not winstate.is_ended:
        column = players.current.get_action(b.valid_inputs)
        winstate = b.update(column, players.current.color)
        display.update(b)
        players.swap()
    display.end_game(b, winstate)