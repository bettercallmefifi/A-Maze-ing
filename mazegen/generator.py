from typing import List, Tuple, Optional, Set
import random
import time

from .maze import Maze
from .cell import Cell
from .pattern_42 import mark_42_cells


class Generator:
    """Generate maze structures using DFS or Prim algorithms."""

    def __init__(
        self,
        width: int,
        height: int,
        exit: Tuple[int, int],
        entry: Tuple[int, int],
        seed: Optional[int],
        perfect: bool,
        output_file: str,
        algorithm: str = "DFS",
    ) -> None:
        """Initialize generation settings and random seed."""
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(time.time_ns())

        self.maze = Maze(width, height, entry, exit,output_file)
        self.perfect = perfect
        self.algorithm = algorithm.upper()
        self.openings: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    def generate(self) -> None:
        """Generate maze walls according to algorithm and perfectness mode."""
        self.openings = []

        for cell in self.maze.grid:
            cell.is_42 = False
            cell.visited = False

        applied = mark_42_cells(self.maze)
        if not applied:
            print("ERROR: 42 pattern omitted (maze too small or overlaps entry/exit).")

        if self.maze.get_cell(*self.maze.entry) is None:
            raise ValueError("invalid coordinates for start point")

        blocked_cells: Set[Tuple[int, int]] = {
            (cell.x, cell.y)
            for cell in self.maze.grid
            if cell.is_42
        }

        if self.algorithm == "PRIM":
            self.openings = self.maze.generate_with_prim(self.maze.entry, blocked_cells)
        else:
            self.openings = self.maze.generate_with_dfs(self.maze.entry, blocked_cells)

        if not self.perfect:
            self._add_extra_openings()

    def _carve_between(self, cell1: Cell, cell2: Cell) -> None:
        """Open the wall between two adjacent cells and track the opening."""
        self.maze.open_wall_between(cell1, cell2)
        self.openings.append(((cell1.x, cell1.y), (cell2.x, cell2.y)))

    def _cells_have_closed_wall_between(self, cell1: Cell, cell2: Cell) -> bool:
        """Return True when two neighboring cells share a closed wall."""
        x = cell2.x - cell1.x
        y = cell2.y - cell1.y

        if x == 0 and y == -1:
            return cell1.north and cell2.south
        if x == 0 and y == 1:
            return cell1.south and cell2.north
        if x == 1 and y == 0:
            return cell1.east and cell2.west
        if x == -1 and y == 0:
            return cell1.west and cell2.east
        return False

    def _add_extra_openings(self) -> None:
        """Add random openings to introduce cycles when PERFECT=False."""
        candidates: List[Tuple[Cell, Cell]] = []

        for cell in self.maze.grid:
            if cell.is_42:
                continue

            for neighbor in self.maze.get_neighbors(cell):
                if neighbor.is_42:
                    continue
                # Keep one orientation only to avoid duplicate candidate pairs.
                if (neighbor.x, neighbor.y) <= (cell.x, cell.y):
                    continue
                if self._cells_have_closed_wall_between(cell, neighbor):
                    candidates.append((cell, neighbor))

        if not candidates:
            return

        random.shuffle(candidates)
        extra_count = max(1, len(candidates) // 10)

        for cell1, cell2 in candidates[:extra_count]:
            self._carve_between(cell1, cell2)

    def get_maze(self) -> Maze:
        """Return the current maze instance."""
        return self.maze

    def get_openings(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Return wall openings carved during generation."""
        return self.openings