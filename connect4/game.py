from typing import Tuple
import pygame as pg
from pygame import KEYDOWN, QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.event import Event, post
import os

from connect4.board import Board, Piece, WinState
from connect4.players import Opponents
from connect4.screen import TextRenderer
from connect4.theme import PygameTheme
from connect4.tokens import Token, HoverToken, Marker, draw_circle

AI_TURN = pg.event.custom_type()
END_GAME = pg.event.custom_type()
INVALID_COL = pg.event.custom_type()
TOKEN_ANIM = pg.event.custom_type()
PLAYER_TURN = pg.event.custom_type()


UNIT = 250
WIDTH = 7 * UNIT
HEIGHT = 8 * UNIT
SCREEN_START_SIZE = (WIDTH, HEIGHT)


def row_col(r: int, c: int, w, spacing) -> Tuple[int, int]:
    return int(w - (r) * spacing), int((c) * spacing)


def col_from_pos(p: int, size) -> int:
    width = size[0]
    spacing = width / 7
    return int(p // spacing)

def map_mouse(x, scale_x, screen_w):
    abs_w = screen_w * scale_x
    start = (screen_w - abs_w) / 2
    return int(min(max(0, WIDTH * (x - start) / abs_w), WIDTH-1))


class PyGame:
    def __init__(self, players: Opponents, theme: PygameTheme, scale=0.4, fps=10) -> None:
        self.board = Board()
        self.thm = theme
        self.players = players

        self.textpos = (int(UNIT / 10), int(UNIT/8))
        self.radius = int(0.4*UNIT)
        self.background = self.thm.BACKGROUND

        startscale = (int(scale*SCREEN_START_SIZE[0]), int(scale*SCREEN_START_SIZE[1]))

        os.environ["SDL_VIDEO_CENTERED"] = '1'
        pg.init()
        pg.display.set_caption("Connect 4")
        self.screen = pg.display.set_mode(startscale, pg.RESIZABLE)#|pg.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.image = pg.Surface(SCREEN_START_SIZE).convert()
        self.image_rect = self.image.get_rect()
        self.clock = pg.time.Clock()
        self.fps = fps
        self.scale = (1,1)

        self.textrenderer = TextRenderer((5, 10), theme.FONT_FAMILY, theme.FONT_SIZE, theme.FONT_COL, UNIT, WIDTH, self.background)
        self.sprites = pg.sprite.Group()
        self.finallayer = pg.sprite.Group()
        self.init_screen()

        self.winstate = WinState(False, Piece(Piece.EMPTY))
        self.running = True

    def init_screen(self):
        self.hovertoken = HoverToken(self.current_color, self._row_col(-1, -1), UNIT)
        self.marker = Marker(self.background, self._row_col(-1, -1), UNIT)
        self.finallayer.add(self.marker)
        self.sprites.add(self.hovertoken)

        self.image.fill(self.thm.BOARD)
        self.draw_board()
        self.textrenderer.prompt_and_blit(self.image, range(7), self.players.current.color)
        pg.display.update()

    def draw_board(self):
        self.image.fill(self.thm.BOARD, (0, UNIT, WIDTH, HEIGHT))
        for i in range(7):
            for j in range(6):
                r, c = self._row_col(j, i)
                draw_circle(self.image, int(c+UNIT/2), int(r+UNIT/2), self.radius, self.background)
        pg.draw.rect(
            self.image, self.background, pg.Rect(0, UNIT, WIDTH, HEIGHT - 7 * UNIT)
        )

    def add_token(self, position: Tuple[int, int]):
        token = Token(self.current_color, self._row_col(*position), UNIT, WIDTH)
        self.sprites.add(token)

    def player_turn(self, action: int):
        self.winstate = self.board.update(action, self.players.current.color)
        self.add_token(self.board.last_pos)
        self.marker.change_pos(self._row_col(*self.board.last_pos))
        if self.winstate.is_ended:
            post(Event(END_GAME))
        self.players.swap()

        self.textrenderer.prompt_and_blit(self.image, self.board.valid_inputs, self.players.current.color)

    def human_turn(self, a):
        if a in self.board.valid_inputs:
            self.player_turn(a)
            if not self.winstate.is_ended:
                self.last = pg.time.get_ticks()
                self.hovertoken.kill()
                post(Event(AI_TURN))
        else:
            post(Event(INVALID_COL, {"col": a}))

    def ai_turn(self):
        now = pg.time.get_ticks()
        if now - self.last >= 400:
            a = self.players.current.get_action(self.board.valid_inputs)
            self.player_turn(a)
            self.hovertoken = HoverToken(self.current_color, self._row_col(-1, -1), UNIT)
            self.sprites.add(self.hovertoken)
        else:
            pg.event.post(Event(AI_TURN))

    def _row_col(self, r: int, c: int) -> Tuple[int, int]:
        return row_col(r, c, WIDTH, UNIT)

    @property
    def current_color(self):
        return self.thm[self.players.current.color]

    def end_game(self) -> None:
        self.textrenderer.end_game(self.winstate)
        self.textrenderer.blit_text(self.image)
        self.hovertoken.kill()
        pg.event.set_blocked(None)
        pg.event.set_allowed(QUIT)

    def set_scale(self, size):
        w_ratio = size[0]/float(self.screen_rect.w)
        h_ratio = size[1]/float(self.screen_rect.h)
        self.scale = (w_ratio, h_ratio)

    def update(self):
        self.draw_board()
        self.sprites.update()
        self.sprites.draw(self.image)
        self.finallayer.update()
        self.finallayer.draw(self.image)
        if self.screen_rect.size != SCREEN_START_SIZE:
            fit_to_rect = self.image_rect.fit(self.screen_rect)
            fit_to_rect.center = self.screen_rect.center
            scaled = pg.transform.smoothscale(self.image, fit_to_rect.size)
            self.screen.blit(scaled, fit_to_rect)
            self.set_scale(fit_to_rect.size)
        else:
            self.screen.blit(self.image, (0,0))

    def event_loop(self):
        for event in pg.event.get():
            if event.type == KEYDOWN and event.unicode.isnumeric():
                self.human_turn(int(event.unicode) - 1)
            elif event.type == MOUSEBUTTONDOWN:
                pos = map_mouse(event.pos[0], self.scale[0], self.screen_rect.w)
                a = col_from_pos(pos, SCREEN_START_SIZE)
                self.human_turn(a)
            elif event.type == AI_TURN:
                self.ai_turn()
            elif event.type == INVALID_COL:
                self.textrenderer.error_prompt(event.col)
                self.textrenderer.highlight_cols(self.board.valid_inputs)
                self.textrenderer.blit_text(self.image)
            if event.type == MOUSEMOTION:
                pos = map_mouse(event.pos[0], self.scale[0], self.screen_rect.w)
                self.hovertoken.change_pos(self._row_col(6, pos // UNIT))
            elif event.type == END_GAME:
                self.end_game()
            elif event.type == QUIT:
                pg.quit()
                quit()
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                self.screen_rect = self.screen.get_rect()

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            pg.display.update()
            pg.display.flip()
            self.clock.tick(self.fps)