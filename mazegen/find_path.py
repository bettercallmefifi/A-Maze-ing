from typing import Dict, List, Optional, Tuple
from .maze import Maze

Coord = Tuple[int, int]


def _open_neighbors(maze: Maze, coord: Coord) -> List[Coord]:
    """Return reachable neighbors without walls or 42 blocks."""
    x, y = coord
    cell = maze.get_cell(x, y)
    if cell is None:
        return []
    if cell.is_42:
        return []

    neighbors: List[Coord] = []
    if not cell.north:
        neighbors.append((x, y - 1))
    if not cell.south:
        neighbors.append((x, y + 1))
    if not cell.west:
        neighbors.append((x - 1, y))
    if not cell.east:
        neighbors.append((x + 1, y))

    valid_neighbors: List[Coord] = []
    for nx, ny in neighbors:
        neighbor_cell = maze.get_cell(nx, ny)
        if neighbor_cell is not None and not neighbor_cell.is_42:
            valid_neighbors.append((nx, ny))

    return valid_neighbors


def bfs_shortest_path(maze: Maze) -> List[Coord]:
    """Compute the shortest path using BFS on the maze."""
    start = maze.entry
    goal = maze.exit

    queue: List[Coord] = [start]
    came_from: Dict[Coord, Optional[Coord]] = {start: None}  # child -> parent

    while queue:
        current_coord = queue.pop(0)
        if current_coord == goal:
            break

        for neighbor in _open_neighbors(maze, current_coord):
            if neighbor not in came_from:
                came_from[neighbor] = current_coord
                queue.append(neighbor)

    if goal not in came_from:
        return []

    path: List[Coord] = []
    current_node: Optional[Coord] = goal
    while current_node is not None:
        path.append(current_node)
        current_node = came_from[current_node]
    path.reverse()

    return path


def mark_path(maze: Maze, path: List[Coord]) -> None:
    """Mark cells in a path so the renderer can highlight them."""
    for x, y in path:
        cell = maze.get_cell(x, y)
        if cell is not None:
            cell.in_path = True