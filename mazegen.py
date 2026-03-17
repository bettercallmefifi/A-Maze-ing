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
        self.pattern_42: list[list[int]] = [
            [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
        ]
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
# ferdaous's part

    def _apply_42_pattern(self) -> None:
        """Injects the 42 pattern by marking its cells as already visited."""
        pattern_h = len(self.pattern_42)
        pattern_w = len(self.pattern_42[0])

        '''Ensure maze is large enough to hold the pattern PLUS'''
        ''' at least 1 cell of padding'''
        if self.width < pattern_w + 2 or self.height < pattern_h + 2:
            print("Error: Maze size is too small to display the '42' pattern.")
            return

        # Center the pattern in the maze
        start_x = (self.width - pattern_w) // 2
        start_y = (self.height - pattern_h) // 2

        for py in range(pattern_h):
            for px in range(pattern_w):
                # In your pattern array, '0' represents the solid walls
                if self.pattern_42[py][px] == 0:
                    maze_x = start_x + px
                    maze_y = start_y + py
                    # Pre-visit the cell so generators route around it
                    # This leaves its walls at 15 (fully closed)
                    self.visited[maze_y][maze_x] = True

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
# ferdaous's part

    def _generate_bfs(self) -> None:
        """Generate the maze using randomized Breadth-First Search."""
        # 1. Find a valid starting cell (avoiding the 42 pattern if applied)
        while True:
            x_start = random.randint(0, self.width - 1)
            y_start = random.randint(0, self.height - 1)
            if not self.visited[y_start][x_start]:
                break

        # 2. Initialize the queue with the starting cell
        queue = [(x_start, y_start)]
        self.visited[y_start][x_start] = True

        # 3. Process the queue
        while queue:
            # Pop from the front of the list (FIFO behavior)
            cx, cy = queue.pop(0)

            # Get all neighbors and shuffle them to ensure the maze is random
            neighbors = self._get_neighbors(cx, cy)
            random.shuffle(neighbors)

            for nx, ny in neighbors:
                # If the neighbor hasn't been visited (and isn't part of the 42!)
                if not self.visited[ny][nx]:
                    # Break the wall
                    self._remove_wall_between(cx, cy, nx, ny)
                    # Mark as visited
                    self.visited[ny][nx] = True
                    # Add to the queue to explore its neighbors later
                    queue.append((nx, ny))

    def generate_maze(self) -> None:
        # Reserve the 42 pattern on the grid first
        self._apply_42_pattern()

        if self.algorithm == "prim":
            self._generate_prim()
        elif self.algorithm == "dfs":
            self._generate_dfs()
        elif self.algorithm == "bfs":
            self._generate_bfs()
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
