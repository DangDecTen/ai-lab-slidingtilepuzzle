# algorithms/bfs.py
from utils.node import Node
from utils.move import get_neighbors
import time


def reverse_path_moves(path):
    translate_table = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
    return [translate_table[move] for move in path]


def join_path(meeting_state, frontier_f, frontier_b):
    node_f = next((node for node in frontier_f if node.state == meeting_state))
    path_f = node_f.extract_path()

    node_b = next((node for node in frontier_b if node.state == meeting_state))
    path_b = node_b.extract_path()
    reversed_path_b = path_b[::-1]
    reversed_moves_path_b = reverse_path_moves(reversed_path_b)

    path_f.extend(reversed_moves_path_b)
    return path_f


def bi_search_proceed(current_node, size, frontier, visited, opposite_visited):
    for action, new_state in get_neighbors(current_node.state, size):
        if tuple(new_state) not in visited:
            child_node = Node(new_state, parent=current_node, action=action, depth=current_node.depth+1)
            visited.add(tuple(new_state))
            frontier.append(child_node)
            
            # Check meeting state
            if tuple(new_state) in opposite_visited:
                return new_state
    return None


def solve(initial_state, goal_state, size, heuristic=None):
    start_time = time.perf_counter()
    visited_f = set()
    visited_b = set()
    frontier_f = [Node(initial_state)]
    frontier_b = [Node(goal_state)]
    visited_f.add(tuple(initial_state))
    visited_b.add(tuple(goal_state))
    nodes_expanded = 0

    if initial_state == goal_state:
        return {
            "status": "Path found",
            "solution_path": [],
            "solution_length": 0,
            "time_taken": round(time.perf_counter() - start_time, 6),
            "space_used": len(visited_f) + len(visited_b),
            "nodes_expanded": nodes_expanded
        }

    meeting_state = None
    while meeting_state is None:
        if (not frontier_f) or (not frontier_b):
            break

        if frontier_f[0].depth > frontier_b[0].depth:
            node = frontier_b.pop(0)
            meeting_state = bi_search_proceed(node, size, frontier_b, visited_b, visited_f)
        else:
            node = frontier_f.pop(0)
            meeting_state = bi_search_proceed(node, size, frontier_f, visited_f, visited_b)

        nodes_expanded += 1

    if meeting_state is not None:
        path = join_path(meeting_state, frontier_f, frontier_b)
        return {
            "status": "Path found",
            "solution_path": path,
            "solution_length": len(path),
            "time_taken": round(time.perf_counter() - start_time, 6),
            "space_used": len(visited_f) + len(visited_b),
            "nodes_expanded": nodes_expanded
        }
    
    return {
        "status": "No path",
        "solution_path": [],
        "solution_length": 0,
        "time_taken": round(time.perf_counter() - start_time, 6),
        "space_used": len(visited_f) + len(visited_b),
        "nodes_expanded": nodes_expanded
    }