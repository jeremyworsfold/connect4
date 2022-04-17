import pygame as pg

from connect4.visuals.tokens import draw_circle, row_col
from connect4.visuals.theme import RGBColor

UNIT = 250
WIDTH = 7 * UNIT
HEIGHT = 8 * UNIT
RADIUS = int(0.4 * UNIT)


class Screen:
    def __init__(self, back_color: RGBColor, board_color: RGBColor, scale=0.4) -> None:
        startscale = (
            int(scale * WIDTH),
            int(scale * HEIGHT),
        )
        self.back_col = back_color
        self.board_col = board_color
        self.screen = pg.display.set_mode(startscale, pg.RESIZABLE)
        self.screen_rect = self.screen.get_rect()
        self.image = pg.Surface((WIDTH, HEIGHT)).convert()
        self.image_rect = self.image.get_rect()

        self.image.fill(board_color)
        self.draw_board()
        self.scale = (1, 1)

    @property
    def xscale(self):
        return self.scale[0]

    @property
    def width(self):
        return self.screen_rect.w

    def resize(self, size):
        self.screen = pg.display.set_mode(size, pg.RESIZABLE)
        self.screen_rect = self.screen.get_rect()

    def set_scale(self, size):
        w_ratio = size[0] / float(self.screen_rect.w)
        h_ratio = size[1] / float(self.screen_rect.h)
        return (w_ratio, h_ratio)

    def map_mouse(self, x: int):
        abs_w = self.width * self.xscale
        start = (self.width - abs_w) / 2
        return int(min(max(0, WIDTH * (x - start) / abs_w), WIDTH - 1))

    def transform_scale(self):
        if self.screen_rect.size == (WIDTH, HEIGHT):
            self.screen.blit(self.image, (0, 0))
            return

        fit_to_rect = self.image_rect.fit(self.screen_rect)
        fit_to_rect.center = self.screen_rect.center
        scaled = pg.transform.smoothscale(self.image, fit_to_rect.size)
        self.screen.blit(scaled, fit_to_rect)
        self.set_scale(fit_to_rect.size)

    def draw_board(self):
        self.image.fill(self.board_col, (0, UNIT, WIDTH, HEIGHT))
        for i in range(7):
            for j in range(6):
                r, c = row_col(j, i, WIDTH, UNIT)
                draw_circle(
                    self.image,
                    int(c + UNIT / 2),
                    int(r + UNIT / 2),
                    RADIUS,
                    self.back_col
                )
        pg.draw.rect(
            self.image, self.back_col, pg.Rect(0, UNIT, WIDTH, HEIGHT - 7 * UNIT)
        )

    def blit_text(self, text, position):
        self.image.fill(self.back_col, (0, 0, WIDTH, HEIGHT))
        self.image.blit(text, position)
