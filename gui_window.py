"""
Zen Voice Assistant - GUI Window Mode
Interactive popup window for typing commands and seeing responses.
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
from brain import AIBrain
from speak import SpeechSynthesizer
from tools import ZenTools
from config import Config
from logger import get_logger
import re

logger = get_logger(__name__)


class ZenGUIWindow:
    """GUI window interface for Zen."""
    
    def __init__(self):
        """Initialize the GUI window."""
        self.root = tk.Tk()
        self.root.title("Zen Voice Assistant")
        self.root.geometry("600x500")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize components
        logger.info("Initializing Zen GUI Window...")
        self.speaker = SpeechSynthesizer(
            rate=Config.SPEECH_RATE,
            volume=Config.SPEECH_VOLUME
        )
        self.brain = AIBrain()
        self.tools = ZenTools()
        
        self._create_widgets()
        logger.info("Zen GUI Window ready!")
    
    def _create_widgets(self):
        """Create GUI widgets."""
        # Title
        title = tk.Label(
            self.root,
            text="🎤 ZEN VOICE ASSISTANT",
            font=("Segoe UI", 18, "bold"),
            bg='#1a1a1a',
            fg='#4CAF50'
        )
        title.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready to help!",
            font=("Segoe UI", 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        self.status_label.pack()
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg='#1a1a1a')
        chat_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Welcome message
        self._add_message("Zen", "Hello! I'm Zen, your AI assistant. Type your commands below!", "#4CAF50")
        self._add_message("Zen", "Try: 'What time is it?', 'Open Notepad', 'Tell me a joke'", "#4CAF50")
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#1a1a1a')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Input label
        input_label = tk.Label(
            input_frame,
            text="You:",
            font=("Segoe UI", 11, "bold"),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.input_entry.bind('<Return>', lambda e: self._send_message())
        self.input_entry.focus()
        
        # Send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 10, "bold"),
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._send_message
        )
        send_button.pack(side=tk.LEFT)
        
        # Quick action buttons
        action_frame = tk.Frame(self.root, bg='#1a1a1a')
        action_frame.pack(pady=(0, 10), padx=20, fill=tk.X)
        
        quick_commands = [
            ("⏰ Time", "What time is it?"),
            ("📝 Notepad", "Open Notepad"),
            ("💡 Joke", "Tell me a joke"),
            ("❌ Exit", "exit")
        ]
        
        for text, command in quick_commands:
            btn = tk.Button(
                action_frame,
                text=text,
                font=("Segoe UI", 9),
                bg='#333333',
                fg='white',
                relief=tk.FLAT,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda c=command: self._quick_command(c)
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def _add_message(self, sender, message, color="#ffffff"):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}: ", ('sender',))
        self.chat_display.tag_config('sender', foreground=color, font=("Segoe UI", 11, "bold"))
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _update_status(self, status):
        """Update the status label."""
        self.status_label.config(text=status)
    
    def _quick_command(self, command):
        """Execute a quick command."""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, command)
        self._send_message()
    
    def _check_keyword_commands(self, text: str) -> tuple:
        """Check for direct keyword commands."""
        text_lower = text.lower()
        
        # Exit
        if any(word in text_lower for word in ["exit", "quit", "goodbye"]):
            return True, "Goodbye! Have a great day!"
        
        # Open app
        if "open" in text_lower:
            match = re.search(r'open\s+(\w+)', text_lower)
            if match:
                app_name = match.group(1)
                result = self.tools.open_application(app_name)
                return True, result
        
        # Time
        if any(phrase in text_lower for phrase in ["what time", "current time", "time"]):
            result = self.tools.get_current_time()
            return True, result
        
        # Search
        if "search for" in text_lower or "search" in text_lower:
            match = re.search(r'search\s+(?:for\s+)?(.+)', text_lower)
            if match:
                query = match.group(1)
                result = self.tools.search_web(query)
                return True, result
        
        # System info
        if "system" in text_lower and ("info" in text_lower or "status" in text_lower):
            result = self.tools.get_system_info()
            return True, result
        
        return False, None
    
    def _process_in_thread(self, user_input):
        """Process input in a separate thread."""
        try:
            # Check keyword commands
            is_keyword, result = self._check_keyword_commands(user_input)
            
            if is_keyword:
                self._add_message("Zen", result, "#4CAF50")
                self.speaker.speak(result)
                self._update_status("Ready")
                
                if any(word in user_input.lower() for word in ["exit", "quit", "goodbye"]):
                    self.root.after(2000, self.root.destroy)
                return
            
            # Send to AI
            self._update_status("Thinking...")
            logger.info(f"Sending to AI: {user_input}")
            response = self.brain.get_response(user_input)
            
            if response["type"] == "text":
                self._add_message("Zen", response["content"], "#4CAF50")
                self._update_status("Speaking...")
                self.speaker.speak(response["content"])
                self._update_status("Ready")
        
        except Exception as e:
            logger.error(f"Error: {e}")
            msg = "Sorry, I encountered an error."
            self._add_message("Zen", msg, "#F44336")
            self.speaker.speak(msg)
            self._update_status("Ready")
    
    def _send_message(self):
        """Handle sending a message."""
        user_input = self.input_entry.get().strip()
        
        if not user_input:
            return
        
        # Add user message
        self._add_message("You", user_input, "#2196F3")
        self.input_entry.delete(0, tk.END)
        
        # Process in separate thread
        self._update_status("Processing...")
        thread = threading.Thread(target=self._process_in_thread, args=(user_input,), daemon=True)
        thread.start()
    
    def run(self):
        """Start the GUI."""
        self.root.mainloop()


def main():
    """Entry point."""
    try:
        app = ZenGUIWindow()
        app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
