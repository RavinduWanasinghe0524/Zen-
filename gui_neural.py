"""
Zen Voice Assistant - Neural Holographic GUI
Futuristic 3D interface with holographic effects, particle systems, and neural visualizations.
"""

import tkinter as tk
from tkinter import ttk
import threading
import math
import random
import time
from typing import List, Tuple
from logger import get_logger

logger = get_logger(__name__)


class Particle:
    """Particle for ambient effects."""
    
    def __init__(self, x, y, vx, vy, size, color, lifetime=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.age = 0
        self.alpha = 1.0
    
    def update(self):
        """Update particle position and age."""
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        self.alpha = 1.0 - (self.age / self.lifetime)
        return self.age < self.lifetime


class NeuralGUI:
    """Advanced futuristic GUI with holographic effects."""
    
    # State constants
    STATE_IDLE = "idle"
    STATE_LISTENING = "listening"
    STATE_THINKING = "thinking"
    STATE_SPEAKING = "speaking"
    STATE_WAKE_WORD = "wake_word"
    
    def __init__(self, theme="cyber_blue", position="bottom-right", opacity=0.95, always_on_top=True):
        """
        Initialize the neural GUI.
        
        Args:
            theme: Visual theme (cyber_blue, neural_purple, quantum_orange, dark_matter)
            position: Window position
            opacity: Window opacity
            always_on_top: Keep window on top
        """
        self.theme_name = theme
        self.position = position
        self.opacity = opacity
        self.always_on_top = always_on_top
        self.current_state = self.STATE_IDLE
        self.animation_frame = 0
        self.particles = []
        self.neural_nodes = []
        
        # Theme configurations
        self.themes = {
            "cyber_blue": {
                "primary": "#00F0FF",
                "secondary": "#0080FF",
                "accent": "#00FFAA",
                "bg": "#0A0E1A",
                "glow": "#00F0FF"
            },
            "neural_purple": {
                "primary": "#B026FF",
                "secondary": "#FF10F0",
                "accent": "#FFB6C1",
                "bg": "#1A0A1E",
                "glow": "#FF10F0"
            },
            "quantum_orange": {
                "primary": "#FF8C00",
                "secondary": "#FFD700",
                "accent": "#FFA500",
                "bg": "#1A1410",
                "glow": "#FFD700"
            },
            "dark_matter": {
                "primary": "#FFFFFF",
                "secondary": "#00FFFF",
                "accent": "#FF00FF",
                "bg": "#000000",
                "glow": "#00FFFF"
            }
        }
        
        self.theme = self.themes.get(theme, self.themes["cyber_blue"])
        
        # Window setup
        self.root = None
        self.gui_thread = None
        self.ready = False
        self.running = True
        
        # Initialize neural network visualization
        self._init_neural_network()
    
    def _init_neural_network(self):
        """Initialize neural network node positions."""
        layers = [3, 5, 4, 2]  # Neural network structure
        self.neural_nodes = []
        
        for layer_idx, num_nodes in enumerate(layers):
            for node_idx in range(num_nodes):
                x = 50 + layer_idx * 100
                y = 100 + (node_idx - num_nodes/2) * 40
                self.neural_nodes.append((x, y, layer_idx))
    
    def start(self):
        """Start the GUI in a separate thread."""
        self.gui_thread = threading.Thread(target=self._create_window, daemon=True)
        self.gui_thread.start()
        
        # Wait for GUI to be ready
        for _ in range(50):
            if self.ready:
                break
            time.sleep(0.1)
        
        logger.info("Neural GUI started with theme: {}".format(self.theme_name))
    
    def _create_window(self):
        """Create the tkinter window with futuristic design."""
        try:
            self.root = tk.Tk()
            self.root.title("Zen Neural Interface")
            
            # Window dimensions
            width = 450
            height = 400
            
            # Calculate position
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if "right" in self.position:
                x = screen_width - width - 30
            else:
                x = 30
            
            if "bottom" in self.position:
                y = screen_height - height - 80
            else:
                y = 80
            
            # Configure window
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            self.root.attributes("-alpha", self.opacity)
            self.root.attributes("-topmost", self.always_on_top)
            self.root.overrideredirect(True)
            self.root.configure(bg=self.theme["bg"])
            
            # Main frame with border glow effect
            main_frame = tk.Frame(
                self.root,
                bg=self.theme["bg"],
                highlightbackground=self.theme["primary"],
                highlightthickness=2
            )
            main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            # Create canvas for animations
            self.canvas = tk.Canvas(
                main_frame,
                width=width-10,
                height=height-80,
                bg=self.theme["bg"],
                highlightthickness=0
            )
            self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Status panel at bottom
            status_frame = tk.Frame(main_frame, bg=self.theme["bg"])
            status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # ZEN logo with glow effect
            self.logo_label = tk.Label(
                status_frame,
                text="⚡ ZEN NEURAL",
                font=("Consolas", 14, "bold"),
                bg=self.theme["bg"],
                fg=self.theme["primary"]
            )
            self.logo_label.pack(side=tk.LEFT)
            
            # Status indicator
            self.status_label = tk.Label(
                status_frame,
                text="● ONLINE",
                font=("Consolas", 10),
                bg=self.theme["bg"],
                fg=self.theme["accent"]
            )
            self.status_label.pack(side=tk.RIGHT)
            
            # State text with cyberpunk style
            self.state_label = tk.Label(
                status_frame,
                text="STANDBY",
                font=("Consolas", 12, "bold"),
                bg=self.theme["bg"],
                fg=self.theme["secondary"]
            )
            self.state_label.pack(side=tk.TOP, pady=5)
            
            # Control buttons with futuristic style
            control_frame = tk.Frame(main_frame, bg=self.theme["bg"])
            control_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
            
            # Minimize button
            min_btn = tk.Label(
                control_frame,
                text="▼",
                font=("Arial", 10, "bold"),
                bg=self.theme["bg"],
                fg=self.theme["secondary"],
                cursor="hand2"
            )
            min_btn.pack(side=tk.LEFT, padx=2)
            min_btn.bind("<Button-1>", lambda e: self.root.iconify())
            
            # Theme cycle button
            theme_btn = tk.Label(
                control_frame,
                text="◐",
                font=("Arial", 12, "bold"),
                bg=self.theme["bg"],
                fg=self.theme["accent"],
                cursor="hand2"
            )
            theme_btn.pack(side=tk.LEFT, padx=2)
            theme_btn.bind("<Button-1>", lambda e: self._cycle_theme())
            
            # Close button
            close_btn = tk.Label(
                control_frame,
                text="✕",
                font=("Arial", 12, "bold"),
                bg=self.theme["bg"],
                fg="#FF4444",
                cursor="hand2"
            )
            close_btn.pack(side=tk.RIGHT, padx=2)
            close_btn.bind("<Button-1>", lambda e: self.stop())
            
            # Make window draggable
            self.canvas.bind("<Button-1>", self._start_drag)
            self.canvas.bind("<B1-Motion>", self._on_drag)
            
            self.ready = True
            
            # Start animations
            self._animate()
            self._update_particles()
            
            # Start tkinter main loop
            self.root.mainloop()
        
        except Exception as e:
            logger.error(f"Failed to create neural GUI: {e}")
    
    def _cycle_theme(self):
        """Cycle through available themes."""
        theme_names = list(self.themes.keys())
        current_idx = theme_names.index(self.theme_name)
        next_idx = (current_idx + 1) % len(theme_names)
        self.theme_name = theme_names[next_idx]
        self.theme = self.themes[self.theme_name]
        
        # Update colors
        self.root.configure(bg=self.theme["bg"])
        logger.info(f"Theme changed to: {self.theme_name}")
    
    def _start_drag(self, event):
        """Start dragging the window."""
        self.drag_x = event.x
        self.drag_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging."""
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")
    
    def _create_particles(self, count=5):
        """Create ambient particles."""
        width = 430
        height = 320
        
        for _ in range(count):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-1, -0.2)
            size = random.uniform(1, 3)
            self.particles.append(Particle(x, y, vx, vy, size, self.theme["accent"], random.randint(60, 120)))
    
    def _update_particles(self):
        """Update particle system."""
        if not self.root or not self.running:
            return
        
        try:
            # Add new particles occasionally
            if random.random() < 0.3 and len(self.particles) < 30:
                self._create_particles(2)
            
            # Update and remove dead particles
            self.particles = [p for p in self.particles if p.update()]
            
            # Schedule next update
            self.root.after(50, self._update_particles)
        except:
            pass
    
    def _animate(self):
        """Main animation loop with futuristic effects."""
        if not self.root or not self.running:
            return
        
        try:
            self.canvas.delete("all")
            
            width = 430
            height = 320
            center_x = width // 2
            center_y = height // 2
            
            # Draw particles
            for particle in self.particles:
                alpha_val = int(particle.alpha * 255)
                color = self._hex_to_rgb_alpha(particle.color, alpha_val)
                self.canvas.create_oval(
                    particle.x - particle.size, particle.y - particle.size,
                    particle.x + particle.size, particle.y + particle.size,
                    fill=color, outline=""
                )
            
            # State-specific visualizations
            if self.current_state == self.STATE_IDLE or self.current_state == self.STATE_WAKE_WORD:
                self._draw_idle_state(center_x, center_y)
            
            elif self.current_state == self.STATE_LISTENING:
                self._draw_listening_state(center_x, center_y)
            
            elif self.current_state == self.STATE_THINKING:
                self._draw_thinking_state(center_x, center_y)
            
            elif self.current_state == self.STATE_SPEAKING:
                self._draw_speaking_state(center_x, center_y)
            
            self.animation_frame += 1
            
            # Schedule next frame (60 FPS target)
            self.root.after(16, self._animate)
        
        except Exception as e:
            logger.error(f"Animation error: {e}")
    
    def _draw_idle_state(self, cx, cy):
        """Draw idle state with pulsing holographic circle."""
        pulse = math.sin(self.animation_frame * 0.05) * 0.3 + 0.7
        radius = 60 * pulse
        
        # Outer glow rings
        for i in range(3):
            r = radius + i * 15
            alpha = int((1 - i * 0.3) * 100)
            color = self._hex_to_rgb_alpha(self.theme["glow"], alpha)
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=color, width=2
            )
        
        # Inner filled circle
        self.canvas.create_oval(
            cx - radius, cy - radius, cx + radius, cy + radius,
            fill=self.theme["primary"], outline=self.theme["glow"], width=3
        )
        
        # Central dot
        self.canvas.create_oval(
            cx - 8, cy - 8, cx + 8, cy + 8,
            fill=self.theme["bg"], outline=self.theme["accent"], width=2
        )
    
    def _draw_listening_state(self, cx, cy):
        """Draw listening state with audio waveform visualization."""
        # Futuristic audio bars
        num_bars = 16
        bar_width = 15
        spacing = 25
        
        start_x = cx - (num_bars * spacing) // 2
        
        for i in range(num_bars):
            x = start_x + i * spacing
            
            # Multiple frequency components
            height1 = abs(math.sin(self.animation_frame * 0.15 + i * 0.4)) * 80
            height2 = abs(math.sin(self.animation_frame * 0.2 + i * 0.6)) * 50
            height = max(height1, height2) + 20
            
            # Gradient effect with multiple rectangles
            for j in range(int(height // 5)):
                y_offset = j * 5
                alpha = int(255 * (1 - j / (height / 5)))
                color = self._hex_to_rgb_alpha(self.theme["primary"], alpha)
                
                self.canvas.create_rectangle(
                    x, cy - y_offset, x + bar_width, cy - y_offset - 5,
                    fill=color, outline=""
                )
                self.canvas.create_rectangle(
                    x, cy + y_offset, x + bar_width, cy + y_offset + 5,
                    fill=color, outline=""
                )
        
        # Center line
        self.canvas.create_line(
            50, cy, width - 50, cy,
            fill=self.theme["glow"], width=2
        )
    
    def _draw_thinking_state(self, cx, cy):
        """Draw thinking state with neural network visualization."""
        # Draw neural connections with flowing energy
        for i, (x1, y1, layer1) in enumerate(self.neural_nodes):
            for j, (x2, y2, layer2) in enumerate(self.neural_nodes):
                if layer2 == layer1 + 1:  # Connect to next layer
                    # Animated energy flow
                    flow = (self.animation_frame * 2 + i * 10 + j * 5) % 100
                    alpha = int(abs(math.sin(flow * 0.1)) * 150)
                    color = self._hex_to_rgb_alpha(self.theme["secondary"], alpha)
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=color, width=2, smooth=True
                    )
        
        # Draw nodes with pulsing effect
        for x, y, layer in self.neural_nodes:
            pulse = abs(math.sin(self.animation_frame * 0.08 + layer * 0.5))
            size = 6 + pulse * 4
            
            # Outer glow
            self.canvas.create_oval(
                x - size - 4, y - size - 4,
                x + size + 4, y + size + 4,
                fill="", outline=self.theme["glow"], width=2
            )
            
            # Node core
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=self.theme["primary"], outline=self.theme["accent"], width=2
            )
    
    def _draw_speaking_state(self, cx, cy):
        """Draw speaking state with expanding sonic rings."""
        # Multiple expanding rings
        num_rings = 5
        
        for i in range(num_rings):
            offset = (self.animation_frame * 3 + i * 20) % 150
            radius = 30 + offset
            alpha = int((1 - offset / 150) * 200)
            color = self._hex_to_rgb_alpha(self.theme["primary"], alpha)
            
            self.canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                outline=color, width=4
            )
        
        # Central speaker icon effect
        speaker_size = 40
        for i in range(3):
            angle_offset = (self.animation_frame * 0.1 + i * (2 * math.pi / 3)) % (2 * math.pi)
            x = cx + math.cos(angle_offset) * 25
            y = cy + math.sin(angle_offset) * 25
            
            self.canvas.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                fill=self.theme["accent"], outline=self.theme["glow"], width=2
            )
    
    def _hex_to_rgb_alpha(self, hex_color, alpha):
        """Convert hex color to RGB with alpha for tkinter."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Tkinter doesn't support alpha directly, so we'll blend with background
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def set_state(self, state, message=None):
        """Change the GUI state with futuristic updates."""
        if not self.ready or not self.root:
            return
        
        try:
            self.current_state = state
            
            # State text mapping with cyberpunk style
            state_text = {
                self.STATE_IDLE: "STANDBY",
                self.STATE_LISTENING: ">>> LISTENING <<<",
                self.STATE_THINKING: "◆ PROCESSING ◆",
                self.STATE_SPEAKING: "▶ TRANSMITTING ▶",
                self.STATE_WAKE_WORD: "◉ MONITORING ◉"
            }.get(state, "ACTIVE")
            
            if message:
                state_text = message.upper()
            
            self.state_label.config(text=state_text, fg=self.theme["secondary"])
            logger.debug(f"Neural GUI state: {state}")
        
        except Exception as e:
            logger.error(f"Failed to set neural GUI state: {e}")
    
    def show_message(self, message, duration=2000):
        """Show a temporary message."""
        if not self.ready or not self.root:
            return
        
        try:
            original_text = self.state_label.cget("text")
            self.state_label.config(text=message.upper(), fg=self.theme["accent"])
            self.root.after(duration, lambda: self.state_label.config(text=original_text, fg=self.theme["secondary"]))
        except Exception as e:
            logger.error(f"Failed to show message: {e}")
    
    def stop(self):
        """Stop the neural GUI."""
        self.running = False
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        logger.info("Neural GUI stopped")


# Standalone test
if __name__ == "__main__":
    print("=== Zen Neural GUI Test ===\n")
    print("Testing futuristic holographic interface...\n")
    
    # Test all themes
    for theme in ["cyber_blue", "neural_purple", "quantum_orange", "dark_matter"]:
        print(f"Testing theme: {theme}")
        gui = NeuralGUI(theme=theme, position="bottom-right")
        gui.start()
        
        time.sleep(2)
        
        # Test state transitions
        states = [
            (NeuralGUI.STATE_WAKE_WORD, "Waiting..."),
            (NeuralGUI.STATE_LISTENING, "Listening..."),
            (NeuralGUI.STATE_THINKING, "Processing..."),
            (NeuralGUI.STATE_SPEAKING, "Speaking..."),
            (NeuralGUI.STATE_IDLE, "Ready"),
        ]
        
        for state, msg in states:
            gui.set_state(state, msg)
            time.sleep(2)
        
        gui.stop()
        time.sleep(1)
    
    print("\n✓ Neural GUI test complete!")
