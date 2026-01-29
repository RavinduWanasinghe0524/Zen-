"""
Zen Voice Assistant - Configuration Module
Centralized configuration management for the assistant.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for Zen voice assistant."""
    
    # AI Provider Settings
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # Options: "openai", "gemini", "ollama"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Voice Settings
    SPEECH_RATE = int(os.getenv("SPEECH_RATE", "150"))  # Words per minute
    SPEECH_VOLUME = float(os.getenv("SPEECH_VOLUME", "0.9"))  # 0.0 to 1.0
    
    # Recognition Settings
    LISTEN_TIMEOUT = int(os.getenv("LISTEN_TIMEOUT", "5"))  # Seconds
    PHRASE_TIME_LIMIT = int(os.getenv("PHRASE_TIME_LIMIT", "10"))  # Seconds
    
    # Wake Word Settings
    WAKE_WORD_ENABLED = os.getenv("WAKE_WORD_ENABLED", "false").lower() == "true"
    WAKE_WORD = os.getenv("WAKE_WORD", "zen")
    WAKE_WORD_SENSITIVITY = float(os.getenv("WAKE_WORD_SENSITIVITY", "0.5"))
    
    # GUI Settings
    GUI_ENABLED = os.getenv("GUI_ENABLED", "true").lower() == "true"
    GUI_POSITION = os.getenv("GUI_POSITION", "bottom-right")  # top-left, top-right, bottom-left, bottom-right
    GUI_OPACITY = float(os.getenv("GUI_OPACITY", "0.9"))
    GUI_ALWAYS_ON_TOP = os.getenv("GUI_ALWAYS_ON_TOP", "true").lower() == "true"
    
    # Performance Settings
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_SIZE = int(os.getenv("CACHE_SIZE", "50"))
    ASYNC_SPEECH = os.getenv("ASYNC_SPEECH", "true").lower() == "true"
    PARALLEL_PROCESSING = os.getenv("PARALLEL_PROCESSING", "true").lower() == "true"
    
    # System Prompt for AI
    SYSTEM_PROMPT = """You are Zen, a helpful and concise voice assistant.

Your personality:
- Friendly but professional
- Clear and concise in your responses (keep answers brief for voice interaction)
- Proactive in offering solutions
- Patient and understanding

Guidelines:
- Keep responses under 2-3 sentences when possible
- For complex topics, offer to elaborate if the user wants more details
- When asked to perform system tasks, acknowledge and confirm the action
- Be conversational and natural

Remember: You're speaking, not typing, so avoid overly long explanations."""
    
    # Conversation History
    MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", "10"))  # Number of messages to keep
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    LOG_ROTATION_SIZE_MB = int(os.getenv("LOG_ROTATION_SIZE_MB", "10"))
    LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "7"))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    @classmethod
    def get_api_key(cls):
        """Get the appropriate API key based on the selected provider."""
        if cls.AI_PROVIDER == "openai":
            return cls.OPENAI_API_KEY
        elif cls.AI_PROVIDER == "gemini":
            return cls.GEMINI_API_KEY
        return None
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if cls.AI_PROVIDER not in ["openai", "gemini", "ollama"]:
            errors.append(f"Invalid AI_PROVIDER: {cls.AI_PROVIDER}")
        
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when using OpenAI")
        
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when using Gemini")
        
        return errors


# Create a default .env file if it doesn't exist
def create_default_env():
    """Create a default .env file with template values."""
    env_path = Path(".env")
    if not env_path.exists():
        default_content = """# Zen Voice Assistant Configuration

# AI Provider: "openai", "gemini", or "ollama"
AI_PROVIDER=gemini

# API Keys (get from https://aistudio.google.com/app/apikey for Gemini)
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# Ollama Settings (if using local model)
OLLAMA_MODEL=llama2

# Voice Settings
SPEECH_RATE=150
SPEECH_VOLUME=0.9

# Recognition Settings
LISTEN_TIMEOUT=5
PHRASE_TIME_LIMIT=10

# Wake Word Settings
WAKE_WORD_ENABLED=false
WAKE_WORD=zen

# Conversation History
MAX_HISTORY_LENGTH=10

# Logging
LOG_LEVEL=INFO
"""
        env_path.write_text(default_content)
        print(f"Created default .env file at {env_path.absolute()}")
        print("Please edit it with your API keys before running Zen.")


if __name__ == "__main__":
    create_default_env()
    
    print("=== Zen Configuration ===")
    print(f"AI Provider: {Config.AI_PROVIDER}")
    print(f"Speech Rate: {Config.SPEECH_RATE} WPM")
    print(f"Wake Word Enabled: {Config.WAKE_WORD_ENABLED}")
    
    errors = Config.validate_config()
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✓ Configuration is valid!")
