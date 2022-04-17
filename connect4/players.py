from abc import ABC, abstractmethod
import numpy as np

from connect4.board import Piece, Board
from connect4.mcts import mcts


class Player(ABC):
    """A player is assigned a Piece to play with.
    They can choose actions given list of possible actions."""

    def __init__(self, color: Piece):
        self.color = color

    @abstractmethod
    def get_action(self, b: Board) -> int:
        """Given numpy array of possible integer actions, returns selected action"""
        pass


def create_player(name: str, p: Piece) -> Player:
    if name == "human":
        return Human(p)
    elif name == "rand":
        return Rand(p)
    elif name == "mcts":
        return MCTS(p)


class Opponents:
    """Creates arena of two players. Allows the selection of the previous and current player"""

    def __init__(self, p1: str, p2: str) -> None:
        self.p1 = create_player(p1, Piece.P1)
        self.p2 = create_player(p2, Piece.P2)

    def swap(self) -> None:
        """Swap the players so current player is the last player etc"""
        self.p1, self.p2 = self.p2, self.p1

    @property
    def current(self) -> Player:
        return self.p1

    @property
    def next(self) -> Player:
        return self.p2

    @property
    def previous(self) -> Player:
        return self.p2

    @property
    def curr_piece(self) -> Piece:
        return self.current.color

    def get_action(self, b: Board) -> int:
        return self.current.get_action(b)


class Human(Player):
    def __init__(self, color: Piece) -> None:
        super().__init__(color)

    def get_action(self, b: Board) -> int:
        """Given numpy array of possible integer actions, get user to input an action in the array"""
        valid_inputs = b.valid_inputs
        allowed = valid_inputs + 1
        while True:
            user_input = input(f"Enter a number from {allowed} to place piece. ")
            try:
                val = int(user_input)
            except ValueError:
                print("Non-integer input, please input integer or press 'q' to quit")
                if user_input == "q":
                    quit()
                continue
            if val not in allowed:
                print(f"Cannot enter piece into column {val}. Valid columns are:")
                print(allowed)
            else:
                break
        return val - 1


class MCTS(Player):
    def __init__(self, color: Piece, its=20):
        super().__init__(color)
        self.its = its

    def get_action(self, b: Board) -> int:
        """Given numpy array of possible integer actions, returns randomly selected actions"""
        action, value = mcts(b, self.color, iterations=self.its)
        print(value)
        return action


class Rand(Player):
    def __init__(self, color: Piece):
        super().__init__(color)
        self.rng = np.random.default_rng()

    def get_action(self, b: Board) -> int:
        """Given numpy array of possible integer actions, returns randomly selected actions"""
        return int(self.rng.choice(b.valid_inputs))
