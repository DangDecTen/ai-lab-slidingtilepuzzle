# 🧩 Sliding Tile Puzzle Solver

A modular Python project to solve the N-puzzle problem using classic search algorithms like BFS, DFS, and A* — with performance tracking and animated GUI visualization using Pygame.

---

## 🚀 Features

- Solves `N x N` sliding tile puzzles (e.g., 3x3, 4x4)
- Supports multiple search algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search (Manhattan heuristic)
- Supports both batch and single-file solving
- Generates structured output with statistics
- Animated GUI visualization (Pygame)

---

## 📁 Project Structure

```
sliding-tile-solver/
├── main.py              # Run solvers and generate output
├── gui.py               # Visualize puzzles and solutions
├── report.py            # (Optional) summarize output results
├── algorithms/          # bfs.py, dfs.py, a_star.py
├── data/
│   ├── input/           # JSON puzzle definitions
│   ├── output/          # JSON solution reports
├── utils/               # move.py, validate.py, node.py, generator.py
├── assets/              # Fonts, tile images (if any)
├── README.md
```

---

## 📦 Installation

```bash
pip install pygame
```

---

## 🧮 Input Format (JSON)

Place in `data/input/` folder:
```json
{
  "name": "Simple 3x3 Puzzle",
  "size": 3,
  "initial_state": [1, 2, 3, 4, 5, 6, 0, 7, 8],
  "goal_state": [1, 2, 3, 4, 5, 6, 7, 8, 0]
}
```

---

## ⚙️ Running the Solver

### Run a single file:
```bash
python main.py --input data/input/simple_3x3.json --algorithm a_star --heuristic manhattan
```

### Run all input files:
```bash
python main.py --all --algorithm bfs
```

### Options:
| Flag | Description |
|------|-------------|
| `--input` | path to input file |
| `--all`   | run on all input files |
| `--algorithm` | `bfs`, `dfs`, `a_star` |
| `--heuristic` | `manhattan` or `none` (only for A*) |

---

## 📤 Output Format (JSON)

Stored in `data/output/` with matching filenames:
```json
{
  "puzzle_name": "Simple 3x3 Puzzle",
  "size": 3,
  "initial_state": [...],
  "goal_state": [...],
  "algorithm": "a_star",
  "heuristic": "manhattan",
  "status": "Path found",
  "solution_path": ["R", "D", ...],
  "solution_length": 12,
  "time_taken": 0.035,
  "space_used": 1341,
  "nodes_expanded": 589
}
```

---

## 🎮 Running the GUI

```bash
python gui.py
```

### Controls:
- `SPACE`: play/pause animation
- `→`: step one move
- `←`: switch to next puzzle

Ensure at least one solution exists in `data/output/` before running.

---

## ➕ Adding a New Algorithm

1. Create a new file in `algorithms/`, e.g. `greedy.py`.
2. Implement a `solve(initial_state, goal_state, size, heuristic=None)` method.
3. Add it to `ALGORITHMS` in `main.py`:
```python
from algorithms import greedy
ALGORITHMS = {
  ...,
  "greedy": greedy.solve
}
```
4. Run it using:
```bash
python main.py --input data/input/your_file.json --algorithm greedy --heuristic manhattan
```

---

## 🧪 Generating Random Puzzles

```python
from utils.generator import generate_random_puzzle
state = generate_random_puzzle(size=3, shuffle_moves=100)
```

---

## 📬 License & Credits

MIT License. Built for educational and experimentation purposes with clean modular design.
