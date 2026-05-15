# Maze Pathfinder

|    NRP     |      Name      |
| :--------: | :------------: |
| 5025241053 | Ary Pasya Fernanda |
| 5025241129 | Mochamad Ramadhan Aditya Rachaman |
| 5025241147 | Lucky Himawan Prasetya |

> An interactive maze generator and pathfinder built with Pygame featuring real-time Dijkstra algorithm visualization.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green?style=flat-square&logo=python)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## About the Project

**Maze Pathfinder** is an educational game application that combines maze exploration gameplay with pathfinding algorithm visualization. Players navigate through procedurally generated mazes, while the hint feature displays the inner workings of the **Dijkstra** algorithm in real-time — which cells are being explored, and the shortest path found.

This project is ideal for:
- Beginners who want to understand **graph algorithms** visually
- Developers learning **Pygame** and simple game architecture
- Demonstrations of **DFS maze generation** and **Dijkstra pathfinding**

---

## Features

| Feature | Description |
|---|---|
| **Procedural Maze** | A unique maze every session using DFS Recursive Backtracker |
| **Dijkstra Hint** | Real-time visualization of the optimal path & explored cells |
| **Live Statistics** | Player steps, time elapsed, and route efficiency |
| **6 Levels** | Maze grows larger each level (11×11 up to 35×35) |
| **Player Trail** | Player movement history displayed on the grid |
| **Win Screen** | Performance summary with optimal path comparison |
| **Dual Input** | Supports both Arrow Keys and WASD |
| **Web-Ready** | Compatible with Pygbag for browser-based deployment |

---

## Screenshot

<img width="527" height="683" alt="screenshot-2026-05-14_17 49 24" src="https://github.com/user-attachments/assets/c1b0a96f-3ed8-442e-9c5a-2cb956d70a72" />

**Color legend:**

| Color | Element |
|---|---|
| 🟢 Neon Green | START position |
| 🟠 Orange | END position (goal) |
| 🔵 Bright Cyan | Current player position |
| 🟦 Dark Blue | Player movement trail |
| 💙 Light Blue | Dijkstra optimal hint path |
| 🟣 Dark Purple | Cells explored by Dijkstra |

---

## Project Architecture

```
maze-pathfinder/
│
├── main.py             # Entry point — main game loop (async/Pygbag-ready)
│
├── core/
│   ├── cell.py         # Single grid cell representation (walls & connections)
│   ├── maze.py         # Maze grid + DFS generator
│   ├── player.py       # Player state (position, steps, history)
│   └── game_state.py   # State machine: PLAYING → WIN, movement & hint logic
│
├── algorithms/
│   └── dijkstra.py     # Dijkstra algorithm (pathfinding + path reconstruction)
│
├── visualization/
│   ├── renderer.py     # All drawing operations via Pygame
│   ├── ui.py           # UI components: Button, Toast notification
│   └── colors.py       # RGB color constants
│
└── requirements.txt    # Python dependencies
```

**Design patterns used:**
- **State Machine** — `GameState` manages the `PLAYING → WIN` transition
- **Separation of Concerns** — logic, rendering, and algorithms are decoupled
- **Lazy Evaluation** — Dijkstra hint is only computed when the user requests it

---

## Code Explanation

### `cell.py` — Cell Representation

Each cell in the maze grid has 4 walls (top, right, bottom, left). A wall set to `True` means it is closed; `False` means it is open (a passable path).

```python
class Cell:
    DIRS = {
        "top":    (-1,  0),
        "bottom": ( 1,  0),
        "left":   ( 0, -1),
        "right":  ( 0,  1),
    }
```

The `open_neighbors()` method returns a list of accessible neighbors — used by Dijkstra during graph traversal.

---

### `maze.py` — DFS Recursive Backtracker Generator

The maze is built using an **iterative DFS with a stack**. This algorithm guarantees that every generated maze is a *perfect maze* (there is always exactly one path between any two points).

```python
def _generate(self):
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        r, c = stack[-1]
        unvisited = [unvisited neighbors]
        if unvisited:
            pick random → remove wall → push to stack
        else:
            stack.pop()  # backtrack
```

**Complexity:** O(rows × cols) — each cell is visited exactly once.

---

### `dijkstra.py` — Pathfinding with Priority Queue

The Dijkstra implementation uses `heapq` (min-heap). Since every step has an equal weight of 1, Dijkstra is equivalent to BFS here, but the heap is retained to correctly represent the original algorithm.

```python
def dijkstra(maze, start, end):
    heap = [(0, start_row, start_col)]   # (distance, r, c)
    while heap:
        d, r, c = heapq.heappop(heap)
        for nr, nc in maze.neighbors_open(r, c):
            if new_dist < dist.get(nb, ∞):
                dist[nb] = new_dist
                heapq.heappush(heap, (new_dist, nr, nc))
```

