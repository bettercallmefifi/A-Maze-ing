from typing import Tuple, Optional
import random
import time

from .maze import Maze
from .cell import Cell


class Generator:
    def __init__(
        self,
        width: int,
        height: int,
        exit: Tuple[int, int],
        entry: Tuple[int, int],
        seed: Optional[int],
        perfect: bool,
        output_file,
    ) -> None:
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(time.time_ns())

        self.maze = Maze(width, height, entry, exit,output_file)
        self.perfect = perfect

    def generate(self) -> None:
        start_point = self.maze.get_cell(*self.maze.entry)
        if start_point is None:
            raise ValueError("invalid coordinates for start point")

        self._dfs(start_point)

    def _dfs(self, cell: Cell) -> None:
        cell.visited = True

        neighbors = self.maze.get_neighbors(cell)
        random.shuffle(neighbors)

        for neighbor in neighbors:
            if not neighbor.visited:
                self.maze.open_wall_between(cell, neighbor)
                self._dfs(neighbor)

    def get_maze(self) -> Maze:
        return self.maze