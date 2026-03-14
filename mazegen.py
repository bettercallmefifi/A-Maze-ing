from typing import List, Tuple, Optional
import random


class MazeGenerator:
    def __init__(
            self, width: int, height: int, entry: Tuple[int,int],
            exit: Tuple[int,int], perfect: bool=True,
            seed: Optional[int]=None):
        """
        Initialize the maze generator
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self.maze = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def get_walls_of_cell(self, x: int, y: int) -> List[Tuple[int, int, int, int]]:
        walls = []
        #north
        if y > 0:
            walls.append((x, y, x, y-1))
        #East
        if x < self.width - 1:
            walls.append((x, y, x+1, y))
        #West
        if x > 0:
            walls.append((x, y, x-1, y))    
        #South
        if y < self.height - 1:
            walls.append((x, y, x, y+1))
        return walls

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Remove wall between two adjacent cells"""
        #neighbor is norh
        if x1 == x2 and y1 - 1 == y2:
            self.maze[y1][x1] -= 1
            self.maze[y2][x2] -= 4
        #neighbor is south
        elif x1 == x2 and y2 == y1 + 1:
            self.maze[y1][x1] -= 4
            self.maze[y2][x2] -= 1
        #neighbor is west
        elif x1 - 1 == x2 and y1 == y2:
            self.maze[y1][x1] -= 8
            self.maze[y2][x2] -= 2
        #neighbor is east
        elif x1 + 1 == x2 and y1 == y2:
            self.maze[y1][x1] -= 8
            self.maze[y2][x2] -= 2


    def generate_maze(self) -> None:
        """
        Generate the maze using Prim's algorithm
        """
        for y in range(self.height):
            for x in range(self.width):
                self.visited[y][x] = False
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.visited[y][x] = True

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

    def display_maze(self, path: bool=False) -> None:
        """
        Optional terminal display of maze
        """
        pass