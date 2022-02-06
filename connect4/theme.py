from pydantic import BaseModel, validator
from typing import Tuple
import yaml
from pathlib import Path
from connect4.board import Piece


def valid_rgb(tup: Tuple[int, int, int]) -> Tuple[int, int, int]:
    if any(val < 0 or val > 255 for val in tup):
        raise ValueError("Tuple must contain values in the range 0-255.")
    return tup


def theme_from_file(file):
    path = Path.cwd() / 'conf' / 'themes' / f'{file}.yaml'
    #name = f"{join('themes',file)}.yaml"
    with open(path, 'r') as f:
        configs = yaml.safe_load(f)
    return Theme(**configs)


class Theme(BaseModel):
    BOARD: Tuple[int, int, int] = (0, 0, 255)
    BACKGROUND: Tuple[int, int, int] = (255, 255, 255)
    P1: Tuple[int, int, int] = (255, 0, 0)
    P2: Tuple[int, int, int] = (255, 255, 0)
    FONT_COL: Tuple[int, int, int] = (0, 0, 0)
    FONT_FAMILY: str = "OpenSans"
    FONT_SIZE: int = 22

    _rgb_check = validator(
        "BOARD", "BACKGROUND", "P1", "P2", "FONT_COL", allow_reuse=True
    )(valid_rgb)

    @validator("FONT_FAMILY")
    def font_validation(cls, v):
        path = Path.cwd() / 'assets' / 'fonts' / f"{v}.ttf"
        if not path.exists():
        #if f"{v}.ttf" not in path.glob('*.ttf'):
            raise ValueError(f"{v} is not a recognised font by pygame.")
        return v

    def __getitem__(self, piece: Piece):
        if piece == Piece.P1:
            return self.P1
        elif piece == Piece.P2:
            return self.P2
        else:
            return self.BACKGROUND
