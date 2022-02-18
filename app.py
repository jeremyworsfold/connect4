from pydantic import BaseModel, validator
from pathlib import Path
import yaml

from connect4 import Board, Piece
from connect4.pg import PyGame, ScreenHandler, pygame_theme_from_file
from connect4.players import Human, Rand, Opponents


class PyGameConfig(BaseModel):
    themename: str
    screenwidth: int

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


def main(cfg: PyGameConfig):
    theme = pygame_theme_from_file(cfg.themename)
    b = Board()
    players = Opponents(Human(Piece(Piece.P1)), Rand(Piece(Piece.P2)))
    screenhandler = ScreenHandler(theme, cfg.screenwidth)
    game = PyGame(players, screenhandler)
    game.run(b)


if __name__ == "__main__":
    path = Path.cwd() / 'conf' / "pygame.yaml"
    with open(path) as f:
        args = yaml.safe_load(f)
    cfg = PyGameConfig(**args)
    main(cfg)
