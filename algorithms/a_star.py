# algorithms/a_star.py
from utils.node import Node
from utils.move import get_neighbors
from utils.priority_queue import PriorityQueue
import time

def manhattan_distance(state, goal_state, size):
    distance = 0
    for num in range(1, size * size):
        curr_index = state.index(num)
        goal_index = goal_state.index(num)
        curr_x, curr_y = divmod(curr_index, size)
        goal_x, goal_y = divmod(goal_index, size)
        distance += abs(curr_x - goal_x) + abs(curr_y - goal_y)
    return distance

def solve(initial_state, goal_state, size, heuristic='Manhattan'):
    start_time = time.perf_counter()
    visited = set()
    pq = PriorityQueue()

    h = manhattan_distance(initial_state, goal_state, size)
    root = Node(initial_state, cost=h)
    pq.put(root, h)
    visited.add(tuple(initial_state))

    max_frontier_size = 1
    nodes_expanded = 0

    while not pq.empty():
        node = pq.get()
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

        for action, new_state in get_neighbors(node.state, size):
            new_tuple = tuple(new_state)
            if new_tuple not in visited:
                visited.add(new_tuple)
                g = node.cost + 1
                h = manhattan_distance(new_state, goal_state, size)
                pq.put(Node(new_state, parent=node, action=action, cost=g), g + h)

        max_frontier_size = max(max_frontier_size, len(visited) + len(pq.elements))

    return {
        "status": "No path",
        "solution_path": [],
        "solution_length": 0,
        "time_taken": round(time.perf_counter() - start_time, 6),
        "space_used": max_frontier_size,
        "nodes_expanded": nodes_expanded
    }