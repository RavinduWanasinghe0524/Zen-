"""
Zen Voice Assistant - GUI Overlay Module
Visual feedback for assistant states with modern design.
"""

import tkinter as tk
from tkinter import ttk
import threading
import math
from logger import get_logger

logger = get_logger(__name__)


class ZenGUI:
    """Modern GUI overlay for Zen voice assistant."""
    
    # State constants
    STATE_IDLE = "idle"
    STATE_LISTENING = "listening"
    STATE_THINKING = "thinking"
    STATE_SPEAKING = "speaking"
    STATE_WAKE_WORD = "wake_word"
    
    # Color scheme
    COLORS = {
        STATE_IDLE: "#4CAF50",      # Green
        STATE_LISTENING: "#F44336",  # Red
        STATE_THINKING: "#FFC107",   # Yellow
        STATE_SPEAKING: "#2196F3",   # Blue
        STATE_WAKE_WORD: "#9E9E9E"   # Gray
    }
    
    def __init__(self, position="bottom-right", opacity=0.9, always_on_top=True):
        """
        Initialize the GUI overlay.
        
        Args:
            position: Window position (top-left, top-right, bottom-left, bottom-right)
            opacity: Window opacity 0.0-1.0
            always_on_top: Keep window on top
        """
        self.position = position
        self.opacity = opacity
        self.always_on_top = always_on_top
        self.current_state = self.STATE_IDLE
        self.animation_running = False
        self.animation_frame = 0
        
        # Create window in separate thread
        self.root = None
        self.gui_thread = None
        self.ready = False
    
    def start(self):
        """Start the GUI in a separate thread."""
        self.gui_thread = threading.Thread(target=self._create_window, daemon=True)
        self.gui_thread.start()
        
        # Wait for GUI to be ready
        timeout = 5
        start_time = threading.Event()
        for _ in range(timeout * 10):
            if self.ready:
                break
            threading.Event().wait(0.1)
        
        logger.info("GUI overlay started")
    
    def _create_window(self):
        """Create the tkinter window."""
        try:
            self.root = tk.Tk()
            self.root.title("Zen Assistant")
            
            # Window dimensions
            width = 200
            height = 200
            
            # Calculate position
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if "right" in self.position:
                x = screen_width - width - 20
            else:
                x = 20
            
            if "bottom" in self.position:
                y = screen_height - height - 60
            else:
                y = 60
            
            # Configure window
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            self.root.attributes("-alpha", self.opacity)
            self.root.attributes("-topmost", self.always_on_top)
            self.root.overrideredirect(True)  # Remove window decorations
            
            # Create canvas for animations
            self.canvas = tk.Canvas(
                self.root,
                width=width,
                height=height,
                bg='#1a1a1a',
                highlightthickness=0
            )
            self.canvas.pack(fill=tk.BOTH, expand=True)
            
            # Create status label
            self.status_label = tk.Label(
                self.root,
                text="Zen",
                font=("Segoe UI", 12, "bold"),
                bg='#1a1a1a',
                fg='white'
            )
            self.status_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
            
            # Create status text
            self.state_label = tk.Label(
                self.root,
                text="Ready",
                font=("Segoe UI", 9),
                bg='#1a1a1a',
                fg='#888888'
            )
            self.state_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
            
            # Make window draggable
            self.canvas.bind("<Button-1>", self._start_drag)
            self.canvas.bind("<B1-Motion>", self._on_drag)
            
            # Close button (small X in corner)
            close_btn = tk.Label(
                self.root,
                text="×",
                font=("Arial", 14, "bold"),
                bg='#1a1a1a',
                fg='#888888',
                cursor="hand2"
            )
            close_btn.place(x=width-20, y=5)
            close_btn.bind("<Button-1>", lambda e: self.root.quit())
            
            self.ready = True
            
            # Start animation
            self._animate()
            
            # Start tkinter main loop
            self.root.mainloop()
        
        except Exception as e:
            logger.error(f"Failed to create GUI: {e}")
    
    def _start_drag(self, event):
        """Start dragging the window."""
        self.drag_x = event.x
        self.drag_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging."""
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")
    
    def _animate(self):
        """Animate the visual indicator."""
        if not self.root:
            return
        
        try:
            self.canvas.delete("all")
            
            width = 200
            height = 200
            center_x = width // 2
            center_y = height // 2 - 20
            
            color = self.COLORS.get(self.current_state, "#FFFFFF")
            
            if self.current_state == self.STATE_IDLE or self.current_state == self.STATE_WAKE_WORD:
                # Pulsing circle
                radius = 40 + 10 * math.sin(self.animation_frame * 0.1)
                self.canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    fill=color, outline=color
                )
            
            elif self.current_state == self.STATE_LISTENING:
                # Waveform animation
                for i in range(10):
                    x = center_x - 50 + i * 11
                    height_val = 20 + 30 * abs(math.sin(self.animation_frame * 0.2 + i * 0.5))
                    self.canvas.create_rectangle(
                        x, center_y - height_val,
                        x + 8, center_y + height_val,
                        fill=color, outline=color
                    )
            
            elif self.current_state == self.STATE_THINKING:
                # Spinning loader
                for i in range(8):
                    angle = (self.animation_frame * 0.2 + i * (math.pi / 4)) % (2 * math.pi)
                    x = center_x + 40 * math.cos(angle)
                    y = center_y + 40 * math.sin(angle)
                    alpha = int(255 * (i / 8))
                    self.canvas.create_oval(
                        x - 5, y - 5, x + 5, y + 5,
                        fill=color, outline=color
                    )
            
            elif self.current_state == self.STATE_SPEAKING:
                # Expanding rings
                for i in range(3):
                    offset = (self.animation_frame + i * 20) % 60
                    radius = 30 + offset
                    alpha = 1 - (offset / 60)
                    self.canvas.create_oval(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        outline=color, width=3
                    )
            
            self.animation_frame += 1
            
            # Schedule next frame
            self.root.after(50, self._animate)
        
        except Exception as e:
            logger.error(f"Animation error: {e}")
    
    def set_state(self, state, message=None):
        """
        Change the GUI state.
        
        Args:
            state: New state (idle, listening, thinking, speaking, wake_word)
            message: Optional status message
        """
        if not self.ready or not self.root:
            return
        
        try:
            self.current_state = state
            
            # Update state text
            state_text = {
                self.STATE_IDLE: "Ready",
                self.STATE_LISTENING: "Listening...",
                self.STATE_THINKING: "Processing...",
                self.STATE_SPEAKING: "Speaking...",
                self.STATE_WAKE_WORD: "Waiting for wake word..."
            }.get(state, "Active")
            
            if message:
                state_text = message
            
            self.state_label.config(text=state_text)
            logger.debug(f"GUI state changed to: {state}")
        
        except Exception as e:
            logger.error(f"Failed to set GUI state: {e}")
    
    def show_message(self, message, duration=2000):
        """
        Show a temporary message.
        
        Args:
            message: Message to display
            duration: Duration in milliseconds
        """
        if not self.ready or not self.root:
            return
        
        try:
            original_text = self.state_label.cget("text")
            self.state_label.config(text=message)
            self.root.after(duration, lambda: self.state_label.config(text=original_text))
        except Exception as e:
            logger.error(f"Failed to show message: {e}")
    
    def stop(self):
        """Stop the GUI."""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        logger.info("GUI overlay stopped")


# Standalone test
if __name__ == "__main__":
    print("=== Zen GUI Test ===\n")
    print("Testing GUI overlay with state transitions...")
    
    gui = ZenGUI(position="bottom-right")
    gui.start()
    
    # Wait for GUI to be ready
    import time
    time.sleep(2)
    
    # Test state transitions
    states = [
        (ZenGUI.STATE_WAKE_WORD, "Waiting for wake word..."),
        (ZenGUI.STATE_LISTENING, "Listening to you..."),
        (ZenGUI.STATE_THINKING, "Processing your request..."),
        (ZenGUI.STATE_SPEAKING, "Speaking response..."),
        (ZenGUI.STATE_IDLE, "Ready for next command"),
    ]
    
    try:
        for state, message in states:
            print(f"State: {state}")
            gui.set_state(state, message)
            time.sleep(3)
        
        print("\n✓ GUI test complete! Close the window to exit.")
        
        # Keep running
        while gui.ready:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nStopping GUI...")
        gui.stop()
