from typing import List, Tuple, Optional
from .cell import Cell


class Maze:
    """Represent maze cells, topology helpers, and ASCII rendering."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str
    ) -> None:
        """Initialize maze dimensions, endpoints, and cell grid."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: List[Cell] = [
            Cell(x, y) for y in range(height) for x in range(width)
        ]
        self.output_file = output_file

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Return the cell at coordinates when inside bounds, else None."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y * self.width + x]
        return None

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Return cardinal neighbors for a given cell."""
        neighbors: List[Cell] = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor is not None:
                neighbors.append(neighbor)
        return neighbors

    def get_neighbor_coords(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Return neighboring cell coordinates in N, E, S, W order."""
        neighbors: List[Tuple[int, int]] = []

        if y > 0:
            neighbors.append((x, y - 1))
        if x < self.width - 1:
            neighbors.append((x + 1, y))
        if y < self.height - 1:
            neighbors.append((x, y + 1))
        if x > 0:
            neighbors.append((x - 1, y))

        return neighbors

    def get_walls_of_cell(
        self, x: int, y: int
    ) -> List[Tuple[int, int, int, int]]:
        """Return wall candidates as edges from one cell to each neighbor."""
        walls: List[Tuple[int, int, int, int]] = []
        for nx, ny in self.get_neighbor_coords(x, y):
            walls.append((x, y, nx, ny))
        return walls

    def remove_wall_between_coords(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        """Open wall between two adjacent cells addressed by coordinates."""
        cell1 = self.get_cell(x1, y1)
        cell2 = self.get_cell(x2, y2)

        if cell1 is None or cell2 is None:
            raise ValueError("Invalid coordinates for wall removal")

        self.open_wall_between(cell1, cell2)

<<<<<<< HEAD
    def generate_with_prim(
        self,
        start: Tuple[int, int],
        blocked: Optional[Set[Tuple[int, int]]] = None,
    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Generate a maze using Prim's"""
        """algorithm and return carved openings."""
        blocked_cells = blocked or set()
        sx, sy = start

        if (sx, sy) in blocked_cells:
            return []

        visited: Set[Tuple[int, int]] = {(sx, sy)}
        walls = self.get_walls_of_cell(sx, sy)
        openings: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        while walls:
            x1, y1, x2, y2 = random.choice(walls)
            walls.remove((x1, y1, x2, y2))

            c1 = (x1, y1)
            c2 = (x2, y2)

            if c1 in blocked_cells or c2 in blocked_cells:
                continue

            c1_visited = c1 in visited
            c2_visited = c2 in visited

            if c1_visited == c2_visited:
                continue

            self.remove_wall_between_coords(x1, y1, x2, y2)
            openings.append((c1, c2))

            if not c1_visited:
                visited.add(c1)
                walls.extend(self.get_walls_of_cell(x1, y1))
            else:
                visited.add(c2)
                walls.extend(self.get_walls_of_cell(x2, y2))

        return openings

    def generate_with_dfs(
        self,
        start: Tuple[int, int],
        blocked: Optional[Set[Tuple[int, int]]] = None,
    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Generate a maze using recursive DFS and return carved openings."""
        blocked_cells = blocked or set()
        visited: Set[Tuple[int, int]] = set()
        openings: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        def dfs(x: int, y: int) -> None:
            current = (x, y)
            visited.add(current)

            neighbors = self.get_neighbor_coords(x, y)
            random.shuffle(neighbors)

            for nx, ny in neighbors:
                target = (nx, ny)
                if target in blocked_cells or target in visited:
                    continue

                self.remove_wall_between_coords(x, y, nx, ny)
                openings.append((current, target))
                dfs(nx, ny)

        if start in blocked_cells:
            return openings

        dfs(start[0], start[1])
        return openings

    def open_wall_between(
        self, cell1: Cell, cell2: Cell
    ) -> None:
=======
    def open_wall_between(self, cell1: Cell, cell2: Cell) -> None:
>>>>>>> 4ee574e (fixe all)
        """Open the wall shared by two adjacent cells."""
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
        """Close the wall shared by two adjacent cells."""
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
        """Return a text representation of the maze with markers."""
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
