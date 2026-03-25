from mazegen.maze import Maze
from mazegen.find_path import bfs_shortest_path
from typing import List, Tuple
from pathlib import Path

Coord = Tuple[int, int]


class ExportMaze:
    """Serialize maze data to the required hexadecimal output format."""

    def __init__(self, maze: Maze) -> None:
        """Initialize exporter with a generated maze."""
        self.maze = maze

    def path_to_directions(self, path: List[Coord]) -> str:
        """Convert a path into N/E/S/W direction letters."""
        directions: List[str] = []

        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            if x2 == x1 + 1:
                directions.append("E")
            elif x2 == x1 - 1:
                directions.append("W")
            elif y2 == y1 + 1:
                directions.append("S")
            elif y2 == y1 - 1:
                directions.append("N")

        return "".join(directions)

    def export(self) -> None:
        """Write maze hex grid, entry, exit, and shortest-path directions."""
        path = bfs_shortest_path(self.maze)

        if not path or len(path) < 2:
            directions = ""
        else:
            directions = self.path_to_directions(path)

        output_path = Path(self.maze.output_file)
        if output_path.parent and not output_path.parent.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w") as file:
            for y in range(self.maze.height):
                for x in range(self.maze.width):

                    cell = self.maze.get_cell(x, y)
                    result = 0

                    if cell:
                        if cell.north:
                            result |= 1 << 0
                        if cell.east:
                            result |= 1 << 1
                        if cell.south:
                            result |= 1 << 2
                        if cell.west:
                            result |= 1 << 3

                    file.write(format(result, "X"))

                file.write("\n")

            file.write("\n")
            file.write(f"{self.maze.entry[0]},{self.maze.entry[1]}\n")
            file.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
            file.write(f"{directions}\n")
