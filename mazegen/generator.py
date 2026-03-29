from typing import List, Optional, Set, Tuple
import random
import time

from .cell import Cell
from .maze import Maze
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

        self.maze = Maze(width, height, entry, exit, output_file)
        self.perfect = perfect
        self.algorithm = algorithm.upper()
        self.openings: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        self.visited: List[List[bool]] = [
            [False for _ in range(width)] for _ in range(height)
        ]

    def generate(self) -> None:
        """Generate maze walls according to algorithm and perfectness mode."""
        self.openings = []

        for cell in self.maze.grid:
            cell.is_42 = False
            cell.visited = False

        applied = mark_42_cells(self.maze)
        if not applied:
            raise ValueError(
                "42 pattern cannot fit in this maze size "
                "(minimum required: 7x5)."
            )

        if self.maze.get_cell(*self.maze.entry) is None:
            raise ValueError("invalid coordinates for start point")

        blocked_cells: Set[Tuple[int, int]] = {
            (cell.x, cell.y) for cell in self.maze.grid if cell.is_42
        }

        if self.maze.entry in blocked_cells or self.maze.exit in blocked_cells:
            raise ValueError(
                "ENTRY and EXIT must not overlap the 42 pattern."
            )

        self.generate_maze(blocked_cells)

        if not self.perfect:
            self._add_extra_openings()

        if self._has_fully_open_3x3_zone():
            raise ValueError(
                "Maze generation produced a fully open 3x3 area, "
                "which is forbidden."
            )

    def _carve_between(self, cell1: Cell, cell2: Cell) -> None:
        """Open the wall between two adjacent cells and track the opening."""
        self.maze.open_wall_between(cell1, cell2)
        self.openings.append(((cell1.x, cell1.y), (cell2.x, cell2.y)))

    def _reset_visited(self) -> None:
        """Reset visited state used by generation algorithms."""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self.visited[y][x] = False

    def _available_cells(
        self,
        blocked_cells: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        """Return all cells that are not blocked."""
        return [
            (x, y)
            for y in range(self.maze.height)
            for x in range(self.maze.width)
            if (x, y) not in blocked_cells
        ]

    def _generate_prim(self, blocked_cells: Set[Tuple[int, int]]) -> None:
        """Generate the maze using Prim's algorithm."""
        cells = self._available_cells(blocked_cells)
        if not cells:
            return

        remaining: Set[Tuple[int, int]] = set(cells)

        while remaining:
            x_start, y_start = random.choice(list(remaining))
            self.visited[y_start][x_start] = True
            remaining.discard((x_start, y_start))

            walls: List[Tuple[int, int, int, int]] = []
            walls.extend(self.maze.get_walls_of_cell(x_start, y_start))

            while walls:
                wall = random.choice(walls)
                x1, y1, x2, y2 = wall

                if (x1, y1) in blocked_cells or (x2, y2) in blocked_cells:
                    walls.remove(wall)
                    continue

                cell1_visited = self.visited[y1][x1]
                cell2_visited = self.visited[y2][x2]

                if cell1_visited != cell2_visited:
                    self.maze.remove_wall_between_coords(x1, y1, x2, y2)
                    self.openings.append(((x1, y1), (x2, y2)))

                    if not cell1_visited:
                        self.visited[y1][x1] = True
                        remaining.discard((x1, y1))
                        walls.extend(self.maze.get_walls_of_cell(x1, y1))
                    else:
                        self.visited[y2][x2] = True
                        remaining.discard((x2, y2))
                        walls.extend(self.maze.get_walls_of_cell(x2, y2))

                walls.remove(wall)

    def _dfs_recursive(
        self,
        x: int,
        y: int,
        blocked_cells: Set[Tuple[int, int]],
    ) -> None:
        """Recursive DFS."""
        self.visited[y][x] = True
        neighbors = self.maze.get_neighbor_coords(x, y)
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if (nx, ny) in blocked_cells:
                continue
            if not self.visited[ny][nx]:
                self.maze.remove_wall_between_coords(x, y, nx, ny)
                self.openings.append(((x, y), (nx, ny)))
                self._dfs_recursive(nx, ny, blocked_cells)

    def _generate_dfs(self, blocked_cells: Set[Tuple[int, int]]) -> None:
        """Generate the maze using recursive DFS."""
        cells = self._available_cells(blocked_cells)
        if not cells:
            return

        random.shuffle(cells)
        for x_start, y_start in cells:
            if self.visited[y_start][x_start]:
                continue
            self._dfs_recursive(x_start, y_start, blocked_cells)

    def generate_maze(
        self,
        blocked_cells: Optional[Set[Tuple[int, int]]] = None,
    ) -> None:
        """Run selected algorithm (PRIM or DFS)."""
        blocked = blocked_cells or set()
        self._reset_visited()

        if self.algorithm == "PRIM":
            self._generate_prim(blocked)
        elif self.algorithm == "DFS":
            self._generate_dfs(blocked)
        else:
            raise ValueError("Unknown algorithm")

    def _cells_have_closed_wall_between(
        self,
        cell1: Cell,
        cell2: Cell,
    ) -> bool:
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

    def _cells_have_open_wall_between(
        self,
        cell1: Cell,
        cell2: Cell,
    ) -> bool:
        """Return True when two neighboring cells share an open wall."""
        return not self._cells_have_closed_wall_between(cell1, cell2)

    def _window_is_fully_open(self, start_x: int, start_y: int) -> bool:
        """Return True if a 3x3 window has no internal separating wall."""
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 2):
                left = self.maze.get_cell(x, y)
                right = self.maze.get_cell(x + 1, y)
                if left is None or right is None:
                    return False
                if not self._cells_have_open_wall_between(left, right):
                    return False

        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 3):
                top = self.maze.get_cell(x, y)
                bottom = self.maze.get_cell(x, y + 1)
                if top is None or bottom is None:
                    return False
                if not self._cells_have_open_wall_between(top, bottom):
                    return False

        return True

    def _candidate_window_starts(
        self,
        cell1: Cell,
        cell2: Cell,
    ) -> List[Tuple[int, int]]:
        """Return 3x3 window starts that include the two provided cells."""
        if self.maze.width < 3 or self.maze.height < 3:
            return []

        min_x = min(cell1.x, cell2.x)
        max_x = max(cell1.x, cell2.x)
        min_y = min(cell1.y, cell2.y)
        max_y = max(cell1.y, cell2.y)

        start_x_min = max(0, max_x - 2)
        start_x_max = min(self.maze.width - 3, min_x)
        start_y_min = max(0, max_y - 2)
        start_y_max = min(self.maze.height - 3, min_y)

        starts: List[Tuple[int, int]] = []
        for start_y in range(start_y_min, start_y_max + 1):
            for start_x in range(start_x_min, start_x_max + 1):
                starts.append((start_x, start_y))
        return starts

    def _would_create_open_3x3(self, cell1: Cell, cell2: Cell) -> bool:
        """Check whether opening a wall would create a fully open 3x3 zone."""
        starts = self._candidate_window_starts(cell1, cell2)
        if not starts:
            return False

        self.maze.open_wall_between(cell1, cell2)
        try:
            for start_x, start_y in starts:
                if self._window_is_fully_open(start_x, start_y):
                    return True
            return False
        finally:
            self.maze.close_wall_between(cell1, cell2)

    def _has_fully_open_3x3_zone(self) -> bool:
        """Return True if any fully open 3x3 area exists in the maze."""
        if self.maze.width < 3 or self.maze.height < 3:
            return False

        for y in range(self.maze.height - 2):
            for x in range(self.maze.width - 2):
                if self._window_is_fully_open(x, y):
                    return True
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
                if (neighbor.x, neighbor.y) <= (cell.x, cell.y):
                    continue
                if self._cells_have_closed_wall_between(cell, neighbor):
                    candidates.append((cell, neighbor))

        if not candidates:
            return

        random.shuffle(candidates)
        extra_count = max(1, len(candidates) // 10)
        carved = 0

        for cell1, cell2 in candidates:
            if carved >= extra_count:
                break
            if self._would_create_open_3x3(cell1, cell2):
                continue
            self._carve_between(cell1, cell2)
            carved += 1

    def get_maze(self) -> Maze:
        """Return the current maze instance."""
        return self.maze

    def get_openings(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Return wall openings carved during generation."""
        return self.openings
