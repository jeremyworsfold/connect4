import pygame as pg
from pygame import gfxdraw
from typing import Tuple

RGBColor = Tuple[int, int, int]


def row_col(r: int, c: int, w, spacing) -> Tuple[int, int]:
    return int(w - r * spacing), int(c * spacing)


def darker(rgb: RGBColor):
    return tuple(int(0.9 * val) for val in rgb)


def draw_circle(surf, x, y, radius, color):
    gfxdraw.aacircle(surf, x, y, radius, color)
    gfxdraw.filled_circle(surf, x, y, radius, color)


def draw_token(surf, middle, radius, color):
    draw_circle(surf, middle, middle, radius, color)
    draw_circle(surf, middle, middle, int(0.75 * radius), darker(color))


class AbstractToken(pg.sprite.Sprite):
    def __init__(
        self, color: RGBColor, pos: Tuple[int, int], spacing: int, radius: int
    ) -> None:
        super().__init__()
        middle = int(spacing / 2)
        self.spacing = spacing

        self.image = pg.Surface([spacing, spacing])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        draw_token(self.image, middle, radius, color)
        self.rect = self.image.get_rect()
        self.change_pos(pos)

    def change_pos(self, pos: Tuple[int, int]):
        self.y, self.x = pos


class HoverToken(AbstractToken):
    def __init__(self, color: RGBColor, pos: Tuple[int, int], spacing: int) -> None:
        super().__init__(color, pos, spacing, int(0.4 * spacing))
        self.change_pos(pos)

    def update(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y


class Token(AbstractToken):
    def __init__(
        self, color: RGBColor, pos: Tuple[int, int], spacing: int, width: int
    ) -> None:
        super().__init__(color, pos, spacing, int(0.4 * spacing))
        self.final_y = pos[0]
        self.y = int(width - (7) * spacing)
        self.x = pos[1]

    def update(self) -> None:
        if self.y != self.final_y:
            self.y += self.spacing
        self.rect.x = self.x
        self.rect.y = self.y


class Marker(AbstractToken):
    def __init__(self, color: RGBColor, pos: Tuple[int, int], spacing: int) -> None:
        super().__init__(color, pos, spacing, int(spacing / 32))
        self.change_pos(pos)

    def update(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y


class Sprites:
    def __init__(self, unit, width, markercol, color) -> None:
        self.sprites = pg.sprite.Group()
        self.finallayer = pg.sprite.Group()
        self.unit = unit
        self.width = width

        self.marker = Marker(markercol, self._row_col(-1, -1), self.unit)
        self.add_hovertoken(color)
        self.finallayer.add(self.marker)

    def _row_col(self, r, c):
        return row_col(r, c, w=self.width, spacing=self.unit)

    def kill_hovertoken(self) -> None:
        self.hovertoken.kill()

    def add_hovertoken(self, color) -> None:
        self.hovertoken = HoverToken(
            color, self._row_col(-1, -1), self.unit
        )
        self.sprites.add(self.hovertoken)

    def move_marker(self, pos: Tuple[int, int]) -> None:
        self.marker.change_pos(self._row_col(*pos))

    def add_token(self, position: Tuple[int, int], color) -> None:
        token = Token(color, self._row_col(*position), self.unit, self.width)
        self.sprites.add(token)

    def move_hovertoken(self, pos):
        self.hovertoken.change_pos(self._row_col(6, pos // self.unit))

    def draw(self, window):
        self.sprites.update()
        self.sprites.draw(window)
        self.finallayer.update()
        self.finallayer.draw(window)
