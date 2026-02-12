from PySide6.QtCore import QObject, Signal, Slot
import logging
from brain import AIBrain

logger = logging.getLogger(__name__)

class WorkerBrain(QObject):
    signal_response_ready = Signal(str) # AI response text
    signal_action_required = Signal(dict) # Tool/Action execution
    signal_error = Signal(str)
    
    def __init__(self):
        super().__init__()
        try:
            # We initialize Brain here. 
            # Note: AIBrain might have thread-affinity issues if it uses asyncio loop?
            # Gemini client usually is thread-safe or creates its own context.
            self.brain = AIBrain()
            self.brain.finish_initialization()
        except Exception as e:
            logger.error(f"Failed to initialize Brain: {e}")

    @Slot(str)
    def process_text(self, text):
        """Process incoming text in the worker thread."""
        try:
            logger.info(f"Brain processing: {text}")
            response = self.brain.get_response(text)
            
            if response['type'] == 'text':
                self.signal_response_ready.emit(response['content'])
            elif response['type'] == 'tool_call':
                self.signal_response_ready.emit(str(response['content']))
                
        except Exception as e:
            error_msg = f"Brain Error: {e}"
            logger.error(error_msg)
            self.signal_error.emit(error_msg)
