*This project has been created as part of the 42 curriculum by feel-idr, zahraka.*

# A-Maze-ing

## Description

A-Maze-ing generates, solves, displays, and exports mazes from a configuration file.
The application has four main parts:

- maze generation (DFS or Prim)
- shortest path computation (BFS)
- interactive terminal display
- output export to text format

The maze can include a blocked "42" pattern when maze dimensions are large enough.

## Instructions

### 1) Install dependencies

```bash
make install
```

### 2) Run with default config

```bash
make run
```

### 3) Run debugger

```bash
make debug
```

### 4) Build python package files

```bash
make build
```

### 5) Create the expected root archive `mazegen.tar.gz`

```bash
make package
```

### 6) Clean generated files

```bash
make clean
```

## Configuration File

Default configuration file: `config.txt`

Example:

```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=10,14
OUTPUT_FILE=maze.out
PERFECT=True
SEED=42
ALGORITHM=PRIM
```

Supported keys:

- `WIDTH` (required): integer > 0
- `HEIGHT` (required): integer > 0
- `ENTRY` (required): tuple-like `x,y`, both integers within bounds
- `EXIT` (required): tuple-like `x,y`, both integers within bounds
- `OUTPUT_FILE` (required): non-empty path for exported maze
- `PERFECT` (required): `True` or `False`
- `SEED` (optional): integer >= 0, enables reproducible generation
- `ALGORITHM` (optional): `DFS` or `PRIM`

Format rules:

- comments start with `#`
- every non-comment line must be `KEY=VALUE`
- keys are case-insensitive
- duplicate keys are rejected

Validation behavior:

- missing required keys raise an error
- malformed values raise an error with details
- `ENTRY` and `EXIT` must be different and inside maze bounds

## Chosen Maze Algorithm

Implemented algorithms:

- DFS (recursive depth-first search)
- Prim (randomized frontier expansion)

Reason for this choice:

- DFS is simple and fast, producing long corridors
- Prim produces more distributed branching
- supporting both allows comparing styles while reusing the same maze model

## Reusable Module Documentation

Reusable package name: `mazegen`

Main public objects:

- `MazeGenerator` (alias of `Generator`): creates mazes
- `Maze`: maze representation and wall operations
- `bfs_shortest_path`: shortest path from entry to exit

Example:

```python
from mazegen import MazeGenerator, bfs_shortest_path

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(10, 14),
    seed=42,
    perfect=True,
    output_file="maze.out",
    algorithm="PRIM",
)
generator.generate()
maze = generator.get_maze()
path = bfs_shortest_path(maze)
```

## Display and Interaction

The terminal viewer supports:

- regenerate maze (`r`)
- show/hide shortest path (`p`)
- cycle wall colors (`c`)
- quit (`q`)

## Export Format

The output file contains:

- `HEIGHT` lines of `WIDTH` hexadecimal wall values
- one empty line
- `ENTRY` coordinate line (`x,y`)
- `EXIT` coordinate line (`x,y`)
- shortest path encoded with `N`, `E`, `S`, `W`

## Resources

External references used and how they were used:

- Python docs (`typing`, `pathlib`, packaging): module typing, file export, build setup
- BFS/DFS references (GeeksforGeeks and class notes): shortest-path and DFS traversal design
- Prim algorithm references (articles and notes): alternative maze-generation implementation
- ANSI terminal documentation: colored interactive rendering and controls

## Team and Project Management

### Roles of each team member

- `feel-idr`
  - config parsing and validation
  - BFS shortest path and path marking
  - integration of the 42 pattern constraints
  - project scaffolding and Makefile baseline

- `zahraka`
  - DFS and Prim generation logic
  - interactive terminal renderer
  - maze export formatting
  - packaging and build workflow

### Anticipated planning and how it evolved

- Initial plan
  - week 1: parser + maze core classes
  - week 2: generation + shortest path
  - week 3: display + export + packaging

- Actual evolution
  - generation and parser finished first
  - display took longer because terminal-size and refresh behavior needed extra work
  - packaging and lint/type checks were added earlier than planned to stabilize submissions

### What worked well and what could be improved

What worked well:

- modular separation (`mazegen`, `utils`, `display`, `export`)
- deterministic tests with `SEED`
- strict parser validation reduced runtime errors

What could be improved:

- add unit tests for edge cases and export/path consistency
- improve UX for tiny terminals
- extend algorithm benchmarking and performance profiling

### Tools used

- Git and GitHub for collaboration and review
- Makefile for repeatable local commands
- `flake8` and `mypy` for code quality checks
- Python virtual environments for isolated packaging tests

## Conclusion

This project demonstrates:

- algorithm implementation (DFS, Prim, BFS)
- modular Python architecture
- interactive terminal UX
- reusable package creation and installation workflow
