# utils/validate.py

def is_solvable(state, size):
    """Check if a sliding puzzle is solvable."""
    inversion_count = 0
    tiles = [tile for tile in state if tile != 0]
    
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversion_count += 1

    if size % 2 == 1:
        return inversion_count % 2 == 0
    else:
        row = state.index(0) // size
        blank_row_from_bottom = size - row
        return (inversion_count + blank_row_from_bottom) % 2 == 0
