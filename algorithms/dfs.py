# algorithms/dfs.py
from utils.node import Node
from utils.move import get_neighbors
import time

def solve(initial_state, goal_state, size, heuristic=None):
    start_time = time.perf_counter()
    visited = set()
    frontier = [Node(initial_state)]
    visited.add(tuple(initial_state))

    max_frontier_size = 1
    nodes_expanded = 0

    while frontier:
        node = frontier.pop()
        nodes_expanded += 1

        if node.state == goal_state:
            return {
                "status": "Path found",
                "solution_path": node.extract_path(),
                "solution_length": len(node.extract_path()),
                "time_taken": round(time.perf_counter() - start_time, 6),
                "space_used": max(max_frontier_size, len(visited)),
                "nodes_expanded": nodes_expanded
            }

        for action, new_state in reversed(get_neighbors(node.state, size)):
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                frontier.append(Node(new_state, parent=node, action=action, depth=node.depth+1))

        max_frontier_size = max(max_frontier_size, len(frontier) + len(visited))

    return {
        "status": "No path",
        "solution_path": [],
        "solution_length": 0,
        "time_taken": round(time.perf_counter() - start_time, 6),
        "space_used": max_frontier_size,
        "nodes_expanded": nodes_expanded
    }