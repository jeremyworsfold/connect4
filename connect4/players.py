from abc import ABC, abstractmethod
import random
import numpy as np
# import pygame

from connect4.board import Piece


class Player(ABC):
    def __init__(self, color: Piece):
        self.color = color

    @abstractmethod
    def get_action(self, board):
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
    def __init__(self, color: Piece):
        super().__init__(color)


    def get_action(self, board):
        while True:
            valid_inputs = board.valid_inputs
            user_input = input(f"Enter a number from {valid_inputs} to place piece. ")
            try: 
                val = int(user_input)
            except ValueError:
                print("Non-integer input, please input integer or press 'q' to quit")
                if user_input == 'q': quit()
                continue
            if val not in valid_inputs:
                print(f"Cannot enter piece into column {val}. Valid columns are:")
                print(valid_inputs)
            else:
                break
        return val-1



class Rand(Player):
    def __init__(self, color: Piece):
        super().__init__(color)

    def get_action(self, board):
        return random.choice(np.flatnonzero(board.valid_moves))