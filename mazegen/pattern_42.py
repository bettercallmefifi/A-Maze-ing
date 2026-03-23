from .maze import Maze

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


def mark_42_cells(maze: Maze) -> bool:
    """Mark 42 pattern cells and return True when applied."""
    if not can_apply_42_pattern(maze):
        return False

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
    return True

def can_apply_42_pattern(maze: Maze) -> bool:
    """Check if maze is big enough."""
    return maze.width >= len(PATTERN_42[0]) and maze.height >= len(PATTERN_42)


def apply_42_pattern(maze: Maze) -> None:
    """Apply the 42 pattern by closing walls around marked cells."""
    if not can_apply_42_pattern(maze):
        return

    pattern_h = len(PATTERN_42)
    pattern_w = len(PATTERN_42[0])

    start_x = (maze.width - pattern_w) // 2
    start_y = (maze.height - pattern_h) // 2

    # mark cells
    for py in range(pattern_h):
        for px in range(pattern_w):
            if PATTERN_42[py][px] == 1:
                cx = start_x + px
                cy = start_y + py

                cell = maze.get_cell(cx, cy)
                if cell:
                    cell.is_42 = True
                    cell.visited = True  # important for DFS

    # close walls around 42
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if not cell or not cell.is_42:
                continue

            for neighbor in maze.get_neighbors(cell):
                if not neighbor.is_42:
                    maze.close_wall_between(cell, neighbor)