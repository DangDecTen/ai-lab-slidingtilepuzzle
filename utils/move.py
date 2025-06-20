# utils/move.py

def get_neighbors(state, size):
    """Return list of (action, new_state) pairs reachable from the current state."""
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, size)

    def swap(index1, index2):
        new_state = state.copy()
        new_state[index1], new_state[index2] = new_state[index2], new_state[index1]
        return new_state

    if col > 0:  # Move left
        neighbors.append(("L", swap(zero_index, zero_index - 1)))
    if col < size - 1:  # Move right
        neighbors.append(("R", swap(zero_index, zero_index + 1)))
    if row > 0:  # Move up
        neighbors.append(("U", swap(zero_index, zero_index - size)))
    if row < size - 1:  # Move down
        neighbors.append(("D", swap(zero_index, zero_index + size)))

    return neighbors
