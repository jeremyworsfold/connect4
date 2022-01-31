from abc import ABC, abstractmethod
import numpy as np
# import pygame

from connect4.board import Piece


class Player(ABC):
    """A player is assigned a Piece to play with.
    They can choose actions given list of possible actions."""
    def __init__(self, color: Piece):
        self.color = color

    @abstractmethod
    def get_action(self, valid_inputs: np.ndarray) -> int:
        """Given numpy array of possible integer actions, returns selected action"""
        pass


class Opponents:
    """Creates arena of two players. Allows the selection of the previous and current player"""
    def __init__(self, p1:Player, p2: Player) -> None:
        self.p1 = p1
        self.p2 = p2

    def swap(self) -> None:
        """Swap the players so current player is the last player etc"""
        self.p1, self.p2 = self.p2, self.p1

    @property
    def current(self) -> Player:
        """Get current player"""
        return self.p1
    
    @property
    def next(self) -> Player:
        """Get next player"""
        return self.p2

    @property
    def previous(self) -> Player:
        """Get previous player"""
        return self.p2

class Human(Player):
    def __init__(self, color: Piece) -> None:
        super().__init__(color)


    def get_action(self, valid_inputs: np.ndarray) -> int:
        """Given numpy array of possible integer actions, get user to input an action in the array"""
        allowed = valid_inputs + 1
        while True:
            user_input = input(f"Enter a number from {allowed} to place piece. ")
            try: 
                val = int(user_input)
            except ValueError:
                print("Non-integer input, please input integer or press 'q' to quit")
                if user_input == 'q': quit()
                continue
            if val not in allowed:
                print(f"Cannot enter piece into column {val}. Valid columns are:")
                print(allowed)
            else:
                break
        return val-1



class Rand(Player):
    def __init__(self, color: Piece):
        super().__init__(color)
        self.rng = np.random.default_rng()

    def get_action(self, valid_inputs: np.ndarray) -> int:
        """Given numpy array of possible integer actions, returns randomly selected actions"""
        return self.rng.choice(valid_inputs)