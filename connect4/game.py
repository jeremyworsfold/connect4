import pygame as pg
from pygame import KEYDOWN, QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.event import Event, post

from connect4.board import Board, Piece, WinState
from connect4.players import Opponents
from connect4.screen import ScreenHandler

AI_TURN = pg.event.custom_type()
END_GAME = pg.event.custom_type()
INVALID_COL = pg.event.custom_type()


class PyGame:
    def __init__(self, players: Opponents, scrnhandler: ScreenHandler) -> None:
        self.screenhandler = scrnhandler
        self.running = True
        self.players = players
        self.winstate = WinState(False, Piece(Piece.EMPTY))

    def update_screen(self, board: Board, last_pos) -> None:
        r, c = board.last_pos
        row, col = last_pos
        self.screenhandler.draw_piece(self.players.previous.color, row, col, dot=False)
        self.screenhandler.draw_piece(self.players.current.color, r, c, dot=True)

    def player_turn(self, action: int, board: Board):
        last_pos = board.last_pos
        self.winstate = board.update(action, self.players.current.color)
        self.update_screen(board, last_pos)
        if self.winstate.is_ended:
            post(Event(END_GAME))
        self.players.swap()
        self.screenhandler._prompt_player(self.players.current.color, board.valid_moves)
        return board

    def end_game(self) -> None:
        self.screenhandler.end_game(self.winstate)
        for event in [KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION]:
            pg.event.set_blocked(event)

    def human_turn(self, board, a):
        if a in board.valid_inputs:  # check
            board = self.player_turn(a, board)
            if not self.winstate.is_ended:
                post(Event(AI_TURN))
        else:
            post(Event(INVALID_COL, {"col": a}))
        return board

    def run(self, b: Board) -> None:
        while self.running:
            for event in pg.event.get():
                if event.type == KEYDOWN and event.unicode.isnumeric():
                    self.human_turn(b, int(event.unicode) - 1)
                elif event.type == MOUSEBUTTONDOWN:
                    a = self.screenhandler.col_from_pos(event.pos)
                    self.human_turn(b, a)

                elif event.type == AI_TURN:
                    a = self.players.current.get_action(b.valid_inputs)
                    b = self.player_turn(a, b)

                elif event.type == INVALID_COL:
                    self.screenhandler.error_prompt(event.col)

                if event.type == MOUSEMOTION:
                    self.screenhandler.highlight_slot(
                        self.players.current.color, event.pos
                    )

                elif event.type == END_GAME:
                    self.end_game()

                elif event.type == QUIT:
                    pg.quit()
                    quit()
                pg.display.update()
                pg.display.flip()
