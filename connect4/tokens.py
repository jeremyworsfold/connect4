import pygame as pg
from pygame import gfxdraw
from typing import Tuple

RGBColor = Tuple[int, int, int]


def darker(rgb: RGBColor):
    return tuple(int(0.9*val) for val in rgb)


def draw_circle(surf, x, y, radius, color):
    gfxdraw.aacircle(surf, x, y, radius, color)
    gfxdraw.filled_circle(surf, x, y, radius, color)


def draw_token(surf, middle, radius, color):
    draw_circle(surf, middle, middle, radius, color)
    draw_circle(surf, middle, middle, int(0.75*radius), darker(color))


class AbstractToken(pg.sprite.Sprite):
    def __init__(self, color: RGBColor, pos: Tuple[int, int], spacing: int, radius: int) -> None:
        super().__init__()
        middle = int(spacing/2)
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
        super().__init__(color, pos, spacing, int(0.4*spacing))
        self.change_pos(pos)

    def update(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y


class Token(AbstractToken):
    def __init__(self, color: RGBColor, pos: Tuple[int, int], spacing: int, width: int) -> None:
        super().__init__(color, pos, spacing, int(0.4*spacing))
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
        super().__init__(color, pos, spacing, int(spacing/32))
        self.change_pos(pos)

    def update(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y