"""
Zen Voice Assistant - Main Application (v4.0 Epic & Futuristic)
Orchestrates all components, including AI-driven tool use and vision capabilities.
"""

import threading
import time
import re
from listen import SpeechListener
from speak import SpeechSynthesizer
from brain import AIBrain
from tools import ZenTools
from config import Config
from daily_tasks import DailyTaskManager
from logger import get_logger, ZenLogger

# Initialize enhanced logging system
ZenLogger.initialize(
    log_level=Config.LOG_LEVEL,
    log_to_file=Config.LOG_TO_FILE,
    debug_mode=Config.DEBUG_MODE
)
logger = get_logger(__name__)

# --- Optional Module Imports ---
wake_word_available = False
gui_available = False
neural_gui_available = False
neural_voice_available = False
vision_available = False

try:
    if Config.WAKE_WORD_ENABLED:
        from wake_word import WakeWordDetector
        wake_word_available = True
        logger.info("Wake word detection module loaded.")
except ImportError as e:
    logger.warning(f"Wake word module not available: {e}")

try:
    if Config.GUI_ENABLED:
        if Config.GUI_MODE == 'neural':
            from gui_neural import NeuralGUI
            neural_gui_available = True
            logger.info("Neural GUI module loaded.")
        else:
            from gui import ZenGUI
            gui_available = True
            logger.info("Classic GUI module loaded.")
except ImportError as e:
    logger.warning(f"GUI module '{Config.GUI_MODE}' not available: {e}")

try:
    if Config.NEURAL_VOICE_ENABLED:
        from voice_neural import NeuralVoice
        neural_voice_available = True
        logger.info("Neural Voice module loaded.")
except ImportError as e:
    logger.warning(f"Neural Voice not available: {e}")

try:
    if Config.ENABLE_VISION:
        from ai_vision import AIVision
        vision_available = True
        logger.info("AI Vision module loaded.")
except ImportError as e:
    logger.warning(f"AI Vision module not available: {e}")


