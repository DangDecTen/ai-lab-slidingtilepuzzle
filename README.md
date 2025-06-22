# Sliding Tile Puzzle Solver

A Python project for solving N-puzzle problems using classical AI search algorithms with GUI.

## 🚀 Features

### Core Algorithms
- **Breadth-First Search (BFS)** - Optimal solution, guaranteed shortest path
- **Depth-First Search (DFS)** - Memory efficient, may find longer solutions  
- **A* Search** - Optimal with Manhattan distance heuristic

## 📁 Project Structure

```
AI-Fundamentals/
├── main.py                    # Run solvers and generate output
├── gui.py                     # Dummy GUI
├── puzzle_gui.py       # Visualize puzzles and solutions
├── report.py                  # Summarize output results
├── algorithms/                # Core logic of the project
├── data/
│   ├── input/                 # JSON definitions of initial state
│   └── output/                # JSON solution results
├── utils/                     # Helper functions
├── final_report.md            # Techinical report
└── README.md
```

## 📦 Prerequisites

```bash
pip install pygame
```

## ⚙️ How to Run

### Command Line Interface

Run a single puzzle:
```bash
python main.py --input data/input/easy_8_puzzle.json --algorithm a_star --heuristic manhattan
```

Run all puzzles with BFS:
```bash
python main.py --all --algorithm bfs
```

**Command Line Options:**
| Flag | Description | Options |
|------|-------------|---------|
| `--input` | Path to input file | Any `.json` file in `data/input/` |
| `--all` | Run on all input files | - |
| `--algorithm` | Search algorithm | `bfs`, `dfs`, `a_star`, `ucs` |
| `--heuristic` | Heuristic function | `manhattan`, `none` |

### GUI

Launch the GUI:
```bash
python puzzle_gui.py
```

Ensure at least one solution exists in `data/output/` before running.



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



## 🧪 Generating Random Puzzles

```python
from utils.generator import generate_random_puzzle
state = generate_random_puzzle(size=3, shuffle_moves=100)
```



## 📬 License & Credits

MIT License. Built for educational and experimentation purposes with clean modular design.
