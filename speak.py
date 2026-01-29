"""
Zen Voice Assistant - Text-to-Speech Module
Handles converting text to spoken audio output.
"""

import pyttsx3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechSynthesizer:
    """Handles text-to-speech conversion."""
    
    def __init__(self, rate=150, volume=0.9):
        """
        Initialize the text-to-speech engine.
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.engine = None
        self.rate = rate
        self.volume = volume
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine with error handling."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Try to set a pleasant voice (prefer female voice if available)
            voices = self.engine.getProperty('voices')
            if voices:
                # Select first available voice (can be customized)
                self.engine.setProperty('voice', voices[0].id)
                logger.info(f"Voice initialized: {voices[0].name}")
            
            logger.info("Text-to-speech engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    def speak(self, text):
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to speak
        """
        if not self.engine:
            logger.error("TTS engine not initialized.")
            return
        
        if not text:
            logger.warning("No text provided to speak.")
            return
        
        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
    
    def set_rate(self, rate):
        """Change the speech rate."""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """Change the volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            self.engine.setProperty('volume', self.volume)
    
    def list_voices(self):
        """List all available voices."""
        if not self.engine:
            return []
        voices = self.engine.getProperty('voices')
        return [(v.id, v.name) for v in voices]
    
    def set_voice(self, voice_id):
        """Set a specific voice by ID."""
        if self.engine:
            try:
                self.engine.setProperty('voice', voice_id)
                logger.info(f"Voice changed to: {voice_id}")
            except Exception as e:
                logger.error(f"Failed to set voice: {e}")


# Standalone test
if __name__ == "__main__":
    print("=== Zen Text-to-Speech Test ===")
    
    synthesizer = SpeechSynthesizer()
    
    # List available voices
    print("\nAvailable voices:")
    for voice_id, voice_name in synthesizer.list_voices():
        print(f"  - {voice_name}")
    
    # Test speech
    print("\nTesting speech output...")
    synthesizer.speak("Hello! I am Zen, your personal voice assistant. How can I help you today?")
    print("\nSpeech test complete!")
