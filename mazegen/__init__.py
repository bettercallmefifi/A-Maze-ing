"""Reusable maze generation package.

Basic example:
    from mazegen import MazeGenerator

    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        seed=42,
        perfect=True,
        output_file="maze.txt",
    )
    generator.generate()
    maze = generator.get_maze()
"""

from .generator import Generator as MazeGenerator
from .maze import Maze
from .find_path import bfs_shortest_path

__all__ = [
    "MazeGenerator",
    "Maze",
    "bfs_shortest_path",
]
