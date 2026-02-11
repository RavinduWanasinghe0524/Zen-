"""
Zen Voice Assistant - Neural Voice Synthesis
Advanced text-to-speech with neural voices and emotion support.
"""

import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)


class NeuralVoice:
    """Neural text-to-speech engine with advanced features."""
    
    def __init__(self, provider="elevenlabs", voice="default", emotion="neutral"):
        """
        Initialize neural voice synthesizer.
        
        Args:
            provider: Voice provider (elevenlabs, azure, openai)
            voice: Voice ID or name
            emotion: Emotional tone (neutral, happy, sad, excited, calm)
        """
        self.provider = provider
        self.voice = voice
        self.emotion = emotion
        self.client = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the selected provider."""
        try:
            if self.provider == "elevenlabs":
                self._init_elevenlabs()
            elif self.provider == "azure":
                self._init_azure()
            elif self.provider == "openai":
                self._init_openai()
            else:
                logger.warning(f"Unknown provider: {self.provider}, falling back to pyttsx3")
                self._init_fallback()
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider}: {e}")
            logger.info("Falling back to standard TTS")
            self._init_fallback()
    
    def _init_elevenlabs(self):
        """Initialize ElevenLabs neural voice."""
        try:
            from elevenlabs import client, VoiceSettings
            
            api_key = Config.ELEVENLABS_API_KEY if hasattr(Config, 'ELEVENLABS_API_KEY') else None
            if not api_key:
                raise ValueError("ELEVENLABS_API_KEY not configured")
            
            self.client = client.ElevenLabs(api_key=api_key)
            self.voice_id = Config.ELEVENLABS_VOICE_ID if hasattr(Config, 'ELEVENLABS_VOICE_ID') else "21m00Tcm4TlvDq8ikWAM"
            logger.info("ElevenLabs neural voice initialized")
        except ImportError:
            raise ImportError("elevenlabs package not installed. Run: pip install elevenlabs")
    
    def _init_azure(self):
        """Initialize Azure Cognitive Services neural voice."""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_key = Config.AZURE_SPEECH_KEY if hasattr(Config, 'AZURE_SPEECH_KEY') else None
            speech_region = Config.AZURE_SPEECH_REGION if hasattr(Config, 'AZURE_SPEECH_REGION') else "eastus"
            
            if not speech_key:
                raise ValueError("AZURE_SPEECH_KEY not configured")
            
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Premium neural voice
            
            self.client = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            logger.info("Azure Neural TTS initialized")
        except ImportError:
            raise ImportError("azure-cognitiveservices-speech not installed. Run: pip install azure-cognitiveservices-speech")
    
    def _init_openai(self):
        """Initialize OpenAI TTS."""
        try:
            from openai import OpenAI
            
            api_key = Config.OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            
            self.client = OpenAI(api_key=api_key)
            self.model = "tts-1-hd"  # High-quality model
            self.voice_name = Config.OPENAI_VOICE if hasattr(Config, 'OPENAI_VOICE') else "nova"
            logger.info("OpenAI TTS initialized")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def _init_fallback(self):
        """Initialize fallback pyttsx3 engine."""
        import pyttsx3
        self.client = pyttsx3.init()
        self.provider = "pyttsx3"
        logger.info("Using fallback pyttsx3 TTS")
    
    def speak(self, text: str, save_to_file: Optional[str] = None):
        """
        Synthesize and speak text.
        
        Args:
            text: Text to speak
            save_to_file: Optional path to save audio file
        """
        try:
            if self.provider == "elevenlabs":
                self._speak_elevenlabs(text, save_to_file)
            elif self.provider == "azure":
                self._speak_azure(text, save_to_file)
            elif self.provider == "openai":
                self._speak_openai(text, save_to_file)
            else:
                self._speak_fallback(text)
        except Exception as e:
            logger.error(f"Neural voice error: {e}")
            # Fallback to basic TTS
            self._speak_fallback(text)
    
    def _speak_elevenlabs(self, text: str, save_path: Optional[str] = None):
        """Speak using ElevenLabs."""
        from elevenlabs import play, save
        
        audio = self.client.generate(
            text=text,
            voice=self.voice_id,
            model="eleven_turbo_v2"  # Fastest model
        )
        
        if save_path:
            save(audio, save_path)
        else:
            play(audio)
    
    def _speak_azure(self, text: str, save_path: Optional[str] = None):
        """Speak using Azure."""
        import azure.cognitiveservices.speech as speechsdk
        
        if save_path:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=save_path)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.client.speech_config,
                audio_config=audio_config
            )
        else:
            synthesizer = self.client
        
        # Add SSML for emotion control
        ssml = self._create_ssml(text)
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info("Azure TTS synthesis completed")
        else:
            logger.error(f"Azure TTS failed: {result.reason}")
    
    def _speak_openai(self, text: str, save_path: Optional[str] = None):
        """Speak using OpenAI TTS."""
        import tempfile
        import os
        from playsound import playsound
        
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice_name,
            input=text
        )
        
        if save_path:
            response.stream_to_file(save_path)
        else:
            # Play immediately
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_path = tmp_file.name
                response.stream_to_file(tmp_path)
            
            playsound(tmp_path)
            os.unlink(tmp_path)
    
    def _speak_fallback(self, text: str):
        """Speak using fallback engine."""
        self.client.say(text)
        self.client.runAndWait()
    
    def _create_ssml(self, text: str) -> str:
        """Create SSML with emotion markup for Azure."""
        emotion_styles = {
            "neutral": "default",
            "happy": "cheerful",
            "sad": "sad",
            "excited": "excited",
            "calm": "calm"
        }
        
        style = emotion_styles.get(self.emotion, "default")
        
        ssml = f"""
        <speak version='1.0' xml:lang='en-US'>
            <voice name='en-US-JennyNeural'>
                <mstts:express-as style='{style}'>
                    {text}
                </mstts:express-as>
            </voice>
        </speak>
        """
        return ssml
    
    def set_emotion(self, emotion: str):
        """Change the emotional tone."""
        self.emotion = emotion
        logger.info(f"Emotion set to: {emotion}")
    
    def set_voice(self, voice_id: str):
        """Change the voice."""
        self.voice = voice_id
        logger.info(f"Voice changed to: {voice_id}")


# Standalone test
if __name__ == "__main__":
    print("=== Zen Neural Voice Test ===\n")
    
    # Test with fallback (will work without API keys)
    print("Testing fallback TTS...")
    voice = NeuralVoice(provider="pyttsx3")
    voice.speak("Hello! This is the Zen neural voice system testing basic functionality.")
    
    print("\n✓ Neural voice test complete!")
    print("\nNote: For premium neural voices, configure:")
    print("  - ElevenLabs: Add ELEVENLABS_API_KEY to .env")
    print("  - Azure: Add AZURE_SPEECH_KEY and AZURE_SPEECH_REGION to .env")
    print("  - OpenAI: Uses existing OPENAI_API_KEY")
