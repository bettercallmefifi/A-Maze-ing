from mazegen.maze import Maze
from mazegen.generator import Generator


def main() -> None:
    maze = Maze(10, 10, (0, 0), (0, 5), "maze.txt")
    gen = Generator(10, 10, (0, 0), (0, 5), None, True, "maze.txt")
    gen.generate()
    maze = gen.get_maze()

    print(maze.ascii_render())


main()
