from PySide6.QtCore import QThread, Signal
import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class WorkerListen(QThread):
    signal_text_recognized = Signal(str)
    signal_error = Signal(str)
    signal_listening_started = Signal()
    signal_listening_stopped = Signal()

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = True

        # Adjust for ambient noise once at startup
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def run(self):
        while self.running:
            try:
                self.signal_listening_started.emit()
                with self.microphone as source:
                    # Listen with timeout to allow checking self.running
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    except sr.WaitTimeoutError:
                        continue # Check running flag and loop again

                self.signal_listening_stopped.emit()
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        self.signal_text_recognized.emit(text)
                except sr.UnknownValueError:
                    pass # Ignored
                except sr.RequestError as e:
                    self.signal_error.emit(f"API Error: {e}")

            except Exception as e:
                self.signal_error.emit(str(e))

    def stop(self):
        self.running = False
        self.wait()
