import pygame
import json
import os
import sys
import time
import threading
import math
from main import run_solver, ALGORITHMS, HEURISTICS

# Add the current directory to the path so we can import our modules
sys.path.append('.')

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1500  # Wider window for better layout
WINDOW_HEIGHT = 950  # Taller for better spacing
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
TILE_COLORS = {
    0: (75, 85, 99),  # Empty space - dark gray
    'default': (219, 234, 254),  # Light blue
    'number': (30, 64, 175)  # Dark blue for numbers
}
SHADOW = (0, 0, 0, 30)

# Fonts
pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 32)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 18)
FONT_TILE = pygame.font.Font(None, 36)

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
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False
        
        elif event.type == pygame.MOUSEWHEEL and self.open:
            # Handle mouse wheel scrolling
            if len(self.options) > self.max_visible:
                self.scroll_offset = max(0, min(
                    len(self.options) - self.max_visible,
                    self.scroll_offset - event.y
                ))
        
        return False
    
    def get_selected(self):
        if self.selected < len(self.options):
            return self.options[self.selected]
        return None

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

class ModernPuzzleGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Puzzle Solver - Modern Interface")
        self.clock = pygame.time.Clock()
        
        # Application state
        self.input_files = self.load_input_files()
        self.current_input_file = None
        self.current_algorithm = "bfs"
        self.current_heuristic = "None"
        
        # Puzzle state
        self.initial_state = []
        self.current_state = []
        self.goal_state = []
        self.puzzle_size = 3
        
        # Solution state        
        self.solution_path = []
        self.solution_data = None
        self.current_step = 0
        self.is_auto_solving = False
        self.is_paused = False
        self.animation_speed = 2.0
        self.last_move_time = 0
        self.solving = False
        
        # Enhanced move visualization
        self.move_history = []
        self.current_move_highlight = None
        self.show_move_list = True
        
        # Layout - improved spacing
        self.puzzle_area = pygame.Rect(50, 50, 550, 550)
        self.control_area = pygame.Rect(650, 50, 800, 850)
          # UI Elements
        self.create_ui_elements()
        
        # Load first puzzle if available
        if self.input_files:
            self.load_puzzle(self.input_files[0])
    
    def load_input_files(self):
        """Load all available input files"""
        input_dir = os.path.join("data", "input")
        if not os.path.exists(input_dir):
            return []
        return sorted([f for f in os.listdir(input_dir) if f.endswith(".json")])
    
    def create_ui_elements(self):
        """Create all UI elements with modern design"""
        x = self.control_area.x + 20
        y = self.control_area.y + 20
        
        # Input file dropdown with scrolling
        self.input_dropdown = ModernScrollableDropdown(
            x, y + 40, 300, 40,
            self.input_files if self.input_files else ["No files"],
            max_visible=6  # Show max 6 items at once
        )
        y += 120
        
        # Algorithm dropdown
        self.algorithm_dropdown = ModernScrollableDropdown(
            x, y + 40, 300, 40,
            list(ALGORITHMS.keys()),
            max_visible=8
        )
        y += 120
        
        # Heuristic dropdown
        self.heuristic_dropdown = ModernScrollableDropdown(
            x, y + 40, 300, 40,
            ["None", "manhattan"],
            max_visible=4
        )
        y += 120
        
        # Control buttons with better spacing
        button_y = y + 20
        button_width = 90
        button_spacing = 10
        
        self.solve_button = ModernButton(x, button_y, button_width, 50, "Solve", SUCCESS)
        self.reset_button = ModernButton(x + button_width + button_spacing, button_y, button_width, 50, "Reset", DANGER)
        self.pause_button = ModernButton(x + 2*(button_width + button_spacing), button_y, button_width, 50, "Pause", WARNING)
        self.step_button = ModernButton(x + 3*(button_width + button_spacing), button_y, button_width, 50, "Step", PRIMARY)
        
        y += 100
        
        # Speed slider with proper positioning
        self.speed_slider_y = y + 40  # Store position for label
        self.speed_slider = ModernSlider(x, self.speed_slider_y, 300, 30, 0.5, 5.0, 2.0)
        
        # Update other positions to accommodate speed slider
        self.stats_y = y + 120
        self.progress_y = y + 420
    
    def load_puzzle(self, filename):
        """Load a puzzle from input file"""
        if not filename:
            return
            
        input_path = os.path.join("data", "input", filename)
        try:
            with open(input_path, 'r') as f:
                data = json.load(f)
            
            self.initial_state = data["initial_state"][:]
            self.current_state = data["initial_state"][:]
            self.goal_state = data["goal_state"]
            self.puzzle_size = data["size"]
            self.current_input_file = filename
            self.solution_path = []
            self.current_step = 0
            self.solution_data = None
            
            # Reset UI state
            self.is_auto_solving = False
            self.solving = False
            self.move_history = []
            self.current_move_highlight = None
            
        except Exception as e:
            print(f"Error loading puzzle: {e}")
    
    def solve_puzzle(self):
        """Solve the current puzzle and automatically start animation"""
        if self.solving or not self.current_input_file:
            return
        
        # Stop any current animation
        self.is_auto_solving = False
        self.solving = True
        self.solve_button.text = "Solving..."
        
        def solve_thread():
            try:
                input_file = self.current_input_file
                algorithm = self.current_algorithm
                heuristic = self.current_heuristic if self.current_heuristic != "None" else None
                
                print(f"=== STARTING SOLVER ===")
                print(f"Input file: {input_file}")
                print(f"Algorithm: {algorithm}")
                print(f"Heuristic: {heuristic}")
                
                # Run solver (it saves to output but returns None)
                input_path = f"data/input/{input_file}"
                print("Calling run_solver...")
                run_solver(input_path, algorithm, heuristic)
                print("run_solver completed")
                
                # Construct output filename based on your run_solver pattern:
                # filename = input file without .json
                # suffix = based on algorithm and heuristic
                filename = input_file.replace('.json', '')  # Remove .json extension
                
                # Build suffix based on algorithm and heuristic (matching your code logic)
                if algorithm == "a_star" and heuristic:
                    suffix = f"_a_star_{heuristic}"
                elif algorithm == "a_star" and not heuristic:
                    suffix = "_a_star"
                elif heuristic:
                    suffix = f"_{algorithm}_{heuristic}"
                else:
                    suffix = f"_{algorithm}"
                
                output_filename = f"{filename}{suffix}.json"
                output_path = os.path.join("data", "output", output_filename)
                
                print(f"Expected output file: {output_path}")
                
                # Wait a moment for file to be written completely
                time.sleep(0.3)
                
                # Try to read the output file
                if os.path.exists(output_path):
                    print(f"✅ Found output file: {output_filename}")
                    try:
                        with open(output_path, 'r') as f:
                            result_data = json.load(f)
                        
                        print(f"📖 Successfully loaded solution data")
                        print(f"Status: {result_data.get('status')}")
                        print(f"Solution length: {result_data.get('solution_length', 0)}")
                        
                        if result_data.get("status") == "Path found":
                            self.solution_path = result_data["solution_path"]
                            self.solution_data = result_data
                            self.current_step = 0
                            self.current_state = self.initial_state[:]
                            self.move_history = []
                            self.current_move_highlight = None
                            
                            print(f"🎯 Solution found with {len(self.solution_path)} steps!")
                            print(f"First 5 moves: {self.solution_path[:5]}")
                            
                            # Start automatic animation
                            self.is_auto_solving = True
                            self.is_paused = False
                            self.last_move_time = time.time()
                            
                            print("🚀 Starting automatic animation...")
                        else:
                            self.solution_path = []
                            self.solution_data = result_data
                            print(f"❌ No solution found. Status: {result_data.get('status', 'Unknown')}")
                        
                    except Exception as e:
                        print(f"❌ Error reading output file: {e}")
                        self.solution_data = {"status": "error", "error": f"Error reading output file: {e}"}
                else:
                    print(f"❌ Output file not found: {output_path}")
                    # List actual files for debugging
                    output_dir = os.path.join("data", "output")
                    if os.path.exists(output_dir):
                        actual_files = os.listdir(output_dir)
                        print(f"Files in output directory: {actual_files}")
                        
                        # Try to find the most recently created file with similar name
                        matching_files = [f for f in actual_files if filename in f]
                        if matching_files:
                            # Use the first matching file
                            latest_file = matching_files[0]
                            print(f"🔍 Found matching file: {latest_file}")
                            latest_path = os.path.join(output_dir, latest_file)
                            try:
                                with open(latest_path, 'r') as f:
                                    result_data = json.load(f)
                                
                                if result_data.get("status") == "Path found":
                                    self.solution_path = result_data["solution_path"]
                                    self.solution_data = result_data
                                    self.current_step = 0
                                    self.current_state = self.initial_state[:]
                                    self.move_history = []
                                    self.current_move_highlight = None
                                    
                                    # Start automatic animation
                                    self.is_auto_solving = True
                                    self.is_paused = False
                                    self.last_move_time = time.time()
                                    
                                    print(f"🚀 Starting animation with {len(self.solution_path)} steps!")
                                else:
                                    self.solution_data = result_data
                            except Exception as e:
                                print(f"Error reading matching file: {e}")
                                self.solution_data = {"status": "error", "error": f"Error reading file: {e}"}
                        else:
                            self.solution_data = {"status": "error", "error": "No matching output file found"}
                    else:
                        self.solution_data = {"status": "error", "error": "Output directory not found"}
                    
            except Exception as e:
                print(f"❌ Error in solve_thread: {e}")
                import traceback
                traceback.print_exc()
                self.solution_data = {"status": "error", "error": str(e)}
            finally:
                self.solving = False
                self.solve_button.text = "Solve"
        
        thread = threading.Thread(target=solve_thread)
        thread.daemon = True
        thread.start()
    
    def step_forward(self):
        """Move one step forward in the solution"""
        if not self.solution_path or self.current_step >= len(self.solution_path):
            print("No more steps to execute")
            return False
        
        move_direction = self.solution_path[self.current_step]
        print(f"Applying move {self.current_step + 1}: {move_direction}")
        print(f"State before move: {self.current_state}")
        
        # Highlight current move
        self.current_move_highlight = self.current_step
        
        # Apply move to current state
        if self.apply_move(move_direction):
            print(f"State after move: {self.current_state}")
            
            # Add to move history
            self.move_history.append({
                'step': self.current_step + 1,
                'move': move_direction,
                'state': self.current_state[:]
            })
            
            self.current_step += 1
            
            # Check if puzzle is solved
            if self.current_state == self.goal_state:
                self.is_auto_solving = False
                print("🎉 Puzzle solved successfully!")
                return False
            
            return True
        else:
            print(f"❌ Invalid move: {move_direction}")
            return False
    
    def apply_move(self, move_direction):
        """Apply a move direction to the current state"""
        try:
            # Find the empty space (0)
            if 0 not in self.current_state:
                print("❌ Error: No empty space (0) found in current state")
                return False
                
            empty_pos = self.current_state.index(0)
            size = self.puzzle_size
            row, col = divmod(empty_pos, size)
            
            # Calculate new position based on direction
            new_row, new_col = row, col
            if move_direction == "U":
                new_row = row - 1
            elif move_direction == "D":
                new_row = row + 1
            elif move_direction == "L":
                new_col = col - 1
            elif move_direction == "R":
                new_col = col + 1
            else:
                print(f"❌ Invalid move direction: {move_direction}")
                return False
            
            # Check if move is valid (within bounds)
            if 0 <= new_row < size and 0 <= new_col < size:
                new_pos = new_row * size + new_col
                
                # Swap empty space with the tile at new position
                tile_value = self.current_state[new_pos]
                self.current_state[empty_pos], self.current_state[new_pos] = \
                    self.current_state[new_pos], self.current_state[empty_pos]
                
                print(f"✅ Moved tile {tile_value} {move_direction}")
                return True
            else:
                print(f"❌ Move {move_direction} would go out of bounds from position ({row}, {col})")
                return False
                
        except Exception as e:
            print(f"❌ Error applying move {move_direction}: {e}")
            return False
    
    def reset_puzzle(self):
        """Reset puzzle to initial state"""
        self.current_state = self.initial_state[:]
        self.current_step = 0
        self.is_auto_solving = False
        self.is_paused = False
        self.move_history = []
        self.current_move_highlight = None
    
    def draw_puzzle(self):        
        if not self.current_state:
            return
        
        # Draw puzzle container with success indicator
        container_rect = self.puzzle_area.copy()
        container_rect.inflate_ip(20, 20)
        
        # Check if puzzle is solved
        is_solved = self.current_state == self.goal_state if self.goal_state else False
        
        # Draw shadow
        shadow_rect = container_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_rect, border_radius=15)
        
        # Draw container with success color if solved
        container_color = (220, 252, 231) if is_solved else CARD_BACKGROUND
        border_color = SUCCESS if is_solved else BORDER
        
        pygame.draw.rect(self.screen, container_color, container_rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, container_rect, 3 if is_solved else 2, border_radius=15)
        
        # Add "SOLVED!" text if completed
        if is_solved:            
            solved_text = FONT_LARGE.render("SOLVED!", True, SUCCESS)
            text_rect = solved_text.get_rect(center=(container_rect.centerx, container_rect.y - 15))
            self.screen.blit(solved_text, text_rect)
        
        # Calculate tile size and spacing with better margins
        available_width = self.puzzle_area.width - 40
        available_height = self.puzzle_area.height - 40
        spacing = 12
        
        tile_size = min(
            (available_width - (self.puzzle_size - 1) * spacing) // self.puzzle_size,
            (available_height - (self.puzzle_size - 1) * spacing) // self.puzzle_size
        )
        
        # Center the puzzle grid
        total_width = self.puzzle_size * tile_size + (self.puzzle_size - 1) * spacing
        total_height = self.puzzle_size * tile_size + (self.puzzle_size - 1) * spacing
        start_x = self.puzzle_area.x + (self.puzzle_area.width - total_width) // 2
        start_y = self.puzzle_area.y + (self.puzzle_area.height - total_height) // 2
        
        for i, value in enumerate(self.current_state):
            row = i // self.puzzle_size
            col = i % self.puzzle_size
            
            x = start_x + col * (tile_size + spacing)
            y = start_y + row * (tile_size + spacing)
            
            tile_rect = pygame.Rect(x, y, tile_size, tile_size)
            
            if value == 0:
                # Empty space - make it more visible with a dashed border
                pygame.draw.rect(self.screen, (200, 200, 200), tile_rect, border_radius=12)
                pygame.draw.rect(self.screen, (150, 150, 150), tile_rect, 3, border_radius=12)
                
                # Add subtle pattern to show it's empty
                for dash_y in range(tile_rect.y + 10, tile_rect.bottom - 10, 15):
                    for dash_x in range(tile_rect.x + 10, tile_rect.right - 10, 15):
                        pygame.draw.circle(self.screen, (180, 180, 180), (dash_x, dash_y), 2)
            else:
                # Draw enhanced tile shadow
                shadow_tile = tile_rect.copy()
                shadow_tile.x += 3
                shadow_tile.y += 3
                pygame.draw.rect(self.screen, (0, 0, 0, 60), shadow_tile, border_radius=12)
                
                # Draw tile with gradient effect
                pygame.draw.rect(self.screen, TILE_COLORS['default'], tile_rect, border_radius=12)
                
                # Add subtle inner highlight
                highlight_rect = tile_rect.copy()
                highlight_rect.inflate(-4, -4)
                pygame.draw.rect(self.screen, (240, 248, 255), highlight_rect, 2, border_radius=10)
                
                # Draw border
                pygame.draw.rect(self.screen, BORDER, tile_rect, 3, border_radius=12)
                
                # Draw number with better font sizing
                font_size = max(24, tile_size // 3)
                number_font = pygame.font.Font(None, font_size)
                text = number_font.render(str(value), True, TILE_COLORS['number'])
                text_rect = text.get_rect(center=tile_rect.center)
                self.screen.blit(text, text_rect)
        
        # Draw current move indicator
        if (self.is_auto_solving and self.solution_path and 
            self.current_step > 0 and self.current_step <= len(self.solution_path)):
            
            current_move = self.solution_path[self.current_step - 1] if self.current_step > 0 else None
            if current_move:
                # Find empty space position
                empty_pos = self.current_state.index(0)
                empty_row = empty_pos // self.puzzle_size
                empty_col = empty_pos % self.puzzle_size
                
                # Calculate empty space screen position
                empty_x = start_x + empty_col * (tile_size + spacing) + tile_size // 2
                empty_y = start_y + empty_row * (tile_size + spacing) + tile_size // 2
                
                # Draw move direction arrow
                arrow_size = 20
                arrow_color = (255, 100, 100)  # Red arrow
                
                if current_move == "U":
                    # Arrow pointing up
                    points = [
                        (empty_x, empty_y - arrow_size),
                        (empty_x - arrow_size//2, empty_y),
                        (empty_x + arrow_size//2, empty_y)
                    ]
                elif current_move == "D":
                    # Arrow pointing down  
                    points = [
                        (empty_x, empty_y + arrow_size),
                        (empty_x - arrow_size//2, empty_y),
                        (empty_x + arrow_size//2, empty_y)
                    ]
                elif current_move == "L":
                    # Arrow pointing left
                    points = [
                        (empty_x - arrow_size, empty_y),
                        (empty_x, empty_y - arrow_size//2),
                        (empty_x, empty_y + arrow_size//2)
                    ]
                elif current_move == "R":
                    # Arrow pointing right
                    points = [
                        (empty_x + arrow_size, empty_y),
                        (empty_x, empty_y - arrow_size//2),
                        (empty_x, empty_y + arrow_size//2)
                    ]
                
                if 'points' in locals():
                    pygame.draw.polygon(self.screen, arrow_color, points)
                      # Draw move text
                move_text = FONT_SMALL.render(f"Move: {current_move}", True, arrow_color)
                text_rect = move_text.get_rect(center=(empty_x, empty_y + 40))
                self.screen.blit(move_text, text_rect)
    
    def draw_labels(self):
        """Draw section labels"""
        x = self.control_area.x + 20
        
        # Input file label
        text = FONT_MEDIUM.render("Input File:", True, TEXT_PRIMARY)
        self.screen.blit(text, (x, self.control_area.y + 20))
        
        # Algorithm label
        text = FONT_MEDIUM.render("Algorithm:", True, TEXT_PRIMARY)
        self.screen.blit(text, (x, self.control_area.y + 140))
        
        # Heuristic label
        text = FONT_MEDIUM.render("Heuristic:", True, TEXT_PRIMARY)
        self.screen.blit(text, (x, self.control_area.y + 260))
        
        # Speed label - fixed position using stored coordinate
        text = FONT_MEDIUM.render(f"Animation Speed: {self.speed_slider.get_value():.1f}x", True, TEXT_PRIMARY)
        self.screen.blit(text, (x, self.speed_slider_y - 20))
        
        # Progress and status
        if self.solution_path:
            total_steps = len(self.solution_path)
            progress_text = f"Step: {self.current_step} / {total_steps}"
            if self.is_auto_solving:
                progress_text += " (Auto-solving...)"
            elif self.solving:
                progress_text = "Computing solution..."
            text = FONT_MEDIUM.render(progress_text, True, TEXT_PRIMARY)
            self.screen.blit(text, (x, self.progress_y))
            
            # Progress bar
            if total_steps > 0:
                progress_rect = pygame.Rect(x, self.progress_y + 25, 300, 8)
                pygame.draw.rect(self.screen, BORDER, progress_rect, border_radius=4)
                
                progress_width = (self.current_step / total_steps) * 300
                filled_rect = pygame.Rect(x, self.progress_y + 25, progress_width, 8)
                color = SUCCESS if self.current_step == total_steps else PRIMARY
                pygame.draw.rect(self.screen, color, filled_rect, border_radius=4)
        elif self.solving:
            text = FONT_MEDIUM.render("Computing solution...", True, TEXT_PRIMARY)
            self.screen.blit(text, (x, self.progress_y))
    
    def draw_statistics(self):
        """Draw statistics in a modern card layout"""
        x = self.control_area.x + 20
        y = self.stats_y
        
        # Draw statistics card
        stats_rect = pygame.Rect(x - 10, y - 10, 350, 250)
        shadow_stats = stats_rect.copy()
        shadow_stats.x += 2
        shadow_stats.y += 2
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_stats, border_radius=10)
        pygame.draw.rect(self.screen, CARD_BACKGROUND, stats_rect, border_radius=10)
        pygame.draw.rect(self.screen, BORDER, stats_rect, 2, border_radius=10)
        
        # Title
        title_text = FONT_LARGE.render("Statistics", True, TEXT_PRIMARY)
        self.screen.blit(title_text, (x, y))
        y += 35
        
        if not self.solution_data:
            text = FONT_MEDIUM.render("No solution loaded", True, TEXT_SECONDARY)
            self.screen.blit(text, (x, y))
            return
        
        # Statistics data
        stats = [
            ("Puzzle", self.solution_data.get('puzzle_name', 'Unknown')),
            ("Algorithm", self.solution_data.get('algorithm', 'Unknown')),
            ("Heuristic", self.solution_data.get('heuristic') or 'None'),
            ("Status", self.solution_data.get('status', 'Unknown')),
            ("Solution Length", str(self.solution_data.get('solution_length', 0))),
            ("Time Taken", f"{self.solution_data.get('time_taken', 0):.4f}s"),
            ("Space Used", str(self.solution_data.get('space_used', 0))),
            ("Nodes Expanded", str(self.solution_data.get('nodes_expanded', 0)))
        ]
        
        for i, (label, value) in enumerate(stats):
            # Label
            label_text = FONT_SMALL.render(f"{label}:", True, TEXT_SECONDARY)
            self.screen.blit(label_text, (x, y + i * 22))
            
            # Value
            value_text = FONT_SMALL.render(str(value), True, TEXT_PRIMARY)
            self.screen.blit(value_text, (x + 120, y + i * 22))
    
    def draw_move_list(self):
        """Draw the list of moves being executed"""
        if not self.solution_path or not self.show_move_list:
            return
            
        # Move list area - positioned below the controls
        list_x = self.control_area.x + 400
        list_y = self.control_area.y + 100
        list_width = 350
        list_height = 400
        
        # Draw container
        list_rect = pygame.Rect(list_x, list_y, list_width, list_height)
        shadow_list = list_rect.copy()
        shadow_list.x += 2
        shadow_list.y += 2
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_list, border_radius=10)
        pygame.draw.rect(self.screen, CARD_BACKGROUND, list_rect, border_radius=10)
        pygame.draw.rect(self.screen, BORDER, list_rect, 2, border_radius=10)
        
        # Title
        title_text = FONT_MEDIUM.render("Solution Steps", True, TEXT_PRIMARY)
        self.screen.blit(title_text, (list_x + 10, list_y + 10))
        
        # Progress info
        progress_text = f"Step {self.current_step} of {len(self.solution_path)}"
        progress_surf = FONT_SMALL.render(progress_text, True, TEXT_SECONDARY)
        self.screen.blit(progress_surf, (list_x + 10, list_y + 35))
        
        # Scrollable move list
        moves_start_y = list_y + 60
        visible_moves = (list_height - 70) // 25
        
        # Calculate scroll offset to keep current move visible
        scroll_offset = max(0, self.current_step - visible_moves + 3)
        
        for i, move in enumerate(self.solution_path):
            if i < scroll_offset or i >= scroll_offset + visible_moves:
                continue
                
            move_y = moves_start_y + (i - scroll_offset) * 25
            
            # Highlight current move
            if i == self.current_step - 1 and self.current_move_highlight is not None:
                highlight_rect = pygame.Rect(list_x + 5, move_y - 2, list_width - 10, 24)
                pygame.draw.rect(self.screen, (255, 235, 59, 100), highlight_rect, border_radius=5)
            
            # Move status
            if i < self.current_step:
                status_color = SUCCESS
                status_text = "✓"
            elif i == self.current_step:
                status_color = WARNING
                status_text = "→"
            else:
                status_color = TEXT_SECONDARY
                status_text = " "
            
            # Draw move
            step_text = f"{i+1:2d}. {move}"
            step_surf = FONT_SMALL.render(step_text, True, TEXT_PRIMARY)
            self.screen.blit(step_surf, (list_x + 25, move_y))
              # Draw status
            status_surf = FONT_SMALL.render(status_text, True, status_color)
            self.screen.blit(status_surf, (list_x + 10, move_y))
    
    def handle_event(self, event):
        """Handle pygame events"""
        # Handle dropdown events in reverse order (top to bottom z-index)
        # This ensures the topmost dropdown gets priority
        dropdowns = [self.heuristic_dropdown, self.algorithm_dropdown, self.input_dropdown]
        
        # First, check if any dropdown is open and handle that one first
        open_dropdown = None
        for dropdown in dropdowns:
            if dropdown.open:
                open_dropdown = dropdown
                break
        
        if open_dropdown:
            # If a dropdown is open, only handle events for that dropdown
            if open_dropdown.handle_event(event):
                # Update state based on which dropdown was changed
                if open_dropdown == self.input_dropdown:
                    selected_file = self.input_dropdown.get_selected()
                    if selected_file and selected_file != "No files":
                        self.load_puzzle(selected_file)
                elif open_dropdown == self.algorithm_dropdown:
                    self.current_algorithm = self.algorithm_dropdown.get_selected()
                elif open_dropdown == self.heuristic_dropdown:
                    self.current_heuristic = self.heuristic_dropdown.get_selected()
        else:
            # No dropdown is open, handle all UI elements normally
            if self.input_dropdown.handle_event(event):
                selected_file = self.input_dropdown.get_selected()
                if selected_file and selected_file != "No files":
                    self.load_puzzle(selected_file)
            
            if self.algorithm_dropdown.handle_event(event):
                self.current_algorithm = self.algorithm_dropdown.get_selected()
            
            if self.heuristic_dropdown.handle_event(event):
                self.current_heuristic = self.heuristic_dropdown.get_selected()
            
            # Handle button events
            if self.solve_button.handle_event(event):
                self.solve_puzzle()
            if self.reset_button.handle_event(event):
                self.reset_puzzle()
            if self.pause_button.handle_event(event):
                if self.is_auto_solving:
                    self.is_paused = not self.is_paused
                    self.pause_button.text = "Resume" if self.is_paused else "Pause"
            if self.step_button.handle_event(event):
                if self.solution_path and not self.is_auto_solving:
                    self.step_forward()
            
            # Handle slider events
            self.speed_slider.handle_event(event)
            self.animation_speed = self.speed_slider.get_value()
    
    def update(self, dt):
        """Update the application state"""
        # Handle automatic animation
        if self.is_auto_solving and self.solution_path and not self.is_paused:
            current_time = time.time()
            time_per_move = 1.0 / self.animation_speed
            
            if current_time - self.last_move_time >= time_per_move:
                print(f"Executing step {self.current_step + 1} of {len(self.solution_path)}")
                
                if self.step_forward():
                    self.last_move_time = current_time
                else:
                    # Animation finished
                    self.is_auto_solving = False
                    print("Animation completed!")
    def draw(self):
        """Draw the entire GUI"""        
        self.screen.fill(BACKGROUND)
        
        # Draw puzzle
        self.draw_puzzle()
        
        # Draw text and statistics first (background layer)
        self.draw_labels()
        self.draw_statistics()
        self.draw_move_list()
        
        # Draw buttons (middle layer)
        self.solve_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.step_button.draw(self.screen)
        
        self.speed_slider.draw(self.screen)
        
        # Draw dropdowns last (top layer) so they appear on top
        # First draw closed dropdowns
        closed_dropdowns = []
        open_dropdown = None
        
        for dropdown in [self.input_dropdown, self.algorithm_dropdown, self.heuristic_dropdown]:
            if dropdown.open:
                open_dropdown = dropdown
            else:
                closed_dropdowns.append(dropdown)
        
        # Draw closed dropdowns first
        for dropdown in closed_dropdowns:
            dropdown.draw(self.screen)
        
        # Draw open dropdown last so it appears on top
        if open_dropdown:
            open_dropdown.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main application loop"""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.handle_event(event)
            
            self.update(dt)
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    app = ModernPuzzleGUI()
    app.run()