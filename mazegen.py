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

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get coordinates of all neighbors (not walls!)"""
        neighbors = []
        if y > 0:  # North
            neighbors.append((x, y-1))
        if x < self.width - 1:  # East
            neighbors.append((x+1, y))
        if y < self.height - 1:  # South
            neighbors.append((x, y+1))
        if x > 0:  # West
            neighbors.append((x-1, y))
        return neighbors

    def _get_walls_of_cell(
        self, x: int, y: int
            ) -> List[Tuple[int, int, int, int]]:
        walls = []
        neighbors = self._get_neighbors(x, y)
        for nx, ny in neighbors:
            walls.append((x, y, nx, ny))
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
            self.maze[y1][x1] -= 2
            self.maze[y2][x2] -= 8

    def _generate_prim(self):
        """Generate the maze using Prim's algorithm"""
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

    def _generate_dfs(self) -> None:
        x_start = random.randint(0, self.width - 1)
        y_start = random.randint(0, self.height - 1)
        self._dfs_recursive(x_start, y_start)

    def _dfs_recursive(self, x: int, y: int) -> None:
        """Recusrive DFS"""
        self.visited[y][x] = True
        neighbors = self._get_neighbors(x, y)
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if not self.visited[ny][nx]:
                self._remove_wall_between(x, y, nx, ny)
                self._dfs_recursive(nx, ny)

    def generate_maze(self) -> None:
        if self.algorithm == "prim":
            self._generate_prim()
        elif self.algorithm == "dfs":
            self._generate_dfs()
        else:
            raise ValueError("Unknown algorithm")

    def get_maze(self) -> List[List[int]]:
        """
        Return the maze structure as a 2D grid with hex-encoded walls
        """
        return self.maze

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