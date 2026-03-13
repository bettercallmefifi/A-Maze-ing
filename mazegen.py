from typing import List, Tuple, Optional
import random


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        algorithm="dfs",
        seed: Optional[int] = None,
    ):
        """
        Initialize the maze generator
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.algorithm = algorithm
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self.maze = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def _get_walls_of_cell(self, x: int, y: int) -> List[Tuple[int, int, int, int]]:
        walls = []
        # north
        if y > 0:
            walls.append((x, y, x, y - 1))
        # East
        if x < self.width - 1:
            walls.append((x, y, x + 1, y))
        # West
        if x > 0:
            walls.append((x, y, x - 1, y))
        # South
        if y < self.height - 1:
            walls.append((x, y, x, y + 1))
        return walls

    def _remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Remove wall between two adjacent cells"""
        # neighbor is norh
        if x1 == x2 and y1 - 1 == y2:
            self.maze[y1][x1] -= 1
            self.maze[y2][x2] -= 4
        # neighbor is south
        elif x1 == x2 and y2 == y1 + 1:
            self.maze[y1][x1] -= 4
            self.maze[y2][x2] -= 1
        # neighbor is west
        elif x1 - 1 == x2 and y1 == y2:
            self.maze[y1][x1] -= 8
            self.maze[y2][x2] -= 2
        # neighbor is east
        elif x1 + 1 == x2 and y1 == y2:
            self.maze[y1][x1] -= 8
            self.maze[y2][x2] -= 2

    def _generate_prim(self):
        """Generate the maze using Prim's algorithm"""
        for y in range(self.height):
            for x in range(self.width):
                self.visited[y][x] = False
        x_start = random.randint(0, self.width - 1)
        y_start = random.randint(0, self.height - 1)
        self.visited[y_start][x_start] = True
        walls = []
        initial_walls = self._get_walls_of_cell(x_start, y_start)
        walls.extend(initial_walls)
        while walls:
            wall = random.choice(walls)
            x1, y1, x2, y2 = wall
            cell1_visited = self.visited[y1][x1]
            cell2_visited = self.visited[y2][x2]
            if cell1_visited != cell2_visited:
                self._remove_wall_between(x1, y1, x2, y2)
                if not cell1_visited:
                    self.visited[y1][x1] = True
                    new_walls = self._get_walls_of_cell(x1, y1)
                    walls.extend(new_walls)
                else:
                    self.visited[y2][x2] = True
                    new_walls = self._get_walls_of_cell(x2, y2)
                    walls.extend(new_walls)
            walls.remove(wall)

    def _generate_dfs(self):
        pass

    def generate_maze(self) -> None:
        if self.algorithm == "prim":
            self._generate_prim()
        elif self.algorithm == "dfs":
            self._generate_dfs
        else:
            raise ValueError("Unknown algorithm")

    def get_maze(self) -> List[List[int]]:
        """
        Return the maze structure as a 2D grid with hex-encoded walls
        """
        pass

    def get_solution_path(self) -> str:
        """
        Return shortest path from entry to exit as string of N, E, S, W
        """
        pass

    def display_maze(self, path: bool = False) -> None:
        """
        Optional terminal display of maze
        """
        pass
