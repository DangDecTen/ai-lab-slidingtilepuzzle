# algorithms/bfs.py
from utils.node import Node
from utils.move import get_neighbors
import time

def solve(initial_state, goal_state, size, heuristic=None):
    start_time = time.perf_counter()
    visited = set()
    frontier = [Node(initial_state)]
    visited.add(tuple(initial_state))
    nodes_expanded = 0

    if initial_state == goal_state:
        return {
            "status": "Path found",
            "solution_path": [],
            "solution_length": 0,
            "time_taken": round(time.perf_counter() - start_time, 6),
            "space_used": len(visited),
            "nodes_expanded": nodes_expanded
        }

    while frontier:
        node = frontier.pop(0)
        nodes_expanded += 1        

        for action, new_state in get_neighbors(node.state, size):
            if tuple(new_state) not in visited:
                child_node = Node(new_state, parent=node, action=action, depth=node.depth+1)
                visited.add(tuple(new_state))

                if new_state == goal_state:
                    return {
                        "status": "Path found",
                        "solution_path": child_node.extract_path(),
                        "solution_length": len(child_node.extract_path()),
                        "time_taken": round(time.perf_counter() - start_time, 6),
                        "space_used": len(visited),
                        "nodes_expanded": nodes_expanded
                    }

                frontier.append(child_node)

    return {
        "status": "No path",
        "solution_path": [],
        "solution_length": 0,
        "time_taken": round(time.perf_counter() - start_time, 6),
        "space_used": len(visited),
        "nodes_expanded": nodes_expanded
    }