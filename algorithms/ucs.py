# algorithms/ucs.py
from utils.node import Node
from utils.move import get_neighbors
from utils.priority_queue import PriorityQueue
import time

def solve(initial_state, goal_state, size, heuristic=None):
    start_time = time.perf_counter()
    visited = set()
    frontier = PriorityQueue()

    visited.add(tuple(initial_state))
    frontier.add(Node(initial_state), 0)
    nodes_expanded = 0

    while frontier:
        node, node_f_cost = frontier.pop()
        nodes_expanded += 1

        if node.state == goal_state:
            return {
                "status": "Path found",
                "solution_path": node.extract_path(),
                "solution_length": len(node.extract_path()),
                "time_taken": round(time.perf_counter() - start_time, 6),
                "space_used": len(visited),
                "nodes_expanded": nodes_expanded
            }  

        for action, new_state in get_neighbors(node.state, size):
            child_f_cost = node_f_cost + 1
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                frontier.add(Node(new_state, parent=node, action=action, depth=node.depth+1), child_f_cost)
            elif tuple(new_state) in frontier and child_f_cost + 1 < frontier.get_priority(tuple(new_state)):
                # Replace old node with new node that hold the same state
                frontier.add(Node(new_state, parent=node, action=action, depth=node.depth+1), child_f_cost)

    return {
        "status": "No path",
        "solution_path": [],
        "solution_length": 0,
        "time_taken": round(time.perf_counter() - start_time, 6),
        "space_used": len(visited),
        "nodes_expanded": nodes_expanded
    }