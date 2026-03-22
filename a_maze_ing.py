from utils.parsing import ConfigParser
from mazegen.generator import Generator
from export.export import ExportMaze
from mazegen.pattern_42 import mark_42_cells, apply_42_pattern
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Missing config file (usage: python3 a_maze_ing.py config.txt)")
        return

    try:
        parser = ConfigParser(sys.argv[1])
        parsed_data = parser.parse()

        generator = Generator(
            width=parsed_data["WIDTH"],
            height=parsed_data["HEIGHT"],
            entry=parsed_data["ENTRY"],
            exit=parsed_data["EXIT"],
            seed=parsed_data.get("SEED"),
            perfect=parsed_data["PERFECT"],
            output_file=parsed_data["OUTPUT_FILE"]
        )

        maze = generator.get_maze()

        mark_42_cells(maze)

        generator.generate()

        apply_42_pattern(maze)

        print(maze.ascii_render())

        exporter = ExportMaze(maze)
        exporter.export()

    except ValueError as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()