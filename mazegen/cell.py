from typing import Dict


class Cell:
    """Store maze cell coordinates, wall states, and display flags."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell with all walls closed."""
        self.x = x
        self.y = y
        self.is_42 = False
        self.in_path = False
        self.visited = False
        self.walls: Dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }

    @property
    def north(self) -> bool:
        return self.walls["N"]

    @north.setter
    def north(self, value: bool) -> None:
        self.walls["N"] = value

    @property
    def east(self) -> bool:
        return self.walls["E"]

    @east.setter
    def east(self, value: bool) -> None:
        self.walls["E"] = value

    @property
    def south(self) -> bool:
        return self.walls["S"]

    @south.setter
    def south(self, value: bool) -> None:
        self.walls["S"] = value

    @property
    def west(self) -> bool:
        return self.walls["W"]

    @west.setter
    def west(self, value: bool) -> None:
        self.walls["W"] = value

    def open_wall(self, direction: str) -> None:
        """Open one wall of the cell using N/E/S/W direction aliases."""
        if direction in ["NORTH", "N"]:
            self.walls["N"] = False
        elif direction in ["EAST", "E"]:
            self.walls["E"] = False
        elif direction in ["SOUTH", "S"]:
            self.walls["S"] = False
        elif direction in ["WEST", "W"]:
            self.walls["W"] = False
        else:
            raise ValueError(f"Invalid direction {direction}")

    def close_wall(self, direction: str) -> None:
        """Close one wall of the cell using N/E/S/W direction aliases."""
        if direction in ["NORTH", "N"]:
            self.walls["N"] = True
        elif direction in ["EAST", "E"]:
            self.walls["E"] = True
        elif direction in ["SOUTH", "S"]:
            self.walls["S"] = True
        elif direction in ["WEST", "W"]:
            self.walls["W"] = True
        else:
            raise ValueError(f"Invalid direction {direction}")

    def __repr__(self) -> str:
        return f"Cell({self.x},{self.y},42={self.is_42})"