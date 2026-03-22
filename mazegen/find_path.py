from typing import Dict, List, Optional, Tuple
from collections import deque
from .maze import Maze

Coord = Tuple[int, int]


def _open_neighbors(maze: Maze, coord: Coord) -> List[Coord]:
    x, y = coord
    cell = maze.get_cell(x, y)

    if not cell or cell.is_42:
        return []

    directions = [
        (0, -1, cell.north),  # N
        (0, 1, cell.south),   # S
        (-1, 0, cell.west),   # W
        (1, 0, cell.east),    # E
    ]

    result: List[Coord] = []

    for dx, dy, wall in directions:
        if not wall:
            nx, ny = x + dx, y + dy
            neighbor = maze.get_cell(nx, ny)

            if neighbor and not neighbor.is_42:
                result.append((nx, ny))

    return result


def bfs_shortest_path(maze: Maze) -> List[Coord]:
    start = maze.entry
    goal = maze.exit

    start_cell = maze.get_cell(*start)
    goal_cell = maze.get_cell(*goal)

    if not start_cell or not goal_cell:
        return []

    if start_cell.is_42 or goal_cell.is_42:
        return []

    queue = deque([start])
    came_from: Dict[Coord, Optional[Coord]] = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in _open_neighbors(maze, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return []

    path: List[Coord] = []
    node: Optional[Coord] = goal

    while node is not None:
        path.append(node)
        node = came_from[node]

    path.reverse()
    return path


def mark_path(maze: Maze, path: List[Coord]) -> None:
    for x, y in path:
        cell = maze.get_cell(x, y)
        if cell:
            cell.in_path = True