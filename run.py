from connect4.board import Board, Piece
from connect4.terminal import ColorTerminal, BWTerminal
from connect4.players import Human, Rand


if __name__ == "__main__":
    b = Board()
    display = BWTerminal()
    display.update(b)
    now, prev = 0, 1
    player = (Human(Piece('R')), Rand(Piece('Y')))
    while not b.get_win_state(player[prev].color).is_ended:
        column = player[now].get_action(b)
        b.add_piece(int(column), player[now].color)
        display.update(b)
        prev = now
        now = 1*(1-now)