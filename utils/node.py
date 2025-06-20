# utils/node.py

class Node:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0):
        self.state = state          # List[int] - flattened puzzle state
        self.parent = parent        # Node or None
        self.action = action        # "L", "R", "U", "D" or None
        self.depth = depth          # For BFS/DFS
        self.cost = cost            # g(n) for A*

    def extract_path(self):
        """Backtrack from goal to start to get the move sequence."""
        path = []
        node = self
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return list(reversed(path))

    def __lt__(self, other):
        # Required for priority queue comparisons
        return (self.cost or 0) < (other.cost or 0)
