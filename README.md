*This project has been created as part of the 42 curriculum by feel-idr, zahraka.*

---

#  A-Maze-ing

##  Description

A-Maze-ing is a Python project that generates, solves, visualizes, and exports mazes.

The project is divided into several modules:

* A **maze generator** using DFS or Prim algorithms
* A **pathfinding system** using BFS (shortest path)
* A **terminal-based interactive renderer**
* A **file exporter** that outputs the maze in hexadecimal format

Additionally, the maze includes a special **"42 pattern"** embedded into its structure.

---

##  Instructions

###  Installation

```bash
make install
```

###  Run the project

```bash
make run
```

###  Debug mode

```bash
make debug
```

###  Clean project

```bash
make clean
```

---

##  Configuration file

The program requires a configuration file (e.g., `config.txt`).

### Example:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=10,14
OUTPUT_FILE=maze.out
PERFECT=True
ALGORITHM=PRIM
```

###  Parameters:

* `WIDTH`, `HEIGHT`: Maze dimensions
* `ENTRY`: Start position (x,y)
* `EXIT`: End position (x,y)
* `OUTPUT_FILE`: Output file name
* `PERFECT`:

  * `True` → no cycles (perfect maze)
  * `False` → allows multiple paths
* `SEED` (optional): Random seed
* `ALGORITHM`: `DFS` or `PRIM`

---

##  Maze Algorithm

### Chosen algorithm: **DFS (Depth-First Search)** and **Prim**

* DFS generates long corridors and is simple to implement.
* Prim creates more uniform and complex mazes.

###  Why this choice?

* DFS is **fast and easy**
* Prim provides **better randomness**
* Supporting both allows flexibility

---

##  Pathfinding

We use **BFS (Breadth-First Search)** to compute the shortest path from ENTRY to EXIT.

* Guarantees shortest path
* Avoids blocked cells (42 pattern)

---

##  Reusable Module: `mazegen`

The `mazegen` package is reusable and contains:

* `Maze`: grid structure
* `Cell`: individual cell with walls
* `Generator`: maze generation (DFS / Prim)
* `find_path`: BFS algorithm

### Example usage:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(...)
generator.generate()
maze = generator.get_maze()
```

---

##  Display System

The project includes a terminal renderer:

* Shows maze with ANSI colors
* Interactive controls:

  * `r` → regenerate maze
  * `p` → show shortest path
  * `c` → change colors
  * `q` → quit

---

##  Export System

The maze is exported as:

* Hexadecimal grid (walls encoding)
* Entry and exit coordinates
* Shortest path directions (N/E/S/W)

---

##  Resources

* Python official documentation
* BFS & DFS algorithms (GeeksforGeeks)
* ANSI terminal color codes

These resources were used for:

* Algorithm implementation
* Terminal rendering
* Project structure design

---

##  Team & Project Management

###  Roles

* **feel-idr**:

  * Parsing (config file)
  * BFS shortest path
  * 42 pattern integration
  * Project structure
  * Makefile

* **zahraka**:

  * Maze generation (DFS / Prim)
  * Rendering system
  * Export system
  * Managed project tooling and the packaging structure 

---

##  Conclusion

This project demonstrates:

* Algorithm design (DFS, BFS, Prim)
* Modular Python architecture
* Interactive terminal UI
* Clean and reusable code design

---
