# AI Sliding Puzzle Solver 🧩

A comprehensive Python project for solving N-puzzle problems using classical AI search algorithms with a modern, beautiful GUI interface and extensive test automation.

## 🚀 Features

### Core Algorithms
- **Breadth-First Search (BFS)** - Optimal solution, guaranteed shortest path
- **Depth-First Search (DFS)** - Memory efficient, may find longer solutions  
- **A* Search** - Optimal with Manhattan distance heuristic

### Modern GUI Interface
- **Beautiful Modern Design** - Clean, intuitive interface with modern styling
- **Real-time Visualization** - Watch algorithms solve puzzles step by step
- **Interactive Controls** - Play, pause, step through solutions
- **Performance Statistics** - Detailed metrics and timing information
- **Speed Controls** - Adjustable animation speed
- **Multiple Puzzle Support** - Both 8-puzzle (3x3) and 15-puzzle (4x4)

### Puzzle Collection
- **8-Puzzle Variants**: Easy, Medium, Hard, Challenging, Random, Spiral, Corner Challenge
- **15-Puzzle Variants**: Easy, Medium, Hard, Challenging, Very Hard, Random
- **Test Automation** - Comprehensive testing across all puzzles and algorithms

### Technical Features
- Modular, extensible architecture
- JSON-based puzzle definitions
- Comprehensive output with performance metrics
- Automated test runner with detailed reports
- Cross-platform compatibility

## 📁 Project Structure

```
AI-Fundamentals/
├── main.py                    # Core solver engine
├── puzzle_gui_modern.py       # Modern GUI interface
├── run_modern_gui.py          # GUI launcher script
├── test_automation.py         # Automated test runner
├── algorithms/
│   ├── bfs.py                # Breadth-First Search
│   ├── dfs.py                # Depth-First Search
│   └── a_star.py             # A* with Manhattan heuristic
├── data/
│   ├── input/                # Puzzle definitions
│   │   ├── easy_8_puzzle.json
│   │   ├── medium_8_puzzle.json
│   │   ├── hard_8_puzzle.json
│   │   ├── challenging_8_puzzle.json
│   │   ├── random_8_puzzle_a.json
│   │   ├── random_8_puzzle_b.json
│   │   ├── spiral_8_puzzle.json
│   │   ├── corner_challenge_8_puzzle.json
│   │   ├── easy_15_puzzle.json
│   │   ├── medium_15_puzzle.json
│   │   ├── hard_15_puzzle.json
│   │   ├── challenging_15_puzzle.json
│   │   ├── very_hard_15_puzzle.json
│   │   ├── random_15_puzzle_a.json
│   │   └── random_15_puzzle_b.json
│   └── output/               # Solution results
├── utils/
│   ├── move.py              # Move operations
│   ├── node.py              # Search tree nodes
│   ├── priority_queue.py    # Priority queue implementation
│   └── validate.py          # Puzzle validation
└── README.md
```

## 📦 Prerequisites

```bash
pip install pygame
```



## ⚙️ How to Run

### 🎮 Modern GUI Interface (Recommended)

Launch the beautiful, modern GUI:
```bash
python run_modern_gui.py
```

**GUI Features:**
- Select any puzzle from the dropdown menu
- Choose algorithm (BFS, DFS, A* with Manhattan heuristic)
- Interactive controls: Solve, Play/Pause, Step, Reset
- Real-time performance statistics
- Adjustable animation speed
- Modern, responsive design

### 🤖 Automated Testing

Run comprehensive tests on all puzzles:
```bash
python test_automation.py
```

This will:
- Test all puzzles with all applicable algorithms
- Generate performance reports
- Save detailed results to `data/test_report.json`
- Show comparison between algorithms

### 💻 Command Line Interface

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
| `--algorithm` | Search algorithm | `bfs`, `dfs`, `a_star` |
| `--heuristic` | Heuristic function | `manhattan`, `none` |

### 📊 Performance Analysis

The automated test runner provides detailed performance analysis:
- **Execution time** for each algorithm
- **Solution length** (number of moves)
- **Space complexity** (nodes expanded)
- **Success rate** across different puzzle difficulties

```bash
python gui.py
```

Controls:
- `SPACE`: play/pause animation
- `→`: step one move
- `←`: switch to next puzzle

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
