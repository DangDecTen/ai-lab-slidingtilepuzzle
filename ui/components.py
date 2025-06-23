"""
Modern UI Components for Puzzle GUI
"""
import pygame
from .constants import *


class ModernButton:
    def __init__(self, x, y, width, height, text, color=PRIMARY, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = self._get_hover_color(color)
        self.text_color = text_color
        self.font = FONT_MEDIUM
        self.hovered = False
        self.pressed = False
        self.border_radius = 8
        
    def _get_hover_color(self, color):
        if color == PRIMARY:
            return PRIMARY_HOVER
        elif color == SUCCESS:
            return SUCCESS_HOVER
        elif color == WARNING:
            return WARNING_HOVER
        elif color == DANGER:
            return DANGER_HOVER
        else:
            # Darken any other color by 20%
            return tuple(max(0, int(c * 0.8)) for c in color)
    
    def draw(self, screen):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=self.border_radius)
        
        # Draw button
        current_color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        return False


class ModernSlider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.dragging = False
        
    def draw(self, screen):
        # Draw slider track
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - 3, self.rect.width, 6)
        pygame.draw.rect(screen, BORDER, track_rect, border_radius=3)
        
        # Draw filled portion
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        filled_width = ratio * self.rect.width
        filled_rect = pygame.Rect(self.rect.x, self.rect.centery - 3, filled_width, 6)
        pygame.draw.rect(screen, PRIMARY, filled_rect, border_radius=3)
        
        # Calculate handle position
        handle_x = self.rect.x + ratio * self.rect.width
        handle_center = (int(handle_x), self.rect.centery)
        
        # Draw handle shadow
        pygame.draw.circle(screen, (0, 0, 0, 50), (handle_center[0] + 1, handle_center[1] + 1), 10)
        # Draw handle
        pygame.draw.circle(screen, CARD_BACKGROUND, handle_center, 10)
        pygame.draw.circle(screen, PRIMARY, handle_center, 8)
        pygame.draw.circle(screen, BORDER, handle_center, 10, 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = event.pos[0] - self.rect.x
            relative_x = max(0, min(self.rect.width, relative_x))
            ratio = relative_x / self.rect.width
            self.val = self.min_val + ratio * (self.max_val - self.min_val)
    
    def get_value(self):
        return self.val
