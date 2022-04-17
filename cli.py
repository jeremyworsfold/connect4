from pathlib import Path
import yaml

from connect4.board import Board, Piece, WinState
from connect4.cli import Terminal
from connect4.players import Opponents
from connect4.configs import theme_from_file, CliConfig

def load_config() -> CliConfig:
    path = Path.cwd() / 'conf' / "cli.yaml"
    with open(path) as f:
        args = yaml.safe_load(f)
    return CliConfig(**args)


def main(cfg: CliConfig):
    b = Board()
    theme = theme_from_file(cfg.themename)
    display = Terminal(theme)
    players = Opponents(cfg.player1, cfg.player2)
    display.main(players, b)


if __name__ == "__main__":
    cfg = load_config()
    main(cfg)
