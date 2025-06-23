"""
Statistics and Info Panels
"""
import pygame
from .constants import *


class StatisticsPanel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw_statistics(self, screen, solution_data):
        """Draw statistics in a modern card layout"""
        x, y = self.x, self.y
        
        # Draw statistics card
        stats_rect = pygame.Rect(x - 10, y - 10, 350, 250)
        shadow_stats = stats_rect.copy()
        shadow_stats.x += 2
        shadow_stats.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_stats, border_radius=10)
        pygame.draw.rect(screen, CARD_BACKGROUND, stats_rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, stats_rect, 2, border_radius=10)
        
        # Title
        title_text = FONT_LARGE.render("Statistics", True, TEXT_PRIMARY)
        screen.blit(title_text, (x, y))
        y += 35
        
        if not solution_data:
            text = FONT_MEDIUM.render("No solution loaded", True, TEXT_SECONDARY)
            screen.blit(text, (x, y))
            return
        
        # Statistics data
        stats = [
            ("Puzzle", solution_data.get('puzzle_name', 'Unknown')),
            ("Algorithm", solution_data.get('algorithm', 'Unknown')),
            ("Heuristic", solution_data.get('heuristic') or 'None'),
            ("Status", solution_data.get('status', 'Unknown')),
            ("Solution Length", str(solution_data.get('solution_length', 0))),
            ("Time Taken", f"{solution_data.get('time_taken', 0):.4f}s"),
            ("Space Used", str(solution_data.get('space_used', 0))),
            ("Nodes Expanded", str(solution_data.get('nodes_expanded', 0)))
        ]
        
        for i, (label, value) in enumerate(stats):
            # Label
            label_text = FONT_SMALL.render(f"{label}:", True, TEXT_SECONDARY)
            screen.blit(label_text, (x, y + i * 22))
            
            # Value
            value_text = FONT_SMALL.render(str(value), True, TEXT_PRIMARY)
            screen.blit(value_text, (x + 120, y + i * 22))


class MoveListPanel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw_move_list(self, screen, solution_path, current_step, current_move_highlight, show_move_list=True):
        """Draw the list of moves being executed"""
        if not solution_path or not show_move_list:
            return
        
        # Draw container
        list_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        shadow_list = list_rect.copy()
        shadow_list.x += 2
        shadow_list.y += 2        
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_list, border_radius=10)
        pygame.draw.rect(screen, CARD_BACKGROUND, list_rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, list_rect, 2, border_radius=10)
        
        # Title
        title_text = FONT_MEDIUM.render("Solution Steps", True, TEXT_PRIMARY)
        screen.blit(title_text, (self.x + 10, self.y + 10))
        
        # Scrollable move list
        moves_start_y = self.y + 40
        visible_moves = (self.height - 50) // 25
        
        # Calculate scroll offset to keep current move visible
        scroll_offset = max(0, current_step - visible_moves + 3)
        
        for i, move in enumerate(solution_path):
            if i < scroll_offset or i >= scroll_offset + visible_moves:
                continue
                
            move_y = moves_start_y + (i - scroll_offset) * 25
            
            # Highlight current move
            if i == current_step - 1 and current_move_highlight is not None:
                highlight_rect = pygame.Rect(self.x + 5, move_y - 2, self.width - 10, 24)
                pygame.draw.rect(screen, (255, 235, 59, 100), highlight_rect, border_radius=5)
            
            # Move status
            if i < current_step:
                status_color = SUCCESS
                status_text = "✓"
            elif i == current_step:
                status_color = WARNING
                status_text = "→"
            else:
                status_color = TEXT_SECONDARY
                status_text = " "
            
            # Draw move
            step_text = f"{i+1:2d}. {move}"
            step_surf = FONT_SMALL.render(step_text, True, TEXT_PRIMARY)
            screen.blit(step_surf, (self.x + 25, move_y))
            
            # Draw status
            status_surf = FONT_SMALL.render(status_text, True, status_color)
            screen.blit(status_surf, (self.x + 10, move_y))


class ProgressPanel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
