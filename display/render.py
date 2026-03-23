from __future__ import annotations

from typing import Callable, List, Set, Tuple
import pygame

from mazegen.find_path import bfs_shortest_path
from mazegen.maze import Maze


class MazeRenderer:
    def __init__(
        self,
        maze: Maze,
        openings: List[Tuple[Tuple[int, int], Tuple[int, int]]],
        regenerate_callback: Callable[[], Tuple[Maze, List[Tuple[Tuple[int, int], Tuple[int, int]]]]],
    ) -> None:
        self.maze = maze
        self.openings = openings
        self.regenerate_callback = regenerate_callback

        self.wall_palette = [
            (31, 41, 55),
            (15, 118, 110),
            (37, 99, 235),
            (185, 28, 28),
        ]
        self.wall_palette_index = 0
        self.wall_color = self.wall_palette[self.wall_palette_index]

        self.path_color = (232, 93, 4)
        self.entry_color = (22, 163, 74)
        self.exit_color = (220, 38, 38)
        self.pattern_color = (30, 64, 175)
        self.background_color = (248, 250, 252)
        self.text_color = (17, 24, 39)

        self.show_path = False
        self.steps_per_frame = 4

        self.animation_open_walls: Set[Tuple[int, int, str]] = set()
        self.animation_index = 0
        self.animation_running = False
        self.use_animation_state = False

        self.cell_size = max(18, min(36, 900 // max(self.maze.width, self.maze.height)))
        self.margin = 24
        self.info_height = 70

        pygame.init()
        pygame.display.set_caption("A-Maze-ing Viewer (pygame)")
        width, height = self._maze_pixel_size()
        self.screen = pygame.display.set_mode((width, height + self.info_height))
        self.font = pygame.font.SysFont("monospace", 18)

        self._start_animation(self.openings)

    def _maze_pixel_size(self) -> tuple[int, int]:
        width = self.margin * 2 + self.maze.width * self.cell_size
        height = self.margin * 2 + self.maze.height * self.cell_size
        return width, height

    def _cell_origin(self, x: int, y: int) -> tuple[int, int]:
        return (
            self.margin + x * self.cell_size,
            self.margin + y * self.cell_size,
        )

    def _cell_center(self, x: int, y: int) -> tuple[int, int]:
        ox, oy = self._cell_origin(x, y)
        return (ox + self.cell_size // 2, oy + self.cell_size // 2)

    def _start_animation(self, openings: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.openings = openings
        self.animation_open_walls = set()
        self.animation_index = 0
        self.animation_running = bool(openings)
        self.use_animation_state = bool(openings)

    def _direction_between(
        self,
        source: Tuple[int, int],
        target: Tuple[int, int],
    ) -> Tuple[str, str]:
        (x1, y1), (x2, y2) = source, target
        if x2 == x1 + 1 and y1 == y2:
            return "E", "W"
        if x2 == x1 - 1 and y1 == y2:
            return "W", "E"
        if y2 == y1 + 1 and x1 == x2:
            return "S", "N"
        return "N", "S"

    def _advance_animation(self) -> None:
        if not self.animation_running:
            return

        end_index = min(self.animation_index + self.steps_per_frame, len(self.openings))
        for i in range(self.animation_index, end_index):
            source, target = self.openings[i]
            source_dir, target_dir = self._direction_between(source, target)
            self.animation_open_walls.add((source[0], source[1], source_dir))
            self.animation_open_walls.add((target[0], target[1], target_dir))

        self.animation_index = end_index
        if self.animation_index >= len(self.openings):
            self.animation_running = False

    def _is_wall_closed(self, cell, x: int, y: int, direction: str) -> bool:
        if self.use_animation_state:
            return (x, y, direction) not in self.animation_open_walls
        if direction == "N":
            return cell.north
        if direction == "E":
            return cell.east
        if direction == "S":
            return cell.south
        return cell.west

    def _draw(self) -> None:
        self.screen.fill(self.background_color)

        if self.show_path and not self.animation_running:
            path = bfs_shortest_path(self.maze)
            if len(path) >= 2:
                points = [self._cell_center(x, y) for x, y in path]
                pygame.draw.lines(
                    self.screen,
                    self.path_color,
                    False,

                    points,
                    max(2, self.cell_size // 5),
                )
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if cell is None:
                    continue

                ox, oy = self._cell_origin(x, y)
                x2 = ox + self.cell_size
                y2 = oy + self.cell_size

                if cell.is_42:
                    pygame.draw.rect(
                        self.screen,
                        self.pattern_color,
                        pygame.Rect(ox + 5, oy + 5, self.cell_size - 10, self.cell_size - 10),
                    )

                if self._is_wall_closed(cell, x, y, "N"):
                    pygame.draw.line(self.screen, self.wall_color, (ox, oy), (x2, oy), 2)
                if self._is_wall_closed(cell, x, y, "W"):
                    pygame.draw.line(self.screen, self.wall_color, (ox, oy), (ox, y2), 2)
                if x == self.maze.width - 1 and self._is_wall_closed(cell, x, y, "E"):
                    pygame.draw.line(self.screen, self.wall_color, (x2, oy), (x2, y2), 2)
                if y == self.maze.height - 1 and self._is_wall_closed(cell, x, y, "S"):
                    pygame.draw.line(self.screen, self.wall_color, (ox, y2), (x2, y2), 2)

        entry_x, entry_y = self.maze.entry
        ox, oy = self._cell_origin(entry_x, entry_y)
        pygame.draw.rect(
            self.screen,
            self.entry_color,
            pygame.Rect(ox + 4, oy + 4, self.cell_size - 8, self.cell_size - 8),
        )

        exit_x, exit_y = self.maze.exit
        ex, ey = self._cell_origin(exit_x, exit_y)
        pygame.draw.rect(
            self.screen,
            self.exit_color,
            pygame.Rect(ex + 4, ey + 4, self.cell_size - 8, self.cell_size - 8),
        )

        maze_width, maze_height = self._maze_pixel_size()
        info = "R: regenerate | P: show/hide path | C: wall color | Q or ESC: quit"
        status = "Path visible" if self.show_path else "Path hidden"
        info_surface = self.font.render(info, True, self.text_color)
        status_surface = self.font.render(status, True, self.text_color)
        self.screen.blit(info_surface, (self.margin, maze_height + 16))
        anim_status = "Animating" if self.animation_running else "Animation done"
        anim_surface = self.font.render(anim_status, True, self.text_color)
        self.screen.blit(status_surface, (self.margin, maze_height + 40))
        self.screen.blit(anim_surface, (self.margin + 220, maze_height + 40))

        pygame.display.flip()

    def _on_regenerate(self) -> None:
        self.maze, openings = self.regenerate_callback()
        self._start_animation(openings)

    def _toggle_path(self) -> None:
        self.show_path = not self.show_path

    def _cycle_wall_color(self) -> None:
        self.wall_palette_index = (self.wall_palette_index + 1) % len(self.wall_palette)
        self.wall_color = self.wall_palette[self.wall_palette_index]

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                    elif event.key == pygame.K_r:
                        self._on_regenerate()
                    elif event.key == pygame.K_p:
                        self._toggle_path()
                    elif event.key == pygame.K_c:
                        self._cycle_wall_color()

            self._advance_animation()
            self._draw()
            clock.tick(60)

        pygame.quit()