class ZenAssistant:
    """Main voice assistant orchestrator with AI-driven tool use and vision."""
    
    def __init__(self):
        """Initialize all components."""
        logger.info("Initializing Zen Voice Assistant v4.0 (Futuristic Edition)...")
        
        try:
            self.listener = SpeechListener()
            self.brain = AIBrain()
            self.tools = ZenTools()
            self.vision = None
            self.running = False
            
            if Config.ENABLE_VISION and vision_available:
                try:
                    self.vision = AIVision(provider=Config.VISION_PROVIDER)
                    logger.info("AI Vision system initialized.")
                except Exception as e:
                    logger.error(f"Failed to initialize AI Vision: {e}")
                    vision_available = False

            self._register_all_tools()
            self.brain.finish_initialization()

            if Config.NEURAL_VOICE_ENABLED and neural_voice_available:
                self.speaker = NeuralVoice()
            else:
                self.speaker = SpeechSynthesizer(rate=Config.SPEECH_RATE, volume=Config.SPEECH_VOLUME)
            
            self.task_manager = DailyTaskManager(Config.DAILY_TASK_FILE)
            self.gui = None
            self.wake_word_detector = None
            self.wake_word_mode = False
            
            if Config.GUI_ENABLED:
                self._initialize_gui()
            
            if Config.WAKE_WORD_ENABLED and wake_word_available:
                self._initialize_wake_word()
            
            logger.info("Zen Voice Assistant initialized successfully!")
            
        except Exception as e:
            logger.error(f"Fatal error during initialization: {e}", exc_info=True)
            raise

    def _initialize_gui(self):
        try:
            if Config.GUI_MODE == 'neural' and neural_gui_available:
                self.gui = NeuralGUI(theme=Config.GUI_THEME, opacity=Config.GUI_OPACITY, always_on_top=Config.GUI_ALWAYS_ON_TOP)
            elif gui_available:
                self.gui = ZenGUI(position=Config.GUI_POSITION, opacity=Config.GUI_OPACITY, always_on_top=Config.GUI_ALWAYS_ON_TOP)
            
            if self.gui:
                self.gui.start()
                logger.info(f"{Config.GUI_MODE.capitalize()} GUI initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize GUI: {e}")
            self.gui = None

    def _initialize_wake_word(self):
        try:
            self.wake_word_detector = WakeWordDetector(wake_words=[Config.WAKE_WORD, "activate"], sensitivity=Config.WAKE_WORD_SENSITIVITY, callback=self._on_wake_word)
            self.wake_word_mode = True
            logger.info("Wake word detection initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize wake word detector: {e}")
    
    def _register_all_tools(self):
        """Defines and registers all available tools with the AI brain."""
        logger.info("Registering AI tools...")
        
        # Register standard tools
        tool_methods = {
            "open_application": ("Opens a desktop application.", {"app_name": {"type": "string", "description": "e.g., 'notepad', 'chrome'"}}),
            "get_current_time": ("Gets the current date and time.", {}),
            "search_web": ("Searches Google.", {"query": {"type": "string", "description": "The search term."}}),
            "get_system_info": ("Gets computer CPU and memory usage.", {}),
            "set_volume": ("Sets system volume.", {"level": {"type": "integer", "description": "Volume from 0-100."}}),
            "shutdown_system": ("Shuts down the computer.", {"confirm": {"type": "boolean", "description": "Must be true."}}),
            "restart_system": ("Restarts the computer.", {"confirm": {"type": "boolean", "description": "Must be true."}}),
        }

        for name, (desc, props) in tool_methods.items():
            self.brain.register_tool(
                name=name,
                description=desc,
                function=getattr(self.tools, name),
                parameters={"type": "object", "properties": props, "required": list(props.keys())}
            )

        # Register vision tools if available
        if self.vision:
            self.brain.register_tool(
                name="analyze_screen",
                description="Analyzes the content of the screen and answers a question about it.",
                function=self.vision.analyze_screen,
                parameters={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question to ask about the screen's content."
                        }
                    },
                    "required": ["question"]
                }
            )
        
        logger.info(f"{len(self.brain.tools)} tools registered successfully.")

    def _on_wake_word(self):
        logger.info("Wake word detected - activating")
        if self.gui: self.gui.show_message("🎤 Activated", 1000)
        self.speaker.speak("Yes?")
        self._process_single_command()
    
    def process_input(self, user_input: str):
        if any(word in user_input.lower() for word in ["exit", "quit", "goodbye", "bye zen"]):
            self.speaker.speak("Goodbye! Have a great day!")
            self.running = False
            return

        try:
            if self.gui: self.gui.set_state("thinking")
            
            logger.info(f"Sending to AI: {user_input}")
            response = self.brain.get_response(user_input)
            
            content_to_speak = response.get("content", "I don't have a response.")
            
            if self.gui: self.gui.set_state("speaking")
            self.speaker.speak(content_to_speak)
            
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            self.speaker.speak("I'm sorry, I encountered an error.")
        finally:
            if self.running and self.gui:
                self.gui.set_state("idle" if not self.wake_word_mode else "wake_word")
    
    def _process_single_command(self):
        try:
            if self.gui: self.gui.set_state("listening")
            user_input = self.listener.listen(timeout=Config.LISTEN_TIMEOUT, phrase_time_limit=Config.PHRASE_TIME_LIMIT)
            
            if user_input:
                print(f"\nYou: {user_input}")
                self.process_input(user_input)
            elif self.gui:
                self.gui.set_state("wake_word")
        except Exception as e:
            logger.error(f"Error in single command processing: {e}")
            if self.gui: self.gui.set_state("wake_word")
    
    def _announce_daily_tasks(self):
        if Config.ANNOUNCE_TASKS_ON_STARTUP:
            try:
                summary = self.task_manager.get_task_summary()
                if "no pending tasks" not in summary.lower():
                     self.speaker.speak(summary)
            except Exception as e:
                logger.error(f"Failed to announce tasks: {e}")
    
    def run(self):
        self.running = True
        self.speaker.speak("Hello! I'm Zen, your AI assistant. How can I help?")
        self._announce_daily_tasks()
        
        print("\n" + "="*70 + "\n🎤 ZEN VOICE ASSISTANT - AI Tools & Vision Enabled\n" + "="*70)
        if self.wake_word_mode: print("\n💡 Wake Word Mode: Say 'Zen' to activate.")
        else: print("\n💡 Normal Mode: Ready for your command.")
        if self.gui: print("🎨 GUI: Visual feedback enabled.")
        print("\n" + "="*70 + "\n")
        
        if self.gui: self.gui.set_state("wake_word" if self.wake_word_mode else "idle")
        
        if self.wake_word_mode and self.wake_word_detector:
            self._run_wake_word_mode()
        else:
            self._run_normal_mode()
        
        if self.gui: self.gui.stop()
        logger.info("Zen Voice Assistant shutting down.")

    def _run_wake_word_mode(self):
        self.wake_word_detector.start()
        try:
            while self.running: time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
        finally:
            self.speaker.speak("Goodbye!")
            if self.wake_word_detector: self.wake_word_detector.stop()

    def _run_normal_mode(self):
        while self.running:
            try:
                if self.gui: self.gui.set_state("listening")
                user_input = self.listener.listen(timeout=Config.LISTEN_TIMEOUT, phrase_time_limit=Config.PHRASE_TIME_LIMIT)
                if user_input:
                    print(f"\n🗣️  You: {user_input}")
                    self.process_input(user_input)
                elif self.gui:
                    self.gui.set_state("idle")
            except KeyboardInterrupt:
                self.running = False
                self.speaker.speak("Goodbye!")
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                if self.gui: self.gui.set_state("idle")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        ZEN VOICE ASSISTANT v4.0 - Futuristic Edition     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    gui_status = "✗ Disabled"
    if Config.GUI_ENABLED:
        gui_mode = Config.GUI_MODE
        if (gui_mode == 'neural' and neural_gui_available) or (gui_mode == 'classic' and gui_available):
            gui_status = f"✓ Enabled ({gui_mode})"
        else:
            gui_status = f"✗ Enabled but '{gui_mode}' not available"

    print("🔧 Feature Status:")
    print(f"   • AI Provider: {Config.AI_PROVIDER.upper()}")
    print(f"   • GUI: {gui_status}")
    print(f"   • Neural Voice: {'✓ Enabled' if Config.NEURAL_VOICE_ENABLED and neural_voice_available else '✗ Disabled'}")
    print(f"   • Vision: {'✓ Enabled' if Config.ENABLE_VISION and vision_available else '✗ Disabled'}")
    print(f"   • Wake Word: {'✓ Enabled' if Config.WAKE_WORD_ENABLED and wake_word_available else '✗ Disabled'}")
    print()
    
    config_errors = Config.validate_config()
    if config_errors:
        for error in config_errors: print(f"   - {error}")
        return
    
    try:
        assistant = ZenAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
