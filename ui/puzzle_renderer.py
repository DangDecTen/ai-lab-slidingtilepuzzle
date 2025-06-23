"""
Puzzle Rendering Component
"""
import pygame
from .constants import *


class PuzzleRenderer:
    def __init__(self, puzzle_area):
        self.puzzle_area = puzzle_area
    
    def draw_puzzle(self, screen, current_state, goal_state, puzzle_size, solution_path=None, current_step=0, is_auto_solving=False):
        """Draw the puzzle grid with tiles"""
        if not current_state:
            return
        
        # Draw puzzle container with success indicator
        container_rect = self.puzzle_area.copy()
        container_rect.inflate_ip(20, 20)
        
        # Check if puzzle is solved
        is_solved = current_state == goal_state if goal_state else False
        
        # Draw shadow
        shadow_rect = container_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=15)
        
        # Draw container with success color if solved
        container_color = (220, 252, 231) if is_solved else CARD_BACKGROUND
        border_color = SUCCESS if is_solved else BORDER
        
        pygame.draw.rect(screen, container_color, container_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, container_rect, 3 if is_solved else 2, border_radius=15)
        
        # Add "SOLVED!" text if completed
        if is_solved:            
            solved_text = FONT_LARGE.render("SOLVED!", True, SUCCESS)
            text_rect = solved_text.get_rect(center=(container_rect.centerx, container_rect.y - 15))
            screen.blit(solved_text, text_rect)
        
        # Draw tiles
        start_x, start_y, tile_size, spacing = self._calculate_tile_layout(puzzle_size)
        
        for i, value in enumerate(current_state):
            row = i // puzzle_size
            col = i % puzzle_size
            
            x = start_x + col * (tile_size + spacing)
            y = start_y + row * (tile_size + spacing)
            
            tile_rect = pygame.Rect(x, y, tile_size, tile_size)
            
            if value == 0:
                self._draw_empty_tile(screen, tile_rect)
            else:
                self._draw_numbered_tile(screen, tile_rect, value, tile_size)
        
        # Draw current move indicator
        if is_auto_solving and solution_path and current_step > 0:
            self._draw_move_indicator(screen, current_state, solution_path, current_step, 
                                    puzzle_size, start_x, start_y, tile_size, spacing)
    
    def _calculate_tile_layout(self, puzzle_size):
        """Calculate tile positions and sizes"""
        available_width = self.puzzle_area.width - 40
        available_height = self.puzzle_area.height - 40
        spacing = 12
        
        tile_size = min(
            (available_width - (puzzle_size - 1) * spacing) // puzzle_size,
            (available_height - (puzzle_size - 1) * spacing) // puzzle_size
        )
        
        # Center the puzzle grid
        total_width = puzzle_size * tile_size + (puzzle_size - 1) * spacing
        total_height = puzzle_size * tile_size + (puzzle_size - 1) * spacing
        start_x = self.puzzle_area.x + (self.puzzle_area.width - total_width) // 2
        start_y = self.puzzle_area.y + (self.puzzle_area.height - total_height) // 2
        
        return start_x, start_y, tile_size, spacing
    
    def _draw_empty_tile(self, screen, tile_rect):
        """Draw empty space tile"""
        pygame.draw.rect(screen, (200, 200, 200), tile_rect, border_radius=12)
        pygame.draw.rect(screen, (150, 150, 150), tile_rect, 3, border_radius=12)
        
        # Add subtle pattern to show it's empty
        for dash_y in range(tile_rect.y + 10, tile_rect.bottom - 10, 15):
            for dash_x in range(tile_rect.x + 10, tile_rect.right - 10, 15):
                pygame.draw.circle(screen, (180, 180, 180), (dash_x, dash_y), 2)
    
    def _draw_numbered_tile(self, screen, tile_rect, value, tile_size):
        """Draw numbered tile"""
        # Draw enhanced tile shadow
        shadow_tile = tile_rect.copy()
        shadow_tile.x += 3
        shadow_tile.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 60), shadow_tile, border_radius=12)
        
        # Draw tile with gradient effect
        pygame.draw.rect(screen, TILE_COLORS['default'], tile_rect, border_radius=12)
        
        # Add subtle inner highlight
        highlight_rect = tile_rect.copy()
        highlight_rect.inflate(-4, -4)
        pygame.draw.rect(screen, (240, 248, 255), highlight_rect, 2, border_radius=10)
        
        # Draw border
        pygame.draw.rect(screen, BORDER, tile_rect, 3, border_radius=12)
        
        # Draw number with better font sizing
        font_size = max(24, tile_size // 3)
        number_font = pygame.font.Font(None, font_size)
        text = number_font.render(str(value), True, TILE_COLORS['number'])
        text_rect = text.get_rect(center=tile_rect.center)
        screen.blit(text, text_rect)
    
    def _draw_move_indicator(self, screen, current_state, solution_path, current_step, 
                           puzzle_size, start_x, start_y, tile_size, spacing):
        """Draw arrow indicating current move"""
        if current_step <= len(solution_path):
            current_move = solution_path[current_step - 1] if current_step > 0 else None
            if current_move:
                # Find empty space position
                empty_pos = current_state.index(0)
                empty_row = empty_pos // puzzle_size
                empty_col = empty_pos % puzzle_size
                
                # Calculate empty space screen position
                empty_x = start_x + empty_col * (tile_size + spacing) + tile_size // 2
                empty_y = start_y + empty_row * (tile_size + spacing) + tile_size // 2
                
                # Draw move direction arrow
                arrow_size = 20
                arrow_color = (255, 100, 100)  # Red arrow
                
                points = self._get_arrow_points(current_move, empty_x, empty_y, arrow_size)
                if points:
                    pygame.draw.polygon(screen, arrow_color, points)
                    
                    # Draw move text
                    move_text = FONT_SMALL.render(f"Move: {current_move}", True, arrow_color)
                    text_rect = move_text.get_rect(center=(empty_x, empty_y + 40))
                    screen.blit(move_text, text_rect)
    
    def _get_arrow_points(self, move_direction, x, y, size):
        """Get arrow points for move direction"""
        if move_direction == "U":
            return [(x, y - size), (x - size//2, y), (x + size//2, y)]
        elif move_direction == "D":
            return [(x, y + size), (x - size//2, y), (x + size//2, y)]
        elif move_direction == "L":
            return [(x - size, y), (x, y - size//2), (x, y + size//2)]
        elif move_direction == "R":
            return [(x + size, y), (x, y - size//2), (x, y + size//2)]
        return None
