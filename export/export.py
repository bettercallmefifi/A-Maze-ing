from mazegen.maze import Maze
from mazegen.find_path import bfs_shortest_path
from typing import List, Sequence, Tuple
class ExportMaze:
    def __init__(self,maze:Maze):
        self.maze = maze
    def path_to_directions(self,path) -> str:
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
    
    def export(self)->None:
        path = bfs_shortest_path(self.maze)
        directions = self.path_to_directions(path)
        with open(self.maze.output_file,"w") as file:
            for y in range(self.maze.width):
                for x in range(self.maze.height):
                    cell = self.maze.get_cell(x,y)
                    result =0

                    if cell:
                        if cell.north:
                            result |= 1 << 0
                        if cell.east:
                            result|=1 << 1
                        if cell.south:
                            result|= 1 << 2
                        if cell.west:
                            result|=1 << 3
                        file.write(format(result,"X"))
                file.write("\n")
                
            file.write("\n")
            file.write(f"{self.maze.entry[0]},{self.maze.entry[1]}\n")
            file.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
            file.write(directions)