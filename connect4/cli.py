import numpy as np

from connect4.board import Board, Piece, WinState
from connect4.players import Opponents
from connect4.configs import TerminalTheme


class Terminal:
    def __init__(self, theme: TerminalTheme) -> None:
        super().__init__()
        self.theme = theme
        self._ENDC = "\033[0m"
        self._start = theme.start
        self._end = theme.end

    def __getitem__(self, piece: Piece) -> str:
        return self._piece_as_str(piece)

    def _slots(self, valid_moves: np.ndarray) -> str:
        """Returns string of the valid columns and blank spaces in place of invalid columns"""
        vals = np.arange(1, len(valid_moves) + 1)
        line = list(
            np.where(valid_moves, vals, " ")
        )  # if not valid move, put " " in place.
        line.insert(0, " ")  # align with the printed board
        line.append("\n")
        return " ".join(line)

    def _piece_as_str(self, piece: Piece) -> str:
        return f"{self.theme.back}{self.theme[piece]} {self._ENDC}"

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
            print(f"Player {self.theme[winstate.winner]}{self._ENDC} has just won.")
        else:
            print("The Game is a draw.")

    def main(self, players: Opponents, b: Board):
        winstate = WinState(False, Piece(Piece.EMPTY))
        self.update(b)
        while not winstate.is_ended:
            column = players.current.get_action(b)
            winstate = b.update(column, players.current.color)
            self.update(b)
            players.swap()
        self.end_game(b, winstate)
