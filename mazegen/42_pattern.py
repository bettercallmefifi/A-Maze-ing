from typing import Deque, Set, Tuple

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


def mark_42_cells(maze):
    """Mark 42 cells BEFORE generation so DFS avoids them."""
    
    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    start_x = (maze.width - pattern_w) // 2
    start_y = (maze.height - pattern_h) // 2

    for py in range(pattern_h):
        for px in range(pattern_w):
            if PATTERN_42[py][px] == 1:
                cx = start_x + px
                cy = start_y + py
                cell = maze.get_cell(cx, cy)
                if cell is not None:
                    cell.is_42 = True
                    cell.visited = True


def apply_42_pattern(maze):
    """Apply the 42 pattern by closing walls around marked cells."""
    if not can_apply_42_pattern(maze):
        return
    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    start_x = (maze.width - pattern_w) // 2
    start_y = (maze.height - pattern_h) // 2

    for py in range(pattern_h):
        for px in range(pattern_w):
            if PATTERN_42[py][px] == 1:
                cx = start_x + px
                cy = start_y + py

                cell = maze.get_cell(cx, cy)
                if cell is not None:
                    cell.is_42 = True

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if cell is None or not cell.is_42:
                continue
            for neighbor in maze.neighbors(cell):
                maze.close_wall_between(cell, neighbor)