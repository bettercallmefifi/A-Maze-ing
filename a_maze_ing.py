from utils.parsing import ConfigParser
from mazegen.generator import Generator
from export.export import ExportMaze
from mazegen.pattern_42 import mark_42_cells, apply_42_pattern
from mazegen.maze import Maze
import sys
from typing import Any, Dict, List, Optional, Tuple


def _build_maze(
    parsed_data: Dict[str, Any],
    seed: Optional[int],
) -> Tuple[Maze, List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    """Generate a maze and return it with the carved openings list."""
    generator = Generator(
        width=parsed_data["WIDTH"],
        height=parsed_data["HEIGHT"],
        entry=parsed_data["ENTRY"],
        exit=parsed_data["EXIT"],
        seed=seed,
        perfect=parsed_data["PERFECT"],
        output_file=parsed_data["OUTPUT_FILE"],
    )

    maze = generator.get_maze()
    mark_42_cells(maze)
    generator.generate()
    apply_42_pattern(maze)

    return maze, generator.get_openings()


def main() -> None:
    """Parse configuration, generate maze, export output, and display it."""
    if len(sys.argv) != 2:
        print("Missing config file (usage: python3 a_maze_ing.py config.txt)")
        return

    try:
        parser = ConfigParser(sys.argv[1])
        parsed_data = parser.parse()

        maze, openings = _build_maze(parsed_data, parsed_data.get("SEED"))

        exporter = ExportMaze(maze)
        exporter.export()

        # Try interactive visual mode first; fall back to ASCII output.
        try:
            from display.render import MazeRenderer

            def regenerate_callback() -> Tuple[
                Maze, List[Tuple[Tuple[int, int], Tuple[int, int]]]
            ]:
                # Regeneration ignores the fixed seed to ensure a new maze.
                return _build_maze(parsed_data, None)

            renderer = MazeRenderer(maze, openings, regenerate_callback)
            renderer.run()
        except Exception:
            print(maze.ascii_render())

    except ValueError as e:
        print(f"ERROR: Invalid configuration or maze parameters: {e}")
    except FileNotFoundError as e:
        print(f"ERROR: File not found: {e}")
    except PermissionError as e:
        print(f"ERROR: Permission denied while accessing a file: {e}")
    except ImportError as e:
        print(f"ERROR: Missing dependency or module import failure: {e}")
    except OSError as e:
        print(f"ERROR: System I/O error: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected failure: {e}")


if __name__ == "__main__":
    main()
