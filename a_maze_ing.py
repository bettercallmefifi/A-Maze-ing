import sys
from typing import Optional

"""
This module defines the Maze model for the A_maze_ing game.

It is responsible for generating, storing, and managing the state
and properties of a maze, including its cells, walls, start, and end points.
"""


class MazeModel:
    """
    Manages the maze's structure, generation, and state.
    """

    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width: int = width
        self.height: int = height
        self.seed: int = seed

    @staticmethod
    def _parse_int(value: str, name: str, min_value: Optional[int]) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid integer for {name}: '{value}'."
            ) from exc
        if min_value is not None and parsed < min_value:
            raise ValueError(
                f"{name} must be >= {min_value}, got {parsed}."
            )
        return parsed

    @staticmethod
    def _parse_bool(value: str, name: str) -> bool:
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y"}:
            return True
        if normalized in {"false", "0", "no", "n"}:
            return False
        raise ValueError(
            f"Invalid boolean for {name}: '{value}'."
        )

    @staticmethod
    def _parse_pair(value: str, name: str) -> tuple[int, int]:
        parts = [part.strip() for part in value.split(",")]
        if len(parts) != 2:
            raise ValueError(
                f"{name} must be formatted as 'x,y', got '{value}'."
            )
        x = MazeModel._parse_int(parts[0], f"{name}.x", 0)
        y = MazeModel._parse_int(parts[1], f"{name}.y", 0)
        return (x, y)

    @staticmethod
    def parse_from_file(file_path: str) -> dict:
        """
        Parses a maze configuration from a specified file.
        """
        if not file_path:
            raise ValueError("Config path is required.")

        try:
            with open(file_path, "r", encoding="utf-8") as config_file:
                lines = config_file.readlines()
        except OSError as exc:
            raise OSError(
                f"Could not read config file: {exc}"
            ) from exc

        raw_values: dict[str, str] = {}
        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(
                    f"Line {line_number}: missing '=' separator."
                )
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if not key:
                raise ValueError(f"Line {line_number}: empty key.")
            if not value:
                raise ValueError(
                    f"Line {line_number}: empty value for '{key}'."
                )
            raw_values[key] = value

        required = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]
        missing = [key for key in required if key not in raw_values]
        if missing:
            raise ValueError(
                f"Missing required keys: {', '.join(missing)}."
            )

        width = MazeModel._parse_int(raw_values["WIDTH"], "WIDTH", 1)
        height = MazeModel._parse_int(raw_values["HEIGHT"], "HEIGHT", 1)
        entry = MazeModel._parse_pair(raw_values["ENTRY"], "ENTRY")
        exit_point = MazeModel._parse_pair(raw_values["EXIT"], "EXIT")

        output_file = raw_values["OUTPUT_FILE"].strip()
        if not output_file:
            raise ValueError("OUTPUT_FILE must not be empty.")

        perfect = MazeModel._parse_bool(raw_values["PERFECT"], "PERFECT")

        if entry == exit_point:
            raise ValueError("ENTRY and EXIT must be different.")

        # Check if entry and exit are within bounds
        for name, (x, y) in [("ENTRY", entry), ("EXIT", exit_point)]:
            if x < 0 or x >= width or y < 0 or y >= height:
                raise ValueError(
                    f"{name} must be inside the maze bounds."
                )

        seed: Optional[int] = None
        if "SEED" in raw_values:
            seed = MazeModel._parse_int(raw_values["SEED"], "SEED", 0)

        algorithm = raw_values.get("ALGORITHM", "dfs").strip().lower()
        # Added 'bfs' to support your new generation algorithm
        if algorithm not in {"dfs", "prim", "bfs"}:
            raise ValueError(
                "ALGORITHM must be 'dfs', 'prim', or 'bfs'."
            )

        return {
            "width": width,
            "height": height,
            "seed": seed,
            "algorithm": algorithm,
            "perfect": perfect,
            "entry": entry,
            "exit": exit_point,
            "output_file": output_file,
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        config = MazeModel.parse_from_file(config_file)  # ← Changed this
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Import MazeGenerator
    from mazegen import MazeGenerator
    
    # Create maze generator
    maze_gen = MazeGenerator(
        width=config["width"],      # ← Note: lowercase keys
        height=config["height"],
        entry=config["entry"],
        exit=config["exit"],
        perfect=config["perfect"],
        algorithm=config["algorithm"],
        seed=config["seed"],
    )
    
    # Generate maze
    print("Generating maze...")
    maze_gen.generate_maze()
    
    # Display maze
    print("\nMaze:")
    maze_gen.display_maze()
    
    # Write output file
    output_file = config["output_file"]
    maze_gen.write_output_file(output_file)
    print(f"\nMaze saved to {output_file}")