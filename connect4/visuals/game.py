import pygame as pg
from pygame import KEYDOWN, QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, VIDEORESIZE
from pygame.event import Event, post
import os

from connect4.board import Board, Piece, WinState
from connect4.players import Opponents
from connect4.visuals.text import TextHandler
from connect4.visuals.theme import PygameTheme
from connect4.visuals.tokens import Sprites
from connect4.visuals.screen import Screen, WIDTH, UNIT

AI_TURN = pg.event.custom_type()
END_GAME = pg.event.custom_type()
INVALID_COL = pg.event.custom_type()
TOKEN_ANIM = pg.event.custom_type()
PLAYER_TURN = pg.event.custom_type()


def col_from_pos(p: int) -> int:
    return int(p // UNIT)


class PyGame:
    def __init__(
        self, players: Opponents, theme: PygameTheme, scale=0.4, fps=10
    ) -> None:
        self.board = Board()
        self.thm = theme
        self.players = players
        self.fps = fps
        self.winstate = WinState(False, Piece(Piece.EMPTY))
        self.running = True

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pg.init()
        pg.display.set_caption("Connect 4")
        self.clock = pg.time.Clock()

        self.screen = Screen(theme.background, theme.board, scale)
        self.textrenderer = TextHandler(
            (5, 10),
            theme.f_family,
            theme.f_size,
            theme.f_color,
            UNIT,
            WIDTH,
            theme.background,
        )
        self.sprites = Sprites(UNIT, WIDTH, theme.background, self.current_color)

        self.textrenderer.prompt_and_blit(
            self.screen, range(7), self.players.curr_piece
        )
        pg.display.update()

    @property
    def current_color(self):
        return self.thm[self.players.curr_piece]

    def player_turn(self, action: int):
        self.winstate = self.board.update(action, self.players.curr_piece)
        self.sprites.add_token(self.board.last_pos, self.current_color)
        self.sprites.move_marker(self.board.last_pos)
        if self.winstate.is_ended:
            post(Event(END_GAME))
        self.players.swap()

        self.textrenderer.prompt_and_blit(
            self.screen, self.board.valid_inputs, self.players.curr_piece
        )

    def human_turn(self, a):
        if a not in self.board.valid_inputs:
            post(Event(INVALID_COL, {"col": a}))
            return

        self.player_turn(a)
        if not self.winstate.is_ended:
            self.last = pg.time.get_ticks()
            self.sprites.kill_hovertoken()
            post(Event(AI_TURN))

    def ai_turn(self):
        now = pg.time.get_ticks()
        if now - self.last < 400:
            pg.event.post(Event(AI_TURN))
            return

        a = self.players.get_action(self.board)
        self.player_turn(a)
        self.sprites.add_hovertoken(self.current_color)

    def invalid_col(self, col):
        self.textrenderer.error_prompt(col)
        self.textrenderer.highlight_cols(self.board.valid_inputs)
        self.textrenderer.blit_text(self.screen)

    def mouse_token_placement(self, position):
        pos = self.screen.map_mouse(position[0])
        a = col_from_pos(pos)
        self.human_turn(a)

    def move_hover(self, pos):
        position = self.screen.map_mouse(pos[0])
        self.sprites.move_hovertoken(position)

    def end_game(self) -> None:
        self.textrenderer.end_game(self.winstate)
        self.textrenderer.blit_text(self.screen)
        self.sprites.kill_hovertoken()
        pg.event.set_blocked(None)
        pg.event.set_allowed(QUIT)

    def update(self):
        self.screen.draw_board()
        self.sprites.draw(self.screen.image)
        self.screen.transform_scale()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == KEYDOWN and event.unicode.isnumeric():
                self.human_turn(int(event.unicode) - 1)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_token_placement(event.pos)
            elif event.type == AI_TURN:
                self.ai_turn()
            elif event.type == INVALID_COL:
                self.invalid_col(event.col)
            if event.type == MOUSEMOTION:
                self.move_hover(event.pos)
            elif event.type == END_GAME:
                self.end_game()
            elif event.type == VIDEORESIZE:
                self.screen.resize(event.size)
            elif event.type == QUIT:
                pg.quit()
                quit()

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.fps)
