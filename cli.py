from pathlib import Path
import yaml
from pydantic import BaseModel, validator

from connect4.board import Board, Piece, WinState
from connect4.cli import Terminal, theme_from_file
from connect4.players import Human, Rand, Opponents


class CliConfig(BaseModel):
    themename: str

    @validator("themename")
    def theme_validation(cls, v: str) -> str:
        path = Path.cwd() / 'conf' / 'cli_themes' / f"{v}.yaml"
        print(path)
        if not path.exists():
            raise FileNotFoundError(f"{v} is not a preset theme.")
        return v


def main(cfg: CliConfig):
    b = Board()
    theme = theme_from_file(cfg.themename)
    display = Terminal(theme)
    winstate = WinState(False, Piece(Piece.EMPTY))
    display.update(b)
    players = Opponents(Human(Piece(Piece.P1)), Rand(Piece(Piece.P2)))
    while not winstate.is_ended:
        column = players.current.get_action(b.valid_inputs)
        winstate = b.update(column, players.current.color)
        display.update(b)
        players.swap()
    display.end_game(b, winstate)


if __name__ == "__main__":
    path = Path.cwd() / 'conf' / "cli.yaml"
    with open(path) as f:
        args = yaml.safe_load(f)
    #theme = TerminalTheme(**args)
    cfg = CliConfig(**args)
    main(cfg)
