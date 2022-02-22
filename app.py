from pathlib import Path
import yaml

from connect4.pg import PyGame, pygame_theme_from_file, PyGameConfig
from connect4.players import Opponents


def load_config():
    path = Path.cwd() / 'conf' / "pygame.yaml"
    with open(path) as f:
        args = yaml.safe_load(f)
    return PyGameConfig(**args)


def main(cfg: PyGameConfig):
    theme = pygame_theme_from_file(cfg.themename)
    players = Opponents(cfg.player1, cfg.player2)
    game = PyGame(players, theme)
    #game.run(b)
    game.main()


if __name__ == "__main__":
    cfg = load_config()
    main(cfg)
