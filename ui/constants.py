"""
UI Constants and Theme Configuration
"""
import pygame

# Initialize Pygame fonts
pygame.font.init()

# Window Configuration
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 950
FPS = 60

# Modern Color Palette
BACKGROUND = (245, 247, 250)
CARD_BACKGROUND = (255, 255, 255)
PRIMARY = (59, 130, 246)  # Blue
PRIMARY_HOVER = (37, 99, 235)
SUCCESS = (34, 197, 94)  # Green
SUCCESS_HOVER = (22, 163, 74)
WARNING = (251, 191, 36)  # Yellow
WARNING_HOVER = (245, 158, 11)
DANGER = (239, 68, 68)  # Red
DANGER_HOVER = (220, 38, 38)
TEXT_PRIMARY = (31, 41, 55)
TEXT_SECONDARY = (107, 114, 128)
BORDER = (229, 231, 235)
SHADOW = (0, 0, 0, 30)

# Tile Colors
TILE_COLORS = {
    0: (75, 85, 99),  # Empty space - dark gray
    'default': (219, 234, 254),  # Light blue
    'number': (30, 64, 175)  # Dark blue for numbers
}

# Fonts
FONT_LARGE = pygame.font.Font(None, 32)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 18)
FONT_TILE = pygame.font.Font(None, 36)

# UI Layout
PUZZLE_AREA = pygame.Rect(50, 50, 550, 550)
CONTROL_AREA = pygame.Rect(650, 50, 800, 850)
