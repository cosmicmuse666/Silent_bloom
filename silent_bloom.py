import tkinter as tk
import subprocess
import os
import sys
import logging
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='silent_bloom.log'
)

class SilentBloom:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Silent Bloom")
            
            # Verify nircmd.exe exists
            self.nircmd_path = os.path.join(os.path.dirname(__file__), "nircmd.exe")
            if not os.path.exists(self.nircmd_path):
                logging.error("nircmd.exe not found")
                self.show_error("Required file nircmd.exe not found!")
                sys.exit(1)
            
            # Set window properties
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            
            # Handle window close event
            self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
            
            # Set window size and position with bounds checking
            self.window_size = 60
            screen_width = max(self.root.winfo_screenwidth(), self.window_size * 2)
            screen_height = max(self.root.winfo_screenheight(), self.window_size * 2)
            
            # Ensure window is always visible
            x_position = min(screen_width - self.window_size - 20, screen_width - self.window_size)
            x_position = max(0, x_position)
            y_position = min(screen_height // 2, screen_height - self.window_size)
            y_position = max(0, y_position)
            
            self.root.geometry(f"{self.window_size}x{self.window_size}+{x_position}+{y_position}")
            
            # Create canvas for the circular button
            self.canvas = tk.Canvas(
                self.root,
                width=self.window_size,
                height=self.window_size,
                bg='white',
                highlightthickness=0
            )
            self.canvas.pack(fill='both', expand=True)
            
            # Initialize audio state
            self.is_muted = self.get_mute_state()
            self.create_button()
            
            # Add keyboard shortcuts
            self.root.bind('<Escape>', self.exit_app)
            self.root.bind('<space>', self.toggle_mute)
            
            # Update button color based on initial state
            self.update_button_color()
            
        except tk.TclError as e:
            logging.error(f"Failed to initialize GUI: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error during initialization: {e}")
            sys.exit(1)
    
    def show_error(self, message: str) -> None:
        """Show error message in a simple popup"""
        try:
            error_window = tk.Tk()
            error_window.title("Error")
            error_window.geometry("300x100")
            tk.Label(error_window, text=message, wraplength=250).pack(pady=20)
            tk.Button(error_window, text="OK", command=error_window.destroy).pack()
            error_window.mainloop()
        except Exception as e:
            logging.error(f"Failed to show error window: {e}")
    
    def create_button(self) -> None:
        """Create a simple button"""
        try:
            padding = 5
            
            # Main button circle
            self.button = self.canvas.create_oval(
                padding, padding,
                self.window_size - padding, self.window_size - padding,
                fill='black',
                outline='gray',
                width=1
            )
            
            # Bind mouse events
            self.canvas.tag_bind(self.button, '<Button-1>', self.toggle_mute)
            self.canvas.tag_bind(self.button, '<Button-3>', self.exit_app)
            
        except tk.TclError as e:
            logging.error(f"Failed to create button: {e}")
            self.show_error("Failed to create button interface!")
            self.exit_app()
    
    def update_button_color(self) -> None:
        """Update button color based on mute state"""
        try:
            color = '#FF4444' if self.is_muted else 'black'  # Red when muted, black when unmuted
            self.canvas.itemconfig(self.button, fill=color)
        except Exception as e:
            logging.error(f"Failed to update button color: {e}")
    
    def get_mute_state(self) -> bool:
        """Check if system audio is currently muted"""
        try:
            result = subprocess.run(
                [self.nircmd_path, "mutesysvolume", "2"],  # 2 = get mute state
                capture_output=True,
                text=True,
                timeout=2
            )
            return "Muted" in result.stdout
        except Exception as e:
            logging.error(f"Error checking mute state: {e}")
            return False
    
    def toggle_mute(self, event: Optional[tk.Event] = None) -> None:
        """Toggle system audio mute state"""
        try:
            # Toggle mute state (1 = toggle)
            result = subprocess.run(
                [self.nircmd_path, "mutesysvolume", "2"],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                self.is_muted = not self.is_muted
                self.update_button_color()
                logging.info(f"Audio {'muted' if self.is_muted else 'unmuted'}")
            else:
                logging.error(f"Failed to toggle mute: {result.stderr}")
                self.show_error("Failed to toggle mute state!")
        except subprocess.TimeoutExpired:
            logging.error("Timeout while toggling mute")
            self.show_error("Operation timed out!")
        except Exception as e:
            logging.error(f"Error toggling mute: {e}")
            self.show_error(f"Failed to toggle mute: {str(e)}")
    
    def exit_app(self, event: Optional[tk.Event] = None) -> None:
        """Clean exit of the application"""
        try:
            logging.info("Application shutting down")
            self.root.quit()
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
            sys.exit(1)
    
    def run(self) -> None:
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            self.show_error("Application encountered an error and needs to close!")
            sys.exit(1)

if __name__ == "__main__":
    try:
        app = SilentBloom()
        app.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        # Try to show error in console if GUI fails
        print(f"Fatal error: {e}", file=sys.stderr) 