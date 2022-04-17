import pygame as pg
from pathlib import Path
from queue import Queue

from connect4.board import Piece, WinState
from connect4.visuals.screen import Screen


class TextHandler:
    def __init__(
        self, text_pos, f_family, f_size, f_col, spacing, width, background
    ) -> None:
        self.text_pos = text_pos
        self.width = width
        self.background = background
        self.height = spacing
        self.col = f_col
        self.queue = Queue()
        pg.font.init()
        font_path = Path.cwd() / "assets" / "fonts" / f"{f_family}.ttf"
        self.font = pg.font.Font(font_path, f_size)
        self.cols = [self.font.render(f"{i+1}", True, f_col) for i in range(7)]
        self.col_positions = [
            (int((i + 0.5) * spacing), int(spacing / 2)) for i in range(7)
        ]

        self.color_to_player = {
            Piece.P1: "Player 1",
            Piece.P2: "Player 2",
        }

    def highlight_cols(self, valid_inputs):
        for i in valid_inputs:
            self.queue.put((self.cols[i], self.col_positions[i]))

    def prompt_player(self, color: Piece) -> pg.Surface:
        text = self.font.render(
            f"{self.color_to_player[color]} to go...", True, self.col
        )
        self.queue.put((text, self.text_pos))

    def end_game(self, winstate: WinState) -> None:
        text = self.font.render(
            f"{self.color_to_player[winstate.winner]} player has won!", True, self.col
        )
        self.queue.put((text, self.text_pos))

    def error_prompt(self, action: int) -> None:
        if not action == -1:
            text = self.font.render(
                f"Cannot add piece to column {action}", True, self.col
            )
        else:
            text = self.font.render("", True, self.col)
        self.queue.put((text, self.text_pos))

    def blit_text(self, screen: Screen):
        while not self.queue.empty():
            text, pos = self.queue.get()
            screen.blit_text(text.convert_alpha(), pos)

    def prompt_and_blit(self, screen: Screen, valid_inputs, color):
        self.highlight_cols(valid_inputs)
        self.prompt_player(color)
        self.blit_text(screen)
