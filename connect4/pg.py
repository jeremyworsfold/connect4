from pydantic import BaseModel, validator
from pathlib import Path

from connect4.theme import PygameTheme, pygame_theme_from_file
from connect4.screen import TextRenderer
from connect4.game import PyGame


class PyGameConfig(BaseModel):
    themename: str
    screenwidth: int
    player1: str
    player2: str

    @validator("themename")
    def theme_validation(cls, v: str) -> str:
        path = Path.cwd() / 'conf' / 'pg_themes' / f"{v}.yaml"
        print(path)
        if not path.exists():
            raise FileNotFoundError(f"{v} is not a preset theme.")
        return v

    @validator("screenwidth")
    def positive_integer(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"{v} needs to be a positive integer")
        return v