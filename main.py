"""
Zen Voice Assistant - Main Application (Phase 4 Enhanced)
Orchestrates all components with wake word detection, GUI overlay, and advanced features.
"""

import threading
import re
from listen import SpeechListener
from speak import SpeechSynthesizer
from brain import AIBrain
from tools import ZenTools
from config import Config
from logger import get_logger, ZenLogger

# Initialize enhanced logging system
ZenLogger.initialize(
    log_level=Config.LOG_LEVEL,
    log_to_file=Config.LOG_TO_FILE,
    debug_mode=Config.DEBUG_MODE
)

logger = get_logger(__name__)

# Optional Phase 4 imports with graceful degradation
wake_word_available = False
gui_available = False

try:
    if Config.WAKE_WORD_ENABLED:
        from wake_word import WakeWordDetector
        wake_word_available = True
        logger.info("Wake word detection module loaded")
except ImportError as e:
    logger.warning(f"Wake word detection not available: {e}")

try:
    if Config.GUI_ENABLED:
        from gui import ZenGUI
        gui_available = True
        logger.info("GUI overlay module loaded")
except ImportError as e:
    logger.warning(f"GUI overlay not available: {e}")


class ZenAssistant:
    """Main voice assistant orchestrator with Phase 4 enhancements."""
    
    def __init__(self):
        """Initialize all components."""
        logger.info("Initializing Zen Voice Assistant v2.0...")
        
        try:
            # Core components
            self.listener = SpeechListener()
            self.speaker = SpeechSynthesizer(
                rate=Config.SPEECH_RATE,
                volume=Config.SPEECH_VOLUME
            )
            self.brain = AIBrain()
            self.tools = ZenTools()
            self.running = False
            
            # Phase 4: Optional components
            self.gui = None
            self.wake_word_detector = None
            self.wake_word_mode = False
            
            # Initialize GUI if enabled and available
            if Config.GUI_ENABLED and gui_available:
                try:
                    self.gui = ZenGUI(
                        position=Config.GUI_POSITION,
                        opacity=Config.GUI_OPACITY,
                        always_on_top=Config.GUI_ALWAYS_ON_TOP
                    )
                    self.gui.start()
                    logger.info("GUI overlay initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize GUI: {e}")
                    self.gui = None
            
            # Initialize wake word detector if enabled and available
            if Config.WAKE_WORD_ENABLED and wake_word_available:
                try:
                    self.wake_word_detector = WakeWordDetector(
                        wake_word=Config.WAKE_WORD,
                        sensitivity=Config.WAKE_WORD_SENSITIVITY,
                        callback=self._on_wake_word
                    )
                    self.wake_word_mode = True
                    logger.info("Wake word detection initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize wake word detection: {e}")
                    self.wake_word_detector = None
                    self.wake_word_mode = False
            
            logger.info("Zen Voice Assistant initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize Zen: {e}", exc_info=True)
            raise
    
    def _on_wake_word(self):
        """Callback when wake word is detected."""
        logger.info("Wake word detected - activating")
        if self.gui:
            self.gui.show_message("🎤 Activated", 1000)
        self.speaker.speak("Yes?")
        # Process one command then go back to wake word mode
        self._process_single_command()
    
    def _check_keyword_commands(self, text: str) -> bool:
        """
        Check for direct keyword commands and execute them.
        
        Args:
            text: User's input text
            
        Returns:
            True if a command was executed, False otherwise
        """
        text_lower = text.lower()
        
        # Exit commands
        if any(word in text_lower for word in ["exit", "quit", "goodbye", "bye zen"]):
            self.speaker.speak("Goodbye! Have a great day!")
            self.running = False
            return True
        
        # Open application commands
        if "open" in text_lower:
            # Extract app name
            match = re.search(r'open\s+(\w+)', text_lower)
            if match:
                app_name = match.group(1)
                result = self.tools.open_application(app_name)
                self.speaker.speak(result)
                return True
        
        # Time command
        if any(phrase in text_lower for phrase in ["what time", "current time", "what's the time"]):
            result = self.tools.get_current_time()
            self.speaker.speak(result)
            return True
        
        # Search web command
        if "search for" in text_lower or ("search" in text_lower and "google" in text_lower):
            match = re.search(r'search\s+(?:for\s+)?(.+)', text_lower)
            if match:
                query = match.group(1)
                result = self.tools.search_web(query)
                self.speaker.speak(result)
                return True
        
        # System info command
        if "system" in text_lower and ("info" in text_lower or "status" in text_lower):
            result = self.tools.get_system_info()
            self.speaker.speak(result)
            return True
        
        return False
    
    def process_input(self, user_input: str):
        """
        Process user input and generate response.
        
        Args:
            user_input: User's speech as text
        """
        try:
            # Update GUI state
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_THINKING)
            
            # First check for direct keyword commands
            if self._check_keyword_commands(user_input):
                if self.gui:
                    self.gui.set_state(ZenGUI.STATE_IDLE if not self.wake_word_mode else ZenGUI.STATE_WAKE_WORD)
                return
            
            # If no keyword command, send to AI brain
            logger.info(f"Sending to AI: {user_input}")
            response = self.brain.get_response(user_input)
            
            # Update GUI to speaking state
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_SPEAKING)
            
            if response["type"] == "text":
                self.speaker.speak(response["content"])
            elif response["type"] == "tool_call":
                # Handle tool calls
                tool_result = response["content"]
                self.speaker.speak(tool_result)
            
            # Return to idle
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_IDLE if not self.wake_word_mode else ZenGUI.STATE_WAKE_WORD)
            
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            self.speaker.speak("I'm sorry, I encountered an error processing that.")
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_IDLE if not self.wake_word_mode else ZenGUI.STATE_WAKE_WORD)
    
    def _process_single_command(self):
        """Process a single voice command (used by wake word mode)."""
        try:
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_LISTENING)
            
            user_input = self.listener.listen(
                timeout=Config.LISTEN_TIMEOUT,
                phrase_time_limit=Config.PHRASE_TIME_LIMIT
            )
            
            if user_input:
                print(f"\nYou: {user_input}")
                self.process_input(user_input)
            else:
                if self.gui:
                    self.gui.set_state(ZenGUI.STATE_WAKE_WORD)
                    
        except Exception as e:
            logger.error(f"Error in single command processing: {e}")
            if self.gui:
                self.gui.set_state(ZenGUI.STATE_WAKE_WORD)
    
    def run(self):
        """Main conversation loop."""
        self.running = True
        
        # Greet the user
        if self.wake_word_mode:
            greeting = f"Hello! I'm Zen. Say '{Config.WAKE_WORD}' or 'Hey {Config.WAKE_WORD}' to activate me."
        else:
            greeting = "Hello! I'm Zen, your voice assistant. How can I help you today?"
        
        print(f"\n{greeting}")
        self.speaker.speak(greeting)
        
        print("\n" + "="*70)
        print("🎤 ZEN VOICE ASSISTANT - Ready")
        print("="*70)
        
        if self.wake_word_mode:
            print(f"\n💡 Wake Word Mode: Say '{Config.WAKE_WORD}' to activate")
            print(f"   (Listening passively...)")
        else:
            print("\n📝 Available Commands:")
            print("   • 'Open Notepad' / 'Open Calculator' / 'Open Chrome'")
            print("   • 'What time is it?'")
            print("   • 'Search for [topic]'")
            print("   • 'What's the system status?'")
            print("   • Ask me anything!")
            print("   • Say 'exit' or 'goodbye' to quit")
        
        if self.gui:
            print("\n🎨 GUI: Visual feedback enabled")
            print("   (Look for the overlay in the corner of your screen)")
        
        print("\n" + "="*70 + "\n")
        
        # Set initial GUI state
        if self.gui:
            self.gui.set_state(ZenGUI.STATE_WAKE_WORD if self.wake_word_mode else ZenGUI.STATE_IDLE)
        
        # Wake word mode: Start passive listening
        if self.wake_word_mode and self.wake_word_detector:
            logger.info("Starting in wake word mode")
            self.wake_word_detector.start()
            
            # Keep running while wake word detector is active
            try:
                import time
                while self.running:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                self.speaker.speak("Shutting down. Goodbye!")
            finally:
                if self.wake_word_detector:
                    self.wake_word_detector.stop()
        
        # Normal mode: Continuous listening
        else:
            while self.running:
                try:
                    # Update GUI state
                    if self.gui:
                        self.gui.set_state(ZenGUI.STATE_LISTENING)
                    
                    # Listen for user input
                    user_input = self.listener.listen(
                        timeout=Config.LISTEN_TIMEOUT,
                        phrase_time_limit=Config.PHRASE_TIME_LIMIT
                    )
                    
                    if user_input:
                        print(f"\n🗣️  You: {user_input}")
                        self.process_input(user_input)
                        print()  # Add spacing
                    else:
                        # No speech detected, return to idle
                        if self.gui:
                            self.gui.set_state(ZenGUI.STATE_IDLE)
                        continue
                        
                except KeyboardInterrupt:
                    print("\n\nInterrupted by user.")
                    self.speaker.speak("Shutting down. Goodbye!")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}", exc_info=True)
                    self.speaker.speak("I encountered an error. Let me try again.")
                    if self.gui:
                        self.gui.set_state(ZenGUI.STATE_IDLE)
        
        # Cleanup
        if self.gui:
            self.gui.stop()
        
        logger.info("Zen Voice Assistant shutting down.")


def main():
    """Entry point for the application."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          ZEN VOICE ASSISTANT v2.0 (Phase 4)             ║
    ║          Your Personal AI Companion                      ║
    ║                                                          ║
    ║    ✨ Wake Word Detection  🎨 Visual Feedback           ║
    ║    ⚡ Performance Optimized  📊 Enhanced Logging        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Display feature status
    print("🔧 Feature Status:")
    print(f"   • AI Provider: {Config.AI_PROVIDER.upper()}")
    print(f"   • Wake Word: {'✓ Enabled' if Config.WAKE_WORD_ENABLED and wake_word_available else '✗ Disabled'}")
    print(f"   • GUI Overlay: {'✓ Enabled' if Config.GUI_ENABLED and gui_available else '✗ Disabled'}")
    print(f"   • Logging: {'✓ File & Console' if Config.LOG_TO_FILE else '✓ Console Only'}")
    print()
    
    # Validate configuration
    config_errors = Config.validate_config()
    if config_errors:
        print("\n⚠️  Configuration Errors:")
        for error in config_errors:
            print(f"   - {error}")
        print("\n💡 Please fix these errors in your .env file before running Zen.")
        print("   Run 'python setup.py' for quick setup or edit .env manually.")
        return
    
    try:
        assistant = ZenAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Configure .env with your API key (run: python setup.py)")
        print("   3. Ensure microphone is connected")
        print("   4. Check logs/ directory for detailed error information")


if __name__ == "__main__":
    main()
