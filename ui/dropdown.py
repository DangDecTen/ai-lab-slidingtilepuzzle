"""
Modern Scrollable Dropdown Component
"""
import pygame
from .constants import *


class ModernScrollableDropdown:
    def __init__(self, x, y, width, height, options, default=0, max_visible=8):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = default
        self.max_visible = max_visible  # Maximum items to show before scrolling
        self.font = FONT_MEDIUM
        self.open = False
        self.scroll_offset = 0
        self.hovered_option = -1
        self.border_radius = 8
        
        # Calculate dropdown height based on visible items
        self.dropdown_height = min(len(options), max_visible) * height
        self.dropdown_rect = pygame.Rect(x, y + height, width, self.dropdown_height)
        
        # Scrollbar properties
        self.scrollbar_width = 15
        self.scrollbar_rect = pygame.Rect(
            x + width - self.scrollbar_width, 
            y + height, 
            self.scrollbar_width, 
            self.dropdown_height
        )
        self.scrollbar_thumb_height = max(20, (self.dropdown_height * max_visible) // len(options)) if len(options) > max_visible else 0
        self.dragging_scrollbar = False
    
    def get_visible_options(self):
        """Get the options that should be visible based on scroll offset"""
        end_idx = min(len(self.options), self.scroll_offset + self.max_visible)
        return self.options[self.scroll_offset:end_idx]
    
    def scroll_to_selected(self):
        """Scroll to make selected item visible"""
        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        elif self.selected >= self.scroll_offset + self.max_visible:
            self.scroll_offset = self.selected - self.max_visible + 1
        
        # Clamp scroll offset
        max_scroll = max(0, len(self.options) - self.max_visible)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
    
    def draw(self, screen):
        # Draw main dropdown box with shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=self.border_radius)
        
        pygame.draw.rect(screen, CARD_BACKGROUND, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, BORDER, self.rect, 2, border_radius=self.border_radius)
        
        # Draw selected option text (truncated if too long)
        if self.selected < len(self.options):
            text = self.options[self.selected]
            # Truncate text if too long
            max_chars = (self.rect.width - 40) // 7  # Rough character width estimation
            if len(text) > max_chars:
                text = text[:max_chars-3] + "..."
            
            text_surf = self.font.render(text, True, TEXT_PRIMARY)
            text_rect = text_surf.get_rect(center=(self.rect.centerx - 10, self.rect.centery))
            screen.blit(text_surf, text_rect)
        
        # Draw modern arrow
        arrow_x = self.rect.right - 25
        arrow_y = self.rect.centery
        arrow_points = [
            (arrow_x, arrow_y - 4),
            (arrow_x + 8, arrow_y - 4),
            (arrow_x + 4, arrow_y + 4)
        ]
        pygame.draw.polygon(screen, TEXT_SECONDARY, arrow_points)
        
        # Draw options if open
        if self.open:
            self._draw_dropdown_list(screen)
    
    def _draw_dropdown_list(self, screen):
        """Draw the dropdown list when open"""
        # Draw dropdown shadow
        shadow_dropdown = self.dropdown_rect.copy()
        shadow_dropdown.x += 2
        shadow_dropdown.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_dropdown, border_radius=self.border_radius)
        
        # Draw dropdown background
        pygame.draw.rect(screen, CARD_BACKGROUND, self.dropdown_rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, BORDER, self.dropdown_rect, 2, border_radius=self.border_radius)
        
        # Draw visible options
        visible_options = self.get_visible_options()
        for i, option in enumerate(visible_options):
            actual_index = i + self.scroll_offset
            option_rect = pygame.Rect(
                self.dropdown_rect.x, 
                self.dropdown_rect.y + i * self.rect.height,
                self.dropdown_rect.width - (self.scrollbar_width if len(self.options) > self.max_visible else 0),
                self.rect.height
            )
            
            # Highlight hovered option
            if actual_index == self.hovered_option:
                pygame.draw.rect(screen, (59, 130, 246, 50), option_rect)
            # Highlight selected option
            elif actual_index == self.selected:
                pygame.draw.rect(screen, (34, 197, 94, 30), option_rect)
            
            # Truncate option text if too long
            text = option
            max_chars = (option_rect.width - 20) // 7
            if len(text) > max_chars:
                text = text[:max_chars-3] + "..."
            
            text_surf = self.font.render(text, True, TEXT_PRIMARY)
            text_rect = text_surf.get_rect(center=option_rect.center)
            screen.blit(text_surf, text_rect)
        
        # Draw scrollbar if needed
        if len(self.options) > self.max_visible:
            self._draw_scrollbar(screen)
    
    def _draw_scrollbar(self, screen):
        """Draw scrollbar for long lists"""
        # Scrollbar track
        pygame.draw.rect(screen, (200, 200, 200), self.scrollbar_rect, border_radius=4)
        
        # Scrollbar thumb
        thumb_y_ratio = self.scroll_offset / max(1, len(self.options) - self.max_visible)
        thumb_y = self.scrollbar_rect.y + thumb_y_ratio * (self.dropdown_height - self.scrollbar_thumb_height)
        thumb_rect = pygame.Rect(
            self.scrollbar_rect.x + 2,
            thumb_y,
            self.scrollbar_width - 4,
            self.scrollbar_thumb_height
        )
        pygame.draw.rect(screen, (120, 120, 120), thumb_rect, border_radius=4)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.open:
                self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEWHEEL and self.open:
            self._handle_mouse_wheel(event)
        
        return False
    
    def _handle_mouse_motion(self, event):
        """Handle mouse motion when dropdown is open"""
        self.hovered_option = -1
        # Check if hovering over visible options
        for i in range(len(self.get_visible_options())):
            option_rect = pygame.Rect(
                self.dropdown_rect.x,
                self.dropdown_rect.y + i * self.rect.height,
                self.dropdown_rect.width - (self.scrollbar_width if len(self.options) > self.max_visible else 0),
                self.rect.height
            )
            if option_rect.collidepoint(event.pos):
                self.hovered_option = i + self.scroll_offset
                break
        
        # Handle scrollbar dragging
        if self.dragging_scrollbar and len(self.options) > self.max_visible:
            relative_y = event.pos[1] - self.scrollbar_rect.y
            scroll_ratio = relative_y / self.dropdown_height
            max_scroll = len(self.options) - self.max_visible
            self.scroll_offset = max(0, min(max_scroll, int(scroll_ratio * max_scroll)))
    
    def _handle_mouse_down(self, event):
        """Handle mouse button down events"""
        if self.rect.collidepoint(event.pos):
            self.open = not self.open
            if self.open:
                self.scroll_to_selected()
            return True
        elif self.open:
            # Check scrollbar click
            if len(self.options) > self.max_visible and self.scrollbar_rect.collidepoint(event.pos):
                self.dragging_scrollbar = True
                return True
            
            # Check option click
            for i in range(len(self.get_visible_options())):
                option_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + i * self.rect.height,
                    self.dropdown_rect.width - (self.scrollbar_width if len(self.options) > self.max_visible else 0),
                    self.rect.height
                )
                if option_rect.collidepoint(event.pos):
                    self.selected = i + self.scroll_offset
                    self.open = False
                    return True
            
            # Click outside - close dropdown
            self.open = False
        
        return False
    
    def _handle_mouse_wheel(self, event):
        """Handle mouse wheel scrolling"""
        if len(self.options) > self.max_visible:
            self.scroll_offset = max(0, min(
                len(self.options) - self.max_visible,
                self.scroll_offset - event.y
            ))
    
    def get_selected(self):
        if self.selected < len(self.options):
            return self.options[self.selected]
        return None
