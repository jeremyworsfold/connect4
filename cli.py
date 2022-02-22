from pathlib import Path
import yaml

from connect4.board import Board, Piece, WinState
from connect4.cli import Terminal, theme_from_file, CliConfig
from connect4.players import Opponents

def load_config() -> CliConfig:
    path = Path.cwd() / 'conf' / "cli.yaml"
    with open(path) as f:
        args = yaml.safe_load(f)
    return CliConfig(**args)


def main(cfg: CliConfig):
    b = Board()
    theme = theme_from_file(cfg.themename)
    display = Terminal(theme)
    winstate = WinState(False, Piece(Piece.EMPTY))
    display.update(b)
    players = Opponents(cfg.player1, cfg.player2)
    while not winstate.is_ended:
        column = players.current.get_action(b)
        winstate = b.update(column, players.current.color)
        display.update(b)
        players.swap()
    display.end_game(b, winstate)


if __name__ == "__main__":
    cfg = load_config()
    main(cfg)
