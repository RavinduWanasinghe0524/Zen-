"""
Zen Voice Assistant - Wake Word Detection Module
Passive listening for "Hey Zen" activation.
"""

import threading
import time
from logger import get_logger

logger = get_logger(__name__)


class WakeWordDetector:
    """Handles wake word detection for passive activation."""
    
    def __init__(self, wake_word="zen", sensitivity=0.5, callback=None):
        """
        Initialize wake word detector.
        
        Args:
            wake_word: Wake word to detect (default: "zen")
            sensitivity: Detection sensitivity 0.0-1.0
            callback: Function to call when wake word detected
        """
        self.wake_word = wake_word.lower()
        self.sensitivity = sensitivity
        self.callback = callback
        self.running = False
        self.thread = None
        self.use_porcupine = False
        self.porcupine = None
        
        # Try to initialize Porcupine for accurate wake word detection
        try:
            import pvporcupine
            self.use_porcupine = True
            logger.info("Porcupine library available - using advanced wake word detection")
        except ImportError:
            logger.warning("Porcupine not available - using fallback speech recognition")
            logger.info("For better wake word detection, install: pip install pvporcupine")
    
    def _init_porcupine(self):
        """Initialize Porcupine wake word engine."""
        try:
            import pvporcupine
            
            # Initialize with built-in wake word
            # Porcupine has built-in keywords like "porcupine", "picovoice", etc.
            # For custom wake words, you need an access key from Picovoice Console
            self.porcupine = pvporcupine.create(
                keywords=["porcupine"],  # Using built-in keyword as fallback
                sensitivities=[self.sensitivity]
            )
            logger.info("Porcupine initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            self.use_porcupine = False
            return False
    
    def _detect_with_porcupine(self):
        """Detect wake word using Porcupine library."""
        try:
            import pvporcupine
            import pyaudio
            import struct
            
            if not self._init_porcupine():
                return
            
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            logger.info(f"Listening for wake word (Porcupine mode)...")
            
            while self.running:
                try:
                    pcm = audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    
                    keyword_index = self.porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        logger.info("Wake word detected!")
                        if self.callback:
                            self.callback()
                
                except Exception as e:
                    logger.error(f"Error in Porcupine detection: {e}")
                    time.sleep(0.1)
            
            # Cleanup
            audio_stream.close()
            pa.terminate()
            if self.porcupine:
                self.porcupine.delete()
                
        except Exception as e:
            logger.error(f"Porcupine detection failed: {e}")
            logger.info("Falling back to speech recognition mode")
            self.use_porcupine = False
            self._detect_with_speech_recognition()
    
    def _detect_with_speech_recognition(self):
        """Fallback: Detect wake word using speech recognition."""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                logger.info("Calibrating for wake word detection...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.info(f"Listening for wake word: '{self.wake_word}' (Speech recognition mode)...")
            logger.info("Say 'Hey Zen' or just 'Zen' to activate")
            
            while self.running:
                try:
                    with microphone as source:
                        # Short listening timeout for wake word
                        audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    
                    try:
                        text = recognizer.recognize_google(audio).lower()
                        logger.debug(f"Heard: {text}")
                        
                        # Check if wake word is in the text
                        if self.wake_word in text or f"hey {self.wake_word}" in text:
                            logger.info(f"Wake word detected: {text}")
                            if self.callback:
                                self.callback()
                    
                    except sr.UnknownValueError:
                        # Couldn't understand - continue listening
                        continue
                    except sr.RequestError as e:
                        logger.error(f"Speech recognition error: {e}")
                        time.sleep(1)
                
                except sr.WaitTimeoutError:
                    # No speech detected - continue listening
                    continue
                except Exception as e:
                    logger.error(f"Error in wake word detection: {e}")
                    time.sleep(1)
        
        except Exception as e:
            logger.error(f"Failed to initialize wake word detection: {e}")
            self.running = False
    
    def start(self):
        """Start wake word detection in background thread."""
        if self.running:
            logger.warning("Wake word detection already running")
            return
        
        self.running = True
        
        # Choose detection method
        if self.use_porcupine:
            target = self._detect_with_porcupine
        else:
            target = self._detect_with_speech_recognition
        
        self.thread = threading.Thread(target=target, daemon=True)
        self.thread.start()
        logger.info("Wake word detection started")
    
    def stop(self):
        """Stop wake word detection."""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Wake word detection stopped")
    
    def is_running(self):
        """Check if wake word detection is running."""
        return self.running


# Standalone test
if __name__ == "__main__":
    print("=== Zen Wake Word Detection Test ===\n")
    
    def on_wake_word():
        print("\n🎤 WAKE WORD DETECTED! Zen is now listening...\n")
    
    detector = WakeWordDetector(wake_word="zen", callback=on_wake_word)
    
    print("Starting wake word detection...")
    print("Say 'Hey Zen' or 'Zen' to test activation")
    print("Press Ctrl+C to stop\n")
    
    try:
        detector.start()
        
        # Keep running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nStopping wake word detection...")
        detector.stop()
        print("✓ Test complete!")
