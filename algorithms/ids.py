from utils.node import Node
from utils.move import get_neighbors
import time
import itertools


PATH_FOUND, CUTOFF, FAILURE = 'Path found', 'cutoff', 'No path'


def is_in_path(node, state):
    while node:
        if node.state == state:
            return True
        node = node.parent
    return False


def iterative_dls(initial_state, goal_state, size, depth_limit):
    frontier = [Node(initial_state)]
    nodes_expanded = 0
    cutoff_occurred = False

    while frontier:
        node = frontier.pop()

        if node.state == goal_state:
            return {
                "found": PATH_FOUND,
                "node": node,
                "nodes_expanded": nodes_expanded
            }
        
        if node.depth >= depth_limit:
            cutoff_occurred = True
            continue
        
        nodes_expanded += 1
        
        for action, new_state in reversed(get_neighbors(node.state, size)):
            if not is_in_path(node, new_state):  # Check cycle
                frontier.append(Node(new_state, parent=node, action=action, depth=node.depth + 1))

    return {
        "found": CUTOFF if cutoff_occurred else FAILURE,
        "nodes_expanded": nodes_expanded
    }


def solve(initial_state, goal_state, size, heuristic=None):
    start_time = time.perf_counter()
    nodes_expanded_total = 0

    for depth_limit in itertools.count(0):
        result = iterative_dls(initial_state, goal_state, size, depth_limit)

        nodes_expanded_total += result["nodes_expanded"]

        if result["found"] is not CUTOFF:
            path = [] if result["found"] is FAILURE else result["node"].extract_path()
            return {
                "status": result["found"],
                "solution_path": path,
                "solution_length": len(path),
                "time_taken": round(time.perf_counter() - start_time, 6),
                "space_used": depth_limit,
                "nodes_expanded": nodes_expanded_total
            }
