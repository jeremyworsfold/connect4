from typing import Dict, Any
import numpy as np
from collections import namedtuple
import math
from copy import deepcopy

from connect4.board import Grid, Piece, WinState
from connect4.score import score_by_line
import connect4.gridref as gridref


ColScore = namedtuple("ColScore", ["c", "score"])


class Node:
    # update grid, declare if winner, score func, get valid inputs - make children
    def __init__(self, grid: Grid, parent, current_player: Piece, winstate: WinState):
        self.grid = grid
        self.parent = parent
        self.current_player = current_player
        self.win_state = winstate
        self.children: Dict[int, Any] = {}

    def change_player(self):
        return Piece.RED if self.current_player == Piece.YELLOW else Piece.YELLOW

    def score(self):
        if self.win_state.is_ended:
            return ColScore(
                self.grid.last_move.c, self.get_win_state_score(self.current_player)
            )
        lsts = gridref.get_lines(self.grid.grid)
        score = score_by_line(lsts)
        return ColScore(self.grid.last_move.c, score)

    def make_children(self):
        # the children are the possible moves from the current grid. The depth is how many times this iterates.
        for col in self.grid.valid_moves():
            grid = deepcopy(self.grid)
            grid.update(self.current_player, col)
            winstate = grid.get_win_state(self.current_player)
            self.children[col] = Node(grid, self, self.change_player(), winstate)

    def get_win_state_score(self, player: Piece) -> WinState:
        state = self.grid.get_win_state(player)
        if state.winner != Piece.EMPTY:
            return PDICT[state.winner].score * math.inf
        return 0

    def print_grid(self):
        # flips grid upside down and prints grid
        print()
        for line in np.flipud(self.grid):
            print("|" + " ".join([PDICT[p].print for p in line]) + "|")


def minimax(current_node: Node, depth: int, alpha: int, beta: int, player: bool):

    if current_node.win_state.is_ended or depth == 0:
        return current_node.score()
    elif player:
        current_node.make_children()
        children = sorted(current_node.children, key=lambda x: abs(x - 3))
        max_eval = ColScore(children[0], -math.inf)
        for child in children:
            eval = minimax(current_node.children[child], depth - 1, alpha, beta, player)
            if eval.score > max_eval.score:
                max_eval = ColScore(child, eval.score)
            alpha = max(alpha, eval.score)
            if beta <= alpha:
                break
        return max_eval
    else:
        current_node.make_children()
        children = sorted(current_node.children, key=lambda x: abs(x - 3))
        min_eval = ColScore(children[0], math.inf)
        for child in children:
            eval = minimax(current_node.children[child], depth - 1, alpha, beta, True)
            if eval.score < min_eval.score:
                min_eval = ColScore(child, eval.score)
            beta = min(beta, eval.score)
            if beta <= alpha:
                break
        return min_eval
