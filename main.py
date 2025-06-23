# main.py


""" Accepts CLI arguments:
python main.py --input data/input/example.json --algorithm bfs
python main.py --all --algorithm a_star --heuristic manhattan
"""


import json
import os
import argparse
import time

from utils.validate import is_solvable
from algorithms import bfs, dfs, a_star, ucs, ids, bi_bfs

ALGORITHMS = {
    "bfs": bfs.solve,
    "dfs": dfs.solve,
    "ids": ids.solve,
    "ucs": ucs.solve,
    "bi_bfs": bi_bfs.solve,
    "a_star": a_star.solve,
}

HEURISTICS = ["manhattan", None]

def load_input(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_output(output_path, data):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def run_solver(input_file, algorithm_name, heuristic):
    input_data = load_input(input_file)
    initial = input_data["initial_state"]
    goal = input_data["goal_state"]
    size = input_data["size"]
    name = input_data.get("name", os.path.basename(input_file))

    output = {
        "puzzle_name": name,
        "size": size,
        "initial_state": initial,
        "goal_state": goal,
        "algorithm": algorithm_name,
        "heuristic": heuristic if algorithm_name == "a_star" else None
    }

    if not is_solvable(initial, size):
        output.update({
            "status": "Unsolvable",
            "solution_path": [],
            "solution_length": 0,
            "time_taken": 0,
            "space_used": 0,
            "nodes_expanded": 0
        })
    else:
        solve_fn = ALGORITHMS[algorithm_name]
        result = solve_fn(initial, goal, size, heuristic)
        output.update(result)

    filename = os.path.splitext(os.path.basename(input_file))[0]
    suffix = f"_{algorithm_name}"
    if heuristic:
        suffix += f"_{heuristic}"
    os.makedirs(os.path.join("data", "output"), exist_ok=True)
    output_file = os.path.join("data", "output", f"{filename}{suffix}.json")
    save_output(output_file, output)
    print(f"Saved result to {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Path to input file')
    parser.add_argument('--all', action='store_true', help='Run on all input files')
    parser.add_argument('--algorithm', choices=ALGORITHMS.keys(), required=True)
    parser.add_argument('--heuristic', choices=["manhattan", "none"], default="none")
    args = parser.parse_args()

    heuristic = None if args.heuristic == "none" else args.heuristic

    if args.all:
        input_dir = os.path.join("data", "input")
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".json"):
                run_solver(os.path.join(input_dir, file_name), args.algorithm, heuristic)
    else:
        if not args.input:
            print("Please provide --input file or use --all")
            return
        run_solver(args.input, args.algorithm, heuristic)

if __name__ == '__main__':
    main()
