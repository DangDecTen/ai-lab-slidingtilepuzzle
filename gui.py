# gui.py
import pygame
import json
import os

# Config
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 60

BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)
TILE_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 40
MARGIN = 10

PUZZLE_AREA_WIDTH = 400
CONTROL_AREA_WIDTH = 400

def load_output_files():
    output_dir = os.path.join("data", "output")
    files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
    data = {}
    for f in files:
        with open(os.path.join(output_dir, f)) as file:
            data[f] = json.load(file)
    return data

def draw_tile(screen, font, num, x, y, w, h):
    pygame.draw.rect(screen, TILE_COLOR, (x, y, w, h))
    if num != 0:
        text = font.render(str(num), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(text, text_rect)

def draw_grid(screen, font, state, size):
    tile_w = PUZZLE_AREA_WIDTH // size
    tile_h = WINDOW_HEIGHT // size
    for i in range(size):
        for j in range(size):
            idx = i * size + j
            num = state[idx]
            x = j * tile_w
            y = i * tile_h
            draw_tile(screen, font, num, x, y, tile_w - MARGIN, tile_h - MARGIN)

def draw_info_panel(screen, font, info, start_x):
    lines = [
        f"Puzzle: {info.get('puzzle_name', '')}",
        f"Algorithm: {info.get('algorithm', '')}",
        f"Heuristic: {info.get('heuristic', 'None')}",
        f"Status: {info.get('status', '')}",
        f"Moves: {info.get('solution_length', 0)}",
        f"Time: {info.get('time_taken', 0):.4f}s",
        f"Space: {info.get('space_used', 0)}",
        f"Expanded: {info.get('nodes_expanded', 0)}"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (start_x + 10, 10 + i * (FONT_SIZE + 5)))

def apply_move(state, move, size):
    index = state.index(0)
    row, col = divmod(index, size)
    target = index
    if move == "L" and col > 0:
        target = index - 1
    elif move == "R" and col < size - 1:
        target = index + 1
    elif move == "U" and row > 0:
        target = index - size
    elif move == "D" and row < size - 1:
        target = index + size
    new_state = state.copy()
    new_state[index], new_state[target] = new_state[target], new_state[index]
    return new_state

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Tile Puzzle Viewer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)

    results = load_output_files()
    keys = list(results.keys())
    index = 0
    result = results[keys[index]]

    state = result['initial_state'][:]
    path = result['solution_path']
    size = result['size']

    step = 0
    playing = False
    play_speed = 5  # frames per move
    frame_counter = 0

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen, font, state, size)
        draw_info_panel(screen, font, result, PUZZLE_AREA_WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_RIGHT:
                    if step < len(path):
                        state = apply_move(state, path[step], size)
                        step += 1
                elif event.key == pygame.K_LEFT:
                    index = (index + 1) % len(keys)
                    result = results[keys[index]]
                    state = result['initial_state'][:]
                    path = result['solution_path']
                    size = result['size']
                    step = 0

        if playing and step < len(path):
            frame_counter += 1
            if frame_counter >= play_speed:
                state = apply_move(state, path[step], size)
                step += 1
                frame_counter = 0

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
