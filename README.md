*This project has been created as part of the curriculum by *feel-idr*, *zahraka*.*

#  A-Maze-ing

---

##  Description

**A-Maze-ing** is a Python-based project that generates, solves, exports, and visualizes mazes.

The project has two main goals:

1. **Algorithmic**: Generate a valid maze using graph traversal algorithms.
2. **Software engineering**: Build a clean, reusable, modular Python package.

The system:

* Generates a maze grid with walls
* Ensures a valid path between entry and exit
* Computes the shortest path using BFS
* Exports the maze in a **hexadecimal encoded format**
* Displays the maze using a **pygame graphical interface with animation**

---

##  Core Concepts

This project is based on several fundamental computer science concepts:

* Graph representation (grid = graph)
* Depth-First Search (DFS)
* Breadth-First Search (BFS)
* Pathfinding algorithms
* Object-Oriented Programming (OOP)
* Modular architecture

---

##  Instructions

###  Installation

Using Makefile:

```bash
make install
```

Manual installation:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

---

###  Execution

```bash
make run
```

Or:

```bash
python3 a_maze_ing.py config.txt
```

---

###  Debug Mode

```bash
make debug
```

---

##  Configuration File (FULL SPEC)

Example:

```txt
WIDTH=21
HEIGHT=21
ENTRY=0,0
EXIT=20,20
OUTPUT_FILE=maze.out
PERFECT=True
SEED=42
```

###  Detailed Parameters

| Key         | Type           | Description                   |
| ----------- | -------------- | ----------------------------- |
| WIDTH       | int            | Number of columns             |
| HEIGHT      | int            | Number of rows                |
| ENTRY       | tuple(int,int) | Start coordinate              |
| EXIT        | tuple(int,int) | End coordinate                |
| OUTPUT_FILE | string         | Output file name              |
| PERFECT     | bool           | Perfect maze (tree structure) |
| SEED        | int (optional) | Random seed                   |

---

###  Validation Rules

* WIDTH and HEIGHT must be > 0
* ENTRY and EXIT must be inside bounds
* ENTRY ≠ EXIT
* Coordinates must be positive integers

---

##  Maze Generation Algorithm

###  DFS (Depth-First Search) — Default

#### Principle:

* Start from entry
* Visit a random neighbor
* Remove wall between cells
* Continue recursively
* Backtrack when stuck

#### Properties:

* Produces a **perfect maze** (no cycles)
* Guarantees a path between any two cells
* Creates long corridors

---

### 🔹 Prim’s Algorithm (Alternative)

#### Principle:

* Start from a random cell
* Add neighbors to frontier
* Randomly connect cells

#### Properties:

* More random structure
* Shorter corridors

---

##  Why DFS was chosen?

* Simpler to implement
* More intuitive
* Produces visually pleasing mazes
* Works naturally with stack/recursion
* Efficient for medium-size grids

---

##  Maze Representation

Each maze is a grid of `Cell` objects:

Each cell contains:

* Position `(x, y)`
* Walls: North, East, South, West
* Flags:

  * `visited`
  * `is_42` (pattern cells)
  * `in_path`

Walls are encoded as:

* `True` = wall exists
* `False` = open path

---

##  Hexadecimal Encoding (Export)

Each cell is converted into a hexadecimal value using bitwise encoding:

| Direction | Bit |
| --------- | --- |
| North     | 1   |
| East      | 2   |
| South     | 4   |
| West      | 8   |

Example:

* `0` → no walls
* `F` → all walls

---

##  Pathfinding (BFS)

The shortest path is computed using **Breadth-First Search**.

### Why BFS?

* Guarantees shortest path in unweighted graphs
* Simple and efficient

Steps:

1. Start from ENTRY
2. Explore neighbors level by level
3. Track visited nodes
4. Reconstruct path

---

##  Visualization (pygame)

The maze is rendered using pygame with:

### Features:

* Wall drawing
* Entry (green)
* Exit (red)
* Path visualization (orange)
* 42 pattern highlighting (blue)
* Animated generation

---

###  Controls

| Key     | Action               |
| ------- | -------------------- |
| R       | Regenerate maze      |
| P       | Toggle shortest path |
| C       | Change wall color    |
| Q / ESC | Quit                 |

---

##  Special Feature: 42 Pattern

A predefined pattern is inserted into the maze:

* Blocks certain cells
* Adds visual identity
* Affects pathfinding

Constraints:

* Only applied if maze is large enough
* Cannot overlap entry/exit

---

##  Reusable Module: `mazegen`

The project is designed as a reusable package.

### Modules:

* `generator.py` → Maze generation logic
* `maze.py` → Grid structure
* `cell.py` → Cell model
* `find_path.py` → BFS algorithm
* `pattern_42.py` → Pattern logic

---

###  Example Usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    seed=42,
    perfect=True,
    output_file="maze.txt"
)

gen.generate()
maze = gen.get_maze()
```

---

##  Team & Project Management

###  Roles

* Feel-idr:

  * Configuration parsing (`ConfigParser`)
  * BFS shortest path implementation
  * 42 pattern integration
  * Makefile setup
  * Packaging (`pyproject.toml`)
  * Project structure & organization

* Zahraka:

  * Maze generation algorithms (DFS / Prim)
  * Core maze logic (`Maze`, `Cell`)
  * Rendering system (pygame)
  * Export system (hexadecimal format)
  * Animation and visualization


###  Planning

| Phase  | Goal                |
| ------ | ------------------- |
| Week 1 | Research algorithms |
| Week 2 | Implement DFS       |
| Week 3 | Add BFS + export    |
| Week 4 | Add rendering       |
| Week 5 | Debug & optimize    |

---

###  Evolution

* Initial version: basic DFS
* Added modular architecture
* Introduced BFS pathfinding
* Added animation & UI
* Improved validation & error handling

---

###  What Worked Well

* Clean architecture
* Separation of concerns
* Reusable design
* Strong algorithmic base

---

###  Improvements

* Add more algorithms (Kruskal, Wilson)
* Improve UI/UX
* Add maze difficulty levels
* Optimize large mazes

---

##  Tools Used

* Python 3.10+
* pygame
* flake8 (linting)
* mypy (type checking)
* Makefile

---

##  Resources

* Python Documentation
* BFS & DFS algorithm tutorials
* Maze generation references
* pygame documentation

Used for:

* Algorithm design
* Pathfinding
* Rendering system

---

##  Conclusion

This project combines:

* Algorithmic problem solving
* Data structures
* Software engineering best practices

It demonstrates how to build a complete system:
**from generation → to solving → to visualization → to export**

---
