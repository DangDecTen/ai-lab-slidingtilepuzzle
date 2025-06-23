"""
Refactored Modern Puzzle GUI - Main Application
"""
import pygame
import json
import os
import sys
import time
import threading

# Add the current directory to the path
sys.path.append('.')

from main import run_solver, ALGORITHMS, HEURISTICS
from ui.constants import *
from ui.components import ModernButton, ModernSlider
from ui.dropdown import ModernScrollableDropdown
from ui.puzzle_renderer import PuzzleRenderer
from ui.panels import StatisticsPanel, MoveListPanel, ProgressPanel


class ModernPuzzleGUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Puzzle Solver - Modern Interface")
        self.clock = pygame.time.Clock()
        
        # Application state
        self.input_files = self._load_input_files()
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
          # Initialize UI components with better spacing
        self.puzzle_renderer = PuzzleRenderer(PUZZLE_AREA)
        
        # Recalculate positions for better layout
        # Statistics panel - positioned lower to avoid overlap
        self.statistics_panel = StatisticsPanel(CONTROL_AREA.x + 20, CONTROL_AREA.y + 600)
        
        # Move list panel - positioned on the right side
        self.move_list_panel = MoveListPanel(CONTROL_AREA.x + 400, CONTROL_AREA.y + 100, 350, 400)
        
        # Progress panel - positioned between slider and statistics
        self.progress_panel = ProgressPanel(CONTROL_AREA.x + 20, CONTROL_AREA.y + 520)
        
        # UI Elements
        self._create_ui_elements()
        
        # Load first puzzle if available
        if self.input_files:
            self.load_puzzle(self.input_files[0])
    
    def _load_input_files(self):
        """Load all available input files"""
        input_dir = os.path.join("data", "input")
        if not os.path.exists(input_dir):
            return []
        return sorted([f for f in os.listdir(input_dir) if f.endswith(".json")])
    
    def _create_ui_elements(self):
        """Create all UI elements with modern design"""
        x = CONTROL_AREA.x + 20
        y = CONTROL_AREA.y + 20
        
        # Input file dropdown with scrolling
        self.input_dropdown = ModernScrollableDropdown(
            x, y + 40, 300, 40,
            self.input_files if self.input_files else ["No files"],
            max_visible=6
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
            max_visible=4        )
        y += 120
        
        # Control buttons - simplified to just Play and Reset
        button_y = y + 20
        button_width = 120
        button_spacing = 20
        
        self.play_button = ModernButton(x, button_y, button_width, 50, "Play", SUCCESS)
        self.reset_button = ModernButton(x + button_width + button_spacing, button_y, button_width, 50, "Reset", DANGER)
        y += 100
        
        # Speed slider with better spacing
        self.speed_slider_y = y + 50  # Increased spacing from buttons
        self.speed_slider = ModernSlider(x, self.speed_slider_y, 300, 30, 0.5, 5.0, 2.0)
    
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
        
        self.is_auto_solving = False
        self.solving = True
        self.play_button.text = "Solving..."
        
        def solve_thread():
            try:
                input_file = self.current_input_file
                algorithm = self.current_algorithm
                heuristic = self.current_heuristic if self.current_heuristic != "None" else None
                
                print(f"=== STARTING SOLVER ===")
                print(f"Input file: {input_file}")
                print(f"Algorithm: {algorithm}")
                print(f"Heuristic: {heuristic}")
                
                # Run solver
                input_path = f"data/input/{input_file}"
                run_solver(input_path, algorithm, heuristic)
                
                # Load result
                output_path = self._get_output_path(input_file, algorithm, heuristic)
                time.sleep(0.3)  # Wait for file to be written
                
                if os.path.exists(output_path):
                    with open(output_path, 'r') as f:
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
                        self.solution_path = []
                        self.solution_data = result_data
                        print(f"❌ No solution found. Status: {result_data.get('status', 'Unknown')}")
                else:
                    print(f"❌ Output file not found: {output_path}")
                    self.solution_data = {"status": "error", "error": "Output file not found"}
                    
            except Exception as e:
                print(f"❌ Error in solve_thread: {e}")
                self.solution_data = {"status": "error", "error": str(e)}
            finally:
                self.solving = False
                if self.is_auto_solving:
                    self.play_button.text = "Pause"
                else:
                    self.play_button.text = "Play"
        
        thread = threading.Thread(target=solve_thread)
        thread.daemon = True
        thread.start()
    
    def _get_output_path(self, input_file, algorithm, heuristic):
        """Generate output file path"""
        filename = input_file.replace('.json', '')
        
        if algorithm == "a_star" and heuristic:
            suffix = f"_a_star_{heuristic}"
        elif algorithm == "a_star" and not heuristic:
            suffix = "_a_star"
        elif heuristic:
            suffix = f"_{algorithm}_{heuristic}"
        else:
            suffix = f"_{algorithm}"
        
        output_filename = f"{filename}{suffix}.json"
        return os.path.join("data", "output", output_filename)
    
    def step_forward(self):
        """Move one step forward in the solution"""
        if not self.solution_path or self.current_step >= len(self.solution_path):
            return False
        
        move_direction = self.solution_path[self.current_step]
        self.current_move_highlight = self.current_step
        
        if self._apply_move(move_direction):
            self.move_history.append({
                'step': self.current_step + 1,
                'move': move_direction,
                'state': self.current_state[:]
            })
            self.current_step += 1
            
            if self.current_state == self.goal_state:
                self.is_auto_solving = False
                self.play_button.text = "Play"
                print("🎉 Puzzle solved successfully!")
                return False
            
            return True
        else:
            print(f"❌ Invalid move: {move_direction}")
            return False
    
    def _apply_move(self, move_direction):
        """Apply a move direction to the current state"""
        try:
            if 0 not in self.current_state:
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
                return False
            
            # Check if move is valid
            if 0 <= new_row < size and 0 <= new_col < size:
                new_pos = new_row * size + new_col
                self.current_state[empty_pos], self.current_state[new_pos] = \
                    self.current_state[new_pos], self.current_state[empty_pos]
                return True
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
        self.play_button.text = "Play"
    
    def _draw_labels(self):
        """Draw section labels"""
        x = CONTROL_AREA.x + 20
        
        # Labels
        labels = [
            ("Input File:", CONTROL_AREA.y + 20),
            ("Algorithm:", CONTROL_AREA.y + 140),
            ("Heuristic:", CONTROL_AREA.y + 260),
            (f"Animation Speed: {self.speed_slider.get_value():.1f}x", self.speed_slider_y - 20)
        ]
        
        for label, y in labels:
            text = FONT_MEDIUM.render(label, True, TEXT_PRIMARY)
            self.screen.blit(text, (x, y))
    
    def handle_event(self, event):
        """Handle pygame events with proper z-index"""
        dropdowns = [self.heuristic_dropdown, self.algorithm_dropdown, self.input_dropdown]
        
        # Handle open dropdown first
        open_dropdown = None
        for dropdown in dropdowns:
            if dropdown.open:
                open_dropdown = dropdown
                break
        
        if open_dropdown:
            if open_dropdown.handle_event(event):
                self._handle_dropdown_change(open_dropdown)
        else:
            # Handle all UI elements when no dropdown is open
            self._handle_ui_events(event)
    
    def _handle_dropdown_change(self, dropdown):
        """Handle dropdown selection changes"""
        if dropdown == self.input_dropdown:
            selected_file = self.input_dropdown.get_selected()
            if selected_file and selected_file != "No files":
                self.load_puzzle(selected_file)
        elif dropdown == self.algorithm_dropdown:
            self.current_algorithm = self.algorithm_dropdown.get_selected()
        elif dropdown == self.heuristic_dropdown:
            self.current_heuristic = self.heuristic_dropdown.get_selected()
    def _handle_ui_events(self, event):
        """Handle UI events when no dropdown is open"""
        # Dropdowns
        for dropdown in [self.input_dropdown, self.algorithm_dropdown, self.heuristic_dropdown]:
            if dropdown.handle_event(event):
                self._handle_dropdown_change(dropdown)
        
        # Buttons
        if self.play_button.handle_event(event):
            if not self.is_auto_solving and not self.solving:
                self.solve_puzzle()
            elif self.is_auto_solving:
                # Toggle pause/resume
                self.is_paused = not self.is_paused
                self.play_button.text = "Resume" if self.is_paused else "Pause"
        if self.reset_button.handle_event(event):
            self.reset_puzzle()
        
        # Slider
        self.speed_slider.handle_event(event)
        self.animation_speed = self.speed_slider.get_value()
    
    def update(self, dt):
        """Update the application state"""
        if self.is_auto_solving and self.solution_path and not self.is_paused:
            current_time = time.time()
            time_per_move = 1.0 / self.animation_speed
            if current_time - self.last_move_time >= time_per_move:
                if self.step_forward():
                    self.last_move_time = current_time
                else:
                    self.is_auto_solving = False
                    self.play_button.text = "Play"
    
    def draw(self):
        """Draw the entire GUI with proper layering"""
        self.screen.fill(BACKGROUND)
        
        # Draw puzzle
        self.puzzle_renderer.draw_puzzle(
            self.screen, self.current_state, self.goal_state, self.puzzle_size,
            self.solution_path, self.current_step, self.is_auto_solving
        )
        
        # Draw panels (background layer)
        self._draw_labels()
        self.statistics_panel.draw_statistics(self.screen, self.solution_data)
        self.move_list_panel.draw_move_list(
            self.screen, self.solution_path, self.current_step, 
            self.current_move_highlight, self.show_move_list
        )               
        # Draw buttons (middle layer)
        for button in [self.play_button, self.reset_button]:
            button.draw(self.screen)
        
        self.speed_slider.draw(self.screen)
        
        # Draw dropdowns (top layer)
        closed_dropdowns = []
        open_dropdown = None
        
        for dropdown in [self.input_dropdown, self.algorithm_dropdown, self.heuristic_dropdown]:
            if dropdown.open:
                open_dropdown = dropdown
            else:
                closed_dropdowns.append(dropdown)
        
        for dropdown in closed_dropdowns:
            dropdown.draw(self.screen)
        
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