This function returns two values:
- `path` — list of coordinates from START to END (shortest path)
- `visited` — all cells explored during the search (for purple visualization)

**Complexity:** O((V + E) log V) — V = number of cells, E = number of open edges.

---

### `game_state.py` — Logic & State Machine

`GameState` is the core of the game. It ties together the maze, player, hint system, and timer.

```python
class State(Enum):
    PLAYING = auto()
    WIN     = auto()

class GameState:
    LEVEL_SIZES = [11, 15, 19, 23, 29, 35]  # maze size per level
```

Key methods:
- `move(direction)` — validates walls, moves the player, checks win condition
- `toggle_hint()` — runs/disables Dijkstra from the current player position
- `tick()` — updates the timer every frame

---

### `renderer.py` — Layered Rendering

Drawing is performed in a defined layer order to prevent elements from overlapping incorrectly:

```
Layer 1:  Cell background (passage / trail / hint)
Layer 2:  Hint visited (purple — Dijkstra explored cells)
Layer 3:  Player trail (dark blue)
Layer 4:  Hint path highlight (transparent cyan via SRCALPHA)
Layer 5:  Wall lines
Layer 6:  START & END markers
Layer 7:  Player circle + glow effect
Layer 8:  Right-side UI panel
Layer 9:  Win screen overlay (when player wins)
Layer 10: Toast notification
```

---

### `ui.py` — UI Components

- **`Button`** — clickable button with hover effect, supports disabled state
- **`Toast`** — temporary notification (2.5 seconds) with fade-out animation in the last 0.5 seconds

---

### `colors.py` — Color System

All colors are defined as centralized RGB constants, making it easy to restyle the app without touching rendering code.

```python
BG_DARK       = (  8,  18,  28)   # dark background
PLAYER_COLOR  = (  0, 220, 255)   # bright cyan for player
HINT_VISITED  = ( 80,  20, 150)   # purple for Dijkstra cells
```

---

## How to Run

### Prerequisites

- **Python 3.10** or newer
- **pip** (Python package manager)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/username/maze-pathfinder.git
cd maze-pathfinder
```

**2. (Optional) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python main.py
```

### Running in Browser (via Pygbag)

This project is already compatible with **Pygbag** for web deployment:

```bash
pip install pygbag
pygbag main.py
```

Open `http://localhost:8000` in your browser once the build is complete.

---

## ⌨️ Controls

| Key | Function |
|---|---|
| `↑` `↓` `←` `→` | Move player |
| `W` `A` `S` `D` | Move player (alternative) |
| `H` | Toggle Dijkstra hint on/off |
| `R` | Restart from starting position (same maze) |
| `N` | Generate new maze (same level) / advance to next level (when won) |
| `ESC` | Quit the application |

---

## Algorithms

### DFS Recursive Backtracker (Maze Generation)

Generates a *perfect maze* — a labyrinth where every two cells share exactly one unique path. This property ensures the maze always has a solution and no cell is ever isolated.

```
Start at (0,0)
  → Randomly pick an unvisited neighbor
  → Remove the wall between them
  → Move to that neighbor
  → If no unvisited neighbors → backtrack
  → Repeat until all cells are visited
```

### Dijkstra (Pathfinding)

Finds the shortest path from the player's current position to the goal. Since all edges have a weight of 1, the minimum number of steps equals the BFS distance, but the heap implementation is retained for an accurate representation of the algorithm.

The hint displays two pieces of information simultaneously:
- **Purple cells** — cells "seen" by the algorithm (explored)
- **Bright blue cells** — the shortest path found (optimal path)

---

## Levels & Progression

| Level | Maze Size | Total Cells |
|---|---|---|
| 1 | 11 × 11 | 121 |
| 2 | 15 × 15 | 225 |
| 3 | 19 × 19 | 361 |
| 4 | 23 × 23 | 529 |
| 5 | 29 × 29 | 841 |
| 6+ | 35 × 35 | 1,225 |

Each new level generates a larger and more complex maze. After level 6, the size stays at 35×35 but the layout is always different.

---

## Roadmap

- [ ] Add A* algorithm as an alternative hint mode
- [ ] Timer mode with local leaderboard
- [ ] Player animation (sprite movement)
- [ ] Selectable color themes (dark / light / retro)
- [ ] Export maze as PNG image
- [ ] Local multiplayer (split screen)

---

## Contributing

Contributions are very welcome! Feel free to open an *issue* to report bugs or suggest new features, then submit a *pull request* with a clear description of your changes.

---
