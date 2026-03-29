from utils.parsing import ConfigParser
from mazegen.generator import Generator
from export.export import ExportMaze
from mazegen.pattern_42 import apply_42_pattern
from mazegen.maze import Maze
import sys
import shutil
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
        algorithm=parsed_data.get("ALGORITHM", "DFS"),
    )

    generator.generate()
    maze = generator.get_maze()

    if generator.pattern_applied:
        apply_42_pattern(maze)
    else:
        print(
            "WARNING: 42 pattern cannot fit in this maze size "
            "(minimum required: 7x5)."
        )

    return maze, generator.get_openings()


def _render_ascii_with_size_check(maze: Maze) -> None:
    """Render ASCII maze only when terminal dimensions are sufficient."""
    required_cols = 4 * maze.width + 1
    required_rows = 2 * maze.height + 1
    size = shutil.get_terminal_size(fallback=(80, 24))

    if size.columns < required_cols or size.lines < required_rows:
        print(
            "ERROR: Terminal too small for ASCII maze "
            f"(required at least {required_cols}x{required_rows}, "
            f"current {size.columns}x{size.lines})."
        )
        return

    print(maze.ascii_render())


def main() -> None:
    """Parse configuration, generate maze, export output, and display it."""
    if len(sys.argv) != 2:
        print("Missing config file (usage: python3 a_maze_ing.py config.txt)")
        return

    try:
        parser = ConfigParser(sys.argv[1])
        parsed_data = parser.parse()
        configured_seed = parsed_data.get("SEED")

        maze, openings = _build_maze(parsed_data, configured_seed)

        exporter = ExportMaze(maze)
        exporter.export()

        # Try interactive visual mode first; fall back to ASCII output.
        try:
            from display.render import MazeRenderer

            def regenerate_callback() -> Tuple[
                Maze,
                List[Tuple[Tuple[int, int], Tuple[int, int]]],
            ]:
                return _build_maze(parsed_data, configured_seed)

            renderer = MazeRenderer(maze, openings, regenerate_callback)
            renderer.run()
        except Exception as e:
            print(
                "WARNING: GUI unavailable, falling back to ASCII "
                f"renderer: {e}"
            )
            _render_ascii_with_size_check(maze)

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
    try:
        main()
    except KeyboardInterrupt as e:
        print(f"{e}")
