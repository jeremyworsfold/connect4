from abc import ABC, abstractmethod
import numpy as np
# import pygame

from connect4.board import Piece


class Player(ABC):
    def __init__(self, color: Piece):
        self.color = color

    @abstractmethod
    def get_action(self, valid_inputs: np.ndarray) -> int:
        pass


class Opponents:
    def __init__(self, p1:Player, p2: Player) -> None:
        self.p1 = p1
        self.p2 = p2

    def swap(self):
        self.p1, self.p2 = self.p2, self.p1

    @property
    def current(self):
        return self.p1

class Human(Player):
    def __init__(self, color: Piece) -> None:
        super().__init__(color)


    def get_action(self, valid_inputs: np.ndarray) -> int:
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
        return self.rng.choice(valid_inputs)