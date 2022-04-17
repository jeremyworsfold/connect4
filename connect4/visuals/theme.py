from pydantic import BaseModel, validator
from typing import Tuple
import yaml
from pathlib import Path

from connect4.board import Piece
from connect4.visuals.tokens import RGBColor


def valid_rgb(tup: RGBColor) -> RGBColor:
    if any(val < 0 or val > 255 for val in tup):
        raise ValueError("Tuple must contain values in the range 0-255.")
    return tup


def pygame_theme_from_file(file):
    path = Path.cwd() / "conf" / "pg_themes" / f"{file}.yaml"
    with open(path, "r") as f:
        configs = yaml.safe_load(f)
    return PygameTheme(**configs)


class PygameTheme(BaseModel):
    board: RGBColor = (0, 0, 255)
    background: RGBColor = (255, 255, 255)
    P1: RGBColor = (255, 0, 0)
    P2: RGBColor = (255, 255, 0)
    f_color: RGBColor = (0, 0, 0)
    f_family: str = "OpenSans"
    f_size: int = 22

    _rgb_check = validator(
        "board", "background", "P1", "P2", "f_color", allow_reuse=True
    )(valid_rgb)

    @validator("f_family")
    def font_validation(cls, v):
        path = Path.cwd() / "assets" / "fonts" / f"{v}.ttf"
        if not path.exists():
            raise ValueError(f"{v} is not a recognised font by pygame.")
        return v

    def __getitem__(self, piece: Piece):
        if piece == Piece.P1:
            return self.P1
        elif piece == Piece.P2:
            return self.P2
        else:
            return self.background
