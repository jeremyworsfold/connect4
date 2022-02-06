from typing import Tuple
import pygame as pg
from pygame import gfxdraw
import numpy as np
import os
from pathlib import Path

from connect4.theme import Theme
from connect4.board import Piece, WinState


def darker(rgb: Tuple[int, int, int]):
    return tuple(int(0.9*val) for val in rgb)


class ScreenHandler:
    def __init__(self, theme: Theme, screenwidth: int) -> None:
        self.thm = theme
        self.WIDTH = screenwidth
        self.SPACING = int(self.WIDTH / 7)
        self.HEIGHT = self.WIDTH + self.SPACING
        self.TEXTPOS = (5, 10)
        self.RADIUS = int(0.4*self.SPACING)

        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{50},{50}"
        pg.init()
        pg.display.set_caption("Connect 4")
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.font.init()
        font_path = Path.cwd() / 'assets' / 'fonts' / f'{self.thm.FONT_FAMILY}.ttf'
        self.font = pg.font.Font(font_path, self.thm.FONT_SIZE)
        # self.font = pg.font.SysFont(self.thm.FONT_FAMILY, 24)
        self.textsurface = [
            self.font.render(f"{i+1}", True, self.thm.FONT_COL) for i in range(7)
        ]

        self._togo = {
            Piece.P1: "Player 1",
            Piece.P2: "Player 2",
        }

        self._init_screen()

    def _init_screen(self):
        self.screen.fill(self.thm.BOARD)
        for i, txt in enumerate(self.textsurface):
            self.screen.blit(txt, ((i + 0.5) * self.SPACING - 10, self.SPACING / 2))
            for j in range(6):
                r, c = self.get_row_col(j, i)
                self._draw_circle(c, r, self.RADIUS, self.thm.BACKGROUND)
        pg.draw.rect(
            self.screen, self.thm.BACKGROUND, pg.Rect(0, 0, self.WIDTH, self.HEIGHT - 6 * self.SPACING)
        )
        pg.display.update()

    def col_from_pos(self, p: Tuple[int, int]) -> int:
        if (
            p[1] > self.SPACING
            and (p[0] % self.SPACING) > self.SPACING / 8
            and (p[0] % self.SPACING) < 7 * self.SPACING / 8
        ):
            return p[0] // self.SPACING
        else:
            return -1

    def get_row_col(self, r: int, c: int) -> Tuple[int, int]:
        return int(self.WIDTH - (r - 0.5) * self.SPACING), int((c + 0.5) * self.SPACING)

    def _draw_circle(self, x, y, radius, color, draw_inner=False):
        pos_x, pos_y = int(x), int(y)
        gfxdraw.aacircle(self.screen, pos_x, pos_y, radius, color)
        gfxdraw.filled_circle(self.screen, pos_x, pos_y, radius, color)
        if draw_inner:
            gfxdraw.aacircle(self.screen, pos_x, pos_y, int(0.75*radius), darker(color))
            gfxdraw.filled_circle(self.screen, pos_x, pos_y, int(0.75*radius), darker(color))

    def draw_piece(self, color: Piece, row: int, col: int, dot=True) -> None:
        r, c = self.get_row_col(row, col)
        self._draw_circle(c, r, self.RADIUS, self.thm[color], draw_inner=True)
        if dot:
            self._draw_circle(c, r, int(self.RADIUS / 8), self.thm.BOARD)

    def highlight_slot(self, piece: Piece, pos: Tuple[int, int]):
        col = pos[0] // self.SPACING  # self.col_from_pos(pos)
        for i in range(7):
            r, c = self.get_row_col(6, i)
            fill_color = self.thm[piece] if col == i else self.thm.BACKGROUND
            self._draw_circle(c, r, self.RADIUS, fill_color, draw_inner=col==i)

    def _prompt_player(self, color: Piece, valid_moves: np.ndarray) -> None:
        self.screen.fill(self.thm.BACKGROUND, (0, 0, self.WIDTH, self.SPACING))
        prompt = self.font.render(
            f"{self._togo[color]} to go...", True, self.thm.FONT_COL
        )
        self.screen.blit(prompt, self.TEXTPOS)
        for i, val in enumerate(valid_moves):
            if val:
                self.screen.blit(
                    self.textsurface[i], ((i + 0.5) * self.SPACING - 5, self.SPACING / 2)
                )

    def end_game(self, winstate: WinState) -> None:
        self.screen.fill(self.thm.BACKGROUND, (0, 0, self.WIDTH, self.HEIGHT - 6 * self.SPACING))
        game_ended = self.font.render(
            f"{self._togo[winstate.winner]} player has won!", True, self.thm.FONT_COL
        )
        self.screen.blit(game_ended, self.TEXTPOS)

    def error_prompt(self, action: int) -> None:
        if not action == -1:
            prompt = self.font.render(
                f"Cannot add piece to column {action}", True, self.thm.FONT_COL
            )
            self.screen.blit(prompt, (250, 20))
