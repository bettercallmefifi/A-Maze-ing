from __future__ import annotations

from typing import Callable, List, Set, Tuple
import os
import shutil
import sys
import time

from mazegen.find_path import bfs_shortest_path
from mazegen.maze import Maze


class MazeRenderer:
    """Interactive terminal renderer with ANSI colors and simple controls."""

    RESET = "\033[0m"
    CLEAR = "\033[2J\033[H"

    def __init__(
        self,
        maze: Maze,
        openings: List[Tuple[Tuple[int, int], Tuple[int, int]]],
        regenerate_callback: Callable[
            [], Tuple[Maze, List[Tuple[Tuple[int, int], Tuple[int, int]]]]
        ],
    ) -> None:
        self.maze = maze
        self.openings = openings
        self.regenerate_callback = regenerate_callback

        self.wall_palette = [
            "\033[38;5;240m",
            "\033[38;5;37m",
            "\033[38;5;33m",
            "\033[38;5;160m",
        ]
        self.wall_palette_index = 0
        self.wall_color = self.wall_palette[self.wall_palette_index]

        self.path_color = "\033[38;5;208m"
        self.entry_color = "\033[38;5;40m"
        self.exit_color = "\033[38;5;196m"
        self.pattern_color = "\033[38;5;27m"
        self.text_color = "\033[38;5;250m"
        self.dim_text_color = "\033[38;5;244m"

        self.show_path = False
        self.path_set: Set[Tuple[int, int]] = set()
        self.path_animation_delay = 0.02
        self.ansi_enabled = sys.stdout.isatty()

    def _paint(self, text: str, color: str) -> str:
        if not self.ansi_enabled:
            return text
        return f"{color}{text}{self.RESET}"

    def _clear_screen(self) -> None:
        command = "cls" if os.name == "nt" else "clear"
        os.system(command)

    def _check_terminal_size(self) -> tuple[bool, str]:
        required_cols = 4 * self.maze.width + 1
        required_rows = 2 * self.maze.height + 8
        size = shutil.get_terminal_size(fallback=(80, 24))
        if size.columns < required_cols or size.lines < required_rows:
            return (
                False,
                "Terminal too small "
                f"(required {required_cols}x{required_rows}, "
                f"current {size.columns}x{size.lines})",
            )
        return True, ""

    def _refresh_path_set(self) -> None:
        self.path_set = set()
        if not self.show_path:
            return
        path = bfs_shortest_path(self.maze)
        self.path_set = set(path)

    def _animate_path_solution(self) -> None:
        path = bfs_shortest_path(self.maze)
        self.path_set = set()
        if not path:
            return

        if not self.ansi_enabled:
            self.path_set = set(path)
            return

        for point in path:
            self.path_set.add(point)
            self._draw(render_controls=False)
            time.sleep(self.path_animation_delay)

    def _cell_char(self, x: int, y: int) -> str:
        cell = self.maze.get_cell(x, y)
        if cell is None:
            return " "
        if (x, y) == self.maze.entry:
            return self._paint("◉", self.entry_color)
        if (x, y) == self.maze.exit:
            return self._paint("◎", self.exit_color)
        if (x, y) in self.path_set:
            return self._paint("•", self.path_color)
        if cell.is_42:
            return self._paint("▒", self.pattern_color)
        return " "

    def _draw_ascii(self) -> str:
        lines: List[str] = []
        wall_plus = self._paint("◆", self.wall_color)
        wall_h = self._paint("═══", self.wall_color)
        wall_v = self._paint("║", self.wall_color)

        top = []
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, 0)
            top.append(wall_plus)
            if cell and cell.north:
                top.append(wall_h)
            else:
                top.append("   ")
        top.append(wall_plus)
        lines.append("".join(top))

        for y in range(self.maze.height):
            middle: List[str] = []
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if cell is None:
                    continue
                if x == 0:
                    middle.append(wall_v if cell.west else " ")
                middle.append(f" {self._cell_char(x, y)} ")
                middle.append(wall_v if cell.east else " ")
            lines.append("".join(middle))

            bottom: List[str] = []
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                bottom.append(wall_plus)
                if cell and cell.south:
                    bottom.append(wall_h)
                else:
                    bottom.append("   ")
            bottom.append(wall_plus)
            lines.append("".join(bottom))

        return "\n".join(lines)

    def _draw(self, render_controls: bool = True) -> None:
        if self.show_path and not self.path_set:
            self._refresh_path_set()
        ok, message = self._check_terminal_size()

        self._clear_screen()
        print(self._paint("╔════════ A-Maze-ing Terminal Viewer ════════╗", self.text_color))

        if not ok:
            print(self._paint(f"ERROR: {message}", self.exit_color))
            print()
            return

        if render_controls:
            print(self._paint("║ r : regenerate maze", self.dim_text_color))
            print(self._paint("║ p : animate / toggle solution path", self.dim_text_color))
            print(self._paint("║ c : cycle wall style color", self.dim_text_color))
            print(self._paint("║ q : quit viewer", self.dim_text_color))
            print(self._paint("╚═════════════════════════════════════════════╝", self.text_color))
            print()

        print(self._draw_ascii())
        print()

    def _on_regenerate(self) -> None:
        self.maze, self.openings = self.regenerate_callback()

    def _toggle_path(self) -> None:
        self.show_path = not self.show_path
        self.path_set = set()
        if self.show_path:
            self._animate_path_solution()

    def _cycle_wall_color(self) -> None:
        self.wall_palette_index = (self.wall_palette_index + 1) % len(self.wall_palette)
        self.wall_color = self.wall_palette[self.wall_palette_index]

    def run(self) -> None:
        running = True
        while running:
            self._draw(render_controls=True)

            ok, _message = self._check_terminal_size()
            try:
                if ok:
                    command = input(
                        "Command (r/p/c/q, Enter=refresh): "
                    ).strip().lower()
                else:
                    command = input("Command (q to quit, Enter=refresh): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if command in {"q", "quit", "esc", "escape"}:
                running = False
            elif command == "r":
                self._on_regenerate()
            elif command == "p":
                self._toggle_path()
            elif command == "c":
                self._cycle_wall_color()
