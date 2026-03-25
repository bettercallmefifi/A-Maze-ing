This project has been created as part of the curriculum by feel-idr and zahraka.

# A-Maze-ing

Python maze generator with:

- DFS or Prim generation
- BFS shortest-path solving
- Hex export format
- Terminal interactive renderer
- 42 pattern integration

## Installation

Using Makefile:

```bash
make install
```

Manual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

## Run

```bash
make run
```

Or:

```bash
python3 a_maze_ing.py config.txt
```

Debug:

```bash
make debug
```

Lint:

```bash
make lint
```

## Config

Example:

```txt
WIDTH=21
HEIGHT=21
ENTRY=4,3
EXIT=14,20
OUTPUT_FILE=maze.out
PERFECT=True
ALGORITHM=prim
SEED=42
```

Parameters:

| Key         | Type           | Required | Notes |
| ----------- | -------------- | -------- | ----- |
| WIDTH       | int            | yes      | > 0 |
| HEIGHT      | int            | yes      | > 0 |
| ENTRY       | tuple(int,int) | yes      | in bounds |
| EXIT        | tuple(int,int) | yes      | in bounds, different from ENTRY |
| OUTPUT_FILE | string         | yes      | non-empty |
| PERFECT     | bool           | yes      | true/false |
| ALGORITHM   | string         | no       | DFS or PRIM, default DFS |
| SEED        | int            | no       | deterministic when provided |

## Terminal Renderer Controls

| Key | Action |
| --- | ------ |
| r   | Regenerate maze |
| p   | Show/hide shortest path |
| c   | Cycle wall color |
| q   | Quit |

Behavior notes:

- After pressing r, path display is reset.
- You must press p again to show the path for the new maze.

## Seed Behavior

- If SEED is provided, generation is deterministic.
- Using the same WIDTH/HEIGHT/ENTRY/EXIT/PERFECT/ALGORITHM/SEED gives the same maze.
- Regenerate (r) reuses the configured seed in the same run.
- If SEED is omitted, generation uses time-based randomness.

## 42 Pattern Rules

The 42 pattern is embedded into the maze and blocks its marked cells.

Rules:

- Minimum maze size is 7x5.
- If size is smaller than 7x5, generation stops with an error.
- ENTRY and EXIT must not overlap any 42-pattern cell.

If constraints are violated, the app prints an error and does not generate/export the maze.

## Algorithms

Supported generation algorithms:

- DFS
- PRIM

Pathfinding:

- BFS shortest path from ENTRY to EXIT

## Export Format

Each cell is encoded in hexadecimal using wall bits:

| Direction | Bit |
| --------- | --- |
| North     | 1 |
| East      | 2 |
| South     | 4 |
| West      | 8 |

Examples:

- 0 means no walls
- F means all walls

## Project Structure

- a_maze_ing.py: CLI entry point
- utils/parsing.py: config parsing and validation
- mazegen/generator.py: maze generation logic
- mazegen/pattern_42.py: 42 pattern marking/applying
- mazegen/find_path.py: BFS shortest path
- display/render.py: terminal interactive renderer
- export/export.py: hex export

## Team Roles

- feel idr:
	- configuration parsing and validation
	- BFS shortest path implementation
	- 42 pattern integration
	- project tooling and structure (Makefile, packaging)

- zahraka:
	- maze generation algorithms (DFS, PRIM)
	- core maze model and wall logic
	- terminal rendering workflow and controls
	- export format implementation
