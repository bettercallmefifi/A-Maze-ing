from typing import List, Tuple, Optional
from .cell import Cell


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: List[Cell] = [
            Cell(x, y) for y in range(height) for x in range(width)
        ]
        self.output_file = output_file
        

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y * self.width + x]
        return None

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        neighbors: List[Cell] = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor is not None:
                neighbors.append(neighbor)
        return neighbors

    def open_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        x = cell2.x - cell1.x
        y = cell2.y - cell1.y

        if x == 0 and y == -1:
            cell1.north = False
            cell2.south = False
        elif x == 0 and y == 1:
            cell1.south = False
            cell2.north = False
        elif x == 1 and y == 0:
            cell1.east = False
            cell2.west = False
        elif x == -1 and y == 0:
            cell1.west = False
            cell2.east = False
        else:
            raise ValueError("Cells are not neighbors")

    def close_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        x = cell2.x - cell1.x
        y = cell2.y - cell1.y

        if x == 0 and y == -1:
            cell1.north = True
            cell2.south = True
        elif x == 0 and y == 1:
            cell1.south = True
            cell2.north = True
        elif x == 1 and y == 0:
            cell1.east = True
            cell2.west = True
        elif x == -1 and y == 0:
            cell1.west = True
            cell2.east = True
        else:
            raise ValueError("Cells are not neighbors")

    def ascii_render(self) -> str:
        lines: List[str] = []

        top = "+"
        for x in range(self.width):
            cell = self.get_cell(x, 0)
            top += "---+" if cell and cell.north else "   +"
        lines.append(top)

        for y in range(self.height):
            middle = ""
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell is None:
                    continue

                if x == 0:
                    middle += "|" if cell.west else " "

                char = " "
                if (x, y) == self.entry:
                    char = "S"
                elif (x, y) == self.exit:
                    char = "E"
                elif cell.in_path:
                    char = "*"
                elif cell.is_42:
                    char = "X"

                middle += f" {char} "
                middle += "|" if cell.east else " "
            lines.append(middle)

            bottom = "+"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                bottom += "---+" if cell and cell.south else "   +"
            lines.append(bottom)

        return "\n".join(lines)