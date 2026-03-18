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
        algorithm: str = "dfs",
        seed: Optional[int] = None,
    ):
        """Initialize the maze generator"""
        
        # 42 pattern definition
        self.pattern_42: List[List[int]] = [
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

    def _apply_42_pattern(self) -> None:
        """Injects the 42 pattern by marking its cells as already visited"""
        pattern_h = len(self.pattern_42)
        pattern_w = len(self.pattern_42[0])

        # Ensure maze is large enough to hold the pattern PLUS at least 1 cell of padding
        if self.width < pattern_w + 2 or self.height < pattern_h + 2:
            print("Error: Maze size is too small to display the '42' pattern.")
            return

        # Center the pattern in the maze
        start_x = (self.width - pattern_w) // 2
        start_y = (self.height - pattern_h) // 2

        for py in range(pattern_h):
            for px in range(pattern_w):
                # In the pattern array, '0' represents the solid walls
                if self.pattern_42[py][px] == 0:
                    maze_x = start_x + px
                    maze_y = start_y + py
                    # Pre-visit the cell so generators route around it
                    # This leaves its walls at 15 (fully closed)
                    self.visited[maze_y][maze_x] = True

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get coordinates of all neighbors"""
        neighbors = []
        if y > 0:  # North
            neighbors.append((x, y - 1))
        if x < self.width - 1:  # East
            neighbors.append((x + 1, y))
        if y < self.height - 1:  # South
            neighbors.append((x, y + 1))
        if x > 0:  # West
            neighbors.append((x - 1, y))
        return neighbors

    def _get_walls_of_cell(
        self, x: int, y: int
    ) -> List[Tuple[int, int, int, int]]:
        """Get all walls around a cell"""
        walls = []
        neighbors = self._get_neighbors(x, y)
        for nx, ny in neighbors:
            walls.append((x, y, nx, ny))
        return walls

    def _remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Remove wall between two adjacent cells"""
        
        if y2 < y1:  # North
            self.maze[y1][x1] &= ~(1 << 0)
            self.maze[y2][x2] &= ~(1 << 2)
        elif y2 > y1:  # South
            self.maze[y1][x1] &= ~(1 << 2)
            self.maze[y2][x2] &= ~(1 << 0)
        elif x2 > x1:  # East
            self.maze[y1][x1] &= ~(1 << 1)
            self.maze[y2][x2] &= ~(1 << 3)
        elif x2 < x1:  # West
            self.maze[y1][x1] &= ~(1 << 3)
            self.maze[y2][x2] &= ~(1 << 1)

    def _generate_prim(self) -> None:
        """Generate the maze using Prim's algorithm"""
        # Find a valid starting cell (avoiding the 42 pattern)
        while True:
            x_start = random.randint(0, self.width - 1)
            y_start = random.randint(0, self.height - 1)
            if not self.visited[y_start][x_start]:
                break
        
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
        """Generate the maze using DFS (Recursive Backtracker)"""
        # Find a valid starting cell (avoiding the 42 pattern)
        while True:
            x_start = random.randint(0, self.width - 1)
            y_start = random.randint(0, self.height - 1)
            if not self.visited[y_start][x_start]:
                break
        
        self._dfs_recursive(x_start, y_start)

    def _dfs_recursive(self, x: int, y: int) -> None:
        """Recursive DFS"""
        self.visited[y][x] = True
        neighbors = self._get_neighbors(x, y)
        random.shuffle(neighbors)
        
        for nx, ny in neighbors:
            if not self.visited[ny][nx]:
                self._remove_wall_between(x, y, nx, ny)
                self._dfs_recursive(nx, ny)

    def _generate_bfs(self) -> None:
        """Generate the maze using randomized Breadth-First Search"""
        # Find a valid starting cell (avoiding the 42 pattern)
        while True:
            x_start = random.randint(0, self.width - 1)
            y_start = random.randint(0, self.height - 1)
            if not self.visited[y_start][x_start]:
                break

        # Initialize the queue with the starting cell
        queue = [(x_start, y_start)]
        self.visited[y_start][x_start] = True

        # Process the queue
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
        """Generate the maze using the selected algorithm"""
        # Reserve the 42 pattern on the grid first
        self._apply_42_pattern()

        if self.algorithm == "prim":
            self._generate_prim()
        elif self.algorithm == "dfs":
            self._generate_dfs()
        elif self.algorithm == "bfs":
            self._generate_bfs()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def get_maze(self) -> List[List[int]]:
        """Return the maze structure as a 2D grid with hex-encoded walls"""
        return self.maze

    def get_shortest_path(self) -> str:
        """Finds the shortest path from entry to exit using BFS."""
        from collections import deque
        
        # Queue stores tuples of (x, y, path_string)
        queue = deque([(self.entry[0], self.entry[1], "")])
        visited = set()
        visited.add(self.entry)
        
        while queue:
            x, y, path = queue.popleft()
            
            if (x, y) == self.exit:
                return path
            
            cell_walls = self.maze[y][x]
            
            # Check North (bit 0 is 0)
            if not (cell_walls & (1 << 0)) and y > 0 and (x, y - 1) not in visited:
                visited.add((x, y - 1))
                queue.append((x, y - 1, path + "N"))
            # Check East (bit 1 is 0)
            if not (cell_walls & (1 << 1)) and x < self.width - 1 and (x + 1, y) not in visited:
                visited.add((x + 1, y))
                queue.append((x + 1, y, path + "E"))
            # Check South (bit 2 is 0)
            if not (cell_walls & (1 << 2)) and y < self.height - 1 and (x, y + 1) not in visited:
                visited.add((x, y + 1))
                queue.append((x, y + 1, path + "S"))
            # Check West (bit 3 is 0)
            if not (cell_walls & (1 << 3)) and x > 0 and (x - 1, y) not in visited:
                visited.add((x - 1, y))
                queue.append((x - 1, y, path + "W"))
                
        return "No path found"


    def display_maze(self, path: bool = False) -> None:
        """Display the maze in terminal using ASCII"""
        
        for y in range(self.height):
            # Print top walls
            line = ""
            for x in range(self.width):
                line += "+"
                if self.maze[y][x] & (1 << 0):  # North wall
                    line += "---"
                else:
                    line += "   "
            line += "+"
            print(line)
            
            # Print cell content
            line = ""
            for x in range(self.width):
                if self.maze[y][x] & (1 << 3):  # West wall
                    line += "|"
                else:
                    line += " "
                
                if (x, y) == self.entry:
                    line += " E "
                elif (x, y) == self.exit:
                    line += " X "
                else:
                    line += "   "
            
            line += "|"
            print(line)
        
        # Print bottom border
        line = ""
        for x in range(self.width):
            line += "+"
            line += "---"
        line += "+"
        print(line)

    def write_output_file(self, filename: str) -> None:
        """Write maze to output file in required format"""
        
        with open(filename, 'w') as f:
            # Write maze grid in hex
            for row in self.maze:
                hex_row = ''.join(format(cell, 'X') for cell in row)
                f.write(hex_row + '\n')
            
            # Write empty line
            f.write('\n')
            
            # Write entry coordinates
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            
            # Write exit coordinates
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            
            # SUBJECT REQUIREMENT: Write the shortest path solution
            path = self.get_shortest_path()
            f.write(f"{path}\n")

            
            