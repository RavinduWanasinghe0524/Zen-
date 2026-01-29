"""
Zen Voice Assistant - Speech Recognition Module
Handles microphone input and converts speech to text.
"""

import speech_recognition as sr
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechListener:
    """Handles speech-to-text conversion using microphone input."""
    
    def __init__(self):
        """Initialize the speech recognizer and microphone."""
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """Initialize the microphone with error handling."""
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Calibrating for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            raise
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for speech and convert to text.
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            str: Transcribed text, or None if recognition failed
        """
        if not self.microphone:
            logger.error("Microphone not initialized.")
            return None
        
        try:
            with self.microphone as source:
                logger.info("Listening...")
                # Listen for audio input
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.info("Processing speech...")
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out - no speech detected.")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio.")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during speech recognition: {e}")
            return None


# Standalone test
if __name__ == "__main__":
    print("=== Zen Speech Recognition Test ===")
    print("Speak into your microphone...")
    
    listener = SpeechListener()
    result = listener.listen()
    
    if result:
        print(f"\nYou said: {result}")
    else:
        print("\nFailed to recognize speech.")
