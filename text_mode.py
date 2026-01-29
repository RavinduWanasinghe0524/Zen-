"""
Zen Voice Assistant - Text Mode (Keyboard Input)
Alternative input mode for testing and development without microphone.
"""

import sys
from brain import AIBrain
from speak import SpeechSynthesizer
from tools import ZenTools
from config import Config
from logger import get_logger
import re

logger = get_logger(__name__)


class ZenTextMode:
    """Text-based voice assistant for testing."""
    
    def __init__(self):
        """Initialize components."""
        logger.info("Initializing Zen in Text Mode...")
        
        self.speaker = SpeechSynthesizer(
            rate=Config.SPEECH_RATE,
            volume=Config.SPEECH_VOLUME
        )
        self.brain = AIBrain()
        self.tools = ZenTools()
        self.running = False
        
        logger.info("Zen Text Mode initialized!")
    
    def _check_keyword_commands(self, text: str) -> bool:
        """Check for direct keyword commands."""
        text_lower = text.lower()
        
        # Exit commands
        if any(word in text_lower for word in ["exit", "quit", "goodbye"]):
            self.speaker.speak("Goodbye! Have a great day!")
            self.running = False
            return True
        
        # Open application
        if "open" in text_lower:
            match = re.search(r'open\s+(\w+)', text_lower)
            if match:
                app_name = match.group(1)
                result = self.tools.open_application(app_name)
                print(f"Zen: {result}")
                self.speaker.speak(result)
                return True
        
        # Time command
        if any(phrase in text_lower for phrase in ["what time", "current time", "time"]):
            result = self.tools.get_current_time()
            print(f"Zen: {result}")
            self.speaker.speak(result)
            return True
        
        # Search web
        if "search for" in text_lower or "search" in text_lower:
            match = re.search(r'search\s+(?:for\s+)?(.+)', text_lower)
            if match:
                query = match.group(1)
                result = self.tools.search_web(query)
                print(f"Zen: {result}")
                self.speaker.speak(result)
                return True
        
        # System info
        if "system" in text_lower and ("info" in text_lower or "status" in text_lower):
            result = self.tools.get_system_info()
            print(f"Zen: {result}")
            self.speaker.speak(result)
            return True
        
        return False
    
    def process_input(self, user_input: str):
        """Process text input."""
        try:
            # Check keyword commands first
            if self._check_keyword_commands(user_input):
                return
            
            # Send to AI
            logger.info(f"Sending to AI: {user_input}")
            print("Zen: [Thinking...]")
            response = self.brain.get_response(user_input)
            
            if response["type"] == "text":
                print(f"Zen: {response['content']}")
                self.speaker.speak(response["content"])
        
        except Exception as e:
            logger.error(f"Error: {e}")
            msg = "Sorry, I encountered an error."
            print(f"Zen: {msg}")
            self.speaker.speak(msg)
    
    def run(self):
        """Main text input loop."""
        self.running = True
        
        print("""
╔══════════════════════════════════════════════════╗
║                                                  ║
║     ZEN VOICE ASSISTANT - TEXT MODE              ║
║     Type instead of speak                        ║
║                                                  ║
╚══════════════════════════════════════════════════╝

TEXT MODE: Type your commands instead of speaking.
This mode helps test Zen without microphone issues.

Available Commands:
  - "What time is it?"
  - "Open Notepad"
  - "Search for Python tutorials"
  - "What's the system status?"
  - Ask anything!
  - Type "exit" to quit

═════════════════════════════════════════════════════
""")
        
        greeting = "Hello! I'm Zen in text mode. Type your commands!"
        print(f"Zen: {greeting}")
        self.speaker.speak(greeting)
        
        while self.running:
            try:
                # Get text input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                self.process_input(user_input)
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.speaker.speak("Goodbye!")
                break
            except EOFError:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")


def main():
    """Entry point."""
    try:
        assistant = ZenTextMode()
        assistant.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
