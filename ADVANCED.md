# Zen Voice Assistant - Advanced Configuration Guide

## 🎯 Overview

This guide covers advanced configuration options, performance tuning, and customization for the Zen voice assistant.

## 🔧 Configuration Options

### AI Provider Settings

#### Using Google Gemini (Recommended for beginners)
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
```
- **Pros**: Free tier available, very capable, easy setup
- **Cons**: Requires internet connection
- **Get API Key**: https://aistudio.google.com/app/apikey

#### Using OpenAI
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```
- **Pros**: Most powerful, great for complex tasks
- **Cons**: Paid service, can get expensive
- **Get API Key**: https://platform.openai.com/api-keys

#### Using Ollama (Local)
```env
AI_PROVIDER=ollama
OLLAMA_MODEL=llama2
```
- **Pros**: Free, privacy-friendly, works offline
- **Cons**: Requires installation, slower on older hardware
- **Setup**: Download from https://ollama.ai/

### Wake Word Detection

Enable passive listening mode where Zen only activates when you say the wake word:

```env
WAKE_WORD_ENABLED=true
WAKE_WORD=zen
WAKE_WORD_SENSITIVITY=0.5
```

**Parameters:**
- `WAKE_WORD_ENABLED`: Enable/disable wake word mode
- `WAKE_WORD`: The word to listen for (lowercase)
- `WAKE_WORD_SENSITIVITY`: 0.0 (less sensitive) to 1.0 (more sensitive)

**Tips:**
- Lower sensitivity = fewer false activations but might miss the word
- Higher sensitivity = better detection but more false positives
- Start with 0.5 and adjust based on your environment

### GUI Overlay Settings

Visual feedback overlay showing Zen's current state:

```env
GUI_ENABLED=true
GUI_POSITION=bottom-right
GUI_OPACITY=0.9
GUI_ALWAYS_ON_TOP=true
```

**GUI_POSITION options:**
- `top-left`, `top-right`, `bottom-left`, `bottom-right`

**Visual States:**
- 🟢 **Green pulse** - Idle, ready for commands
- 🔴 **Red waveform** - Listening to you
- 🟡 **Yellow spinner** - Processing your request
- 🔵 **Blue rings** - Speaking response
- ⚫ **Gray pulse** - Waiting for wake word

**Customization:**
- Drag the GUI window to reposition
- Click the × to close
- Adjust opacity (0.0 = invisible, 1.0 = solid)

### Performance Tuning

Optimize Zen's speed and resource usage:

```env
CACHE_ENABLED=true
CACHE_SIZE=50
ASYNC_SPEECH=true
PARALLEL_PROCESSING=true
```

**CACHE_ENABLED**: Caches AI responses for faster replies to repeat questions
**CACHE_SIZE**: Number of responses to cache (higher = more memory)
**ASYNC_SPEECH**: Non-blocking speech (Zen can listen while speaking)
**PARALLEL_PROCESSING**: Process multiple tasks simultaneously

**Performance Tips:**
- Disable caching if privacy is a concern
- Increase cache size if you ask similar questions often
- Async speech makes interactions feel more natural
- Parallel processing improves responsiveness significantly

### Voice Settings

Customize Zen's voice output:

```env
SPEECH_RATE=150
SPEECH_VOLUME=0.9
```

**SPEECH_RATE**: Words per minute
- Slow: 100-130
- Normal: 140-160
- Fast: 170-200

**SPEECH_VOLUME**: 0.0 (silent) to 1.0 (max volume)

### Recognition Settings

Control how Zen listens:

```env
LISTEN_TIMEOUT=5
PHRASE_TIME_LIMIT=10
```

**LISTEN_TIMEOUT**: Seconds to wait before giving up (no speech detected)
**PHRASE_TIME_LIMIT**: Maximum length of a single phrase in seconds

**Adjustments:**
- Increase timeout if you need more time to start speaking
- Increase phrase limit for longer questions/commands

### Logging Configuration

Control logging behavior:

```env
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_ROTATION_SIZE_MB=10
LOG_RETENTION_DAYS=7
DEBUG_MODE=false
```

**LOG_LEVEL options:**
- `DEBUG` - Everything (very verbose)
- `INFO` - Normal operation info
- `WARNING` - Only warnings and errors
- `ERROR` - Only errors

**Log Files:**
- Location: `logs/` directory
- Main log: `zen_YYYYMMDD.log`
- Error log: `zen_errors_YYYYMMDD.log`
- Auto-rotates when reaching size limit
- Auto-deletes logs older than retention period

**Debug Mode:**
- Enable for troubleshooting
- Provides detailed execution traces
- Increases log file size significantly

## 🎨 Customizing Zen's Personality

Edit the system prompt in `config.py`:

```python
SYSTEM_PROMPT = """You are Zen, a helpful voice assistant.

Your personality:
- Professional but friendly
- Concise but thorough
- Patient and understanding
- Proactive in offering help

Guidelines:
- Keep voice responses under 2-3 sentences
- Offer to elaborate if needed
- Acknowledge commands before executing
- Be conversational and natural
"""
```

## 🚀 Performance Optimization

### For Faster Response Times

1. **Use Gemini or local Ollama** (faster than OpenAI)
2. **Enable caching** for common queries
3. **Enable parallel processing**
4. **Reduce conversation history** (MAX_HISTORY_LENGTH=5)
5. **Use a faster AI model** (if using Ollama, try smaller models)

### For Lower Resource Usage

1. **Disable GUI** if not needed
2. **Disable wake word** for lower CPU usage
3. **Reduce cache size** (CACHE_SIZE=20)
4. **Disable file logging** (LOG_TO_FILE=false)
5. **Lower speech rate** slightly (SPEECH_RATE=120)

### For Better Accuracy

1. **Higher wake word sensitivity** (0.7-0.8)
2. **Longer phrase time limit** (15-20 seconds)
3. **Better microphone** and quieter environment
4. **More detailed system prompt** with examples

## 🛠️ Extending Zen

### Adding Custom Tools

Edit `tools.py` to add new OS automation functions:

```python
@staticmethod
def your_custom_function(param):
    """
    Your custom functionality.
    
    Args:
        param: Description
        
    Returns:
        Status message
    """
    try:
        # Your code here
        return "Success message"
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Error message"
```

Then add keyword detection in `main.py`:

```python
if "your trigger phrase" in text_lower:
    result = self.tools.your_custom_function(arg)
    self.speaker.speak(result)
    return True
```

### Creating Custom Wake Words

For custom wake words with Porcupine:

1. Visit https://console.picovoice.ai/
2. Create a free account
3. Train a custom wake word
4. Download the model file
5. Update `wake_word.py` to use your custom model

## 📊 Monitoring & Debugging

### Checking Logs

View recent logs:
```bash
cat logs/zen_*.log | tail -100
```

View only errors:
```bash
cat logs/zen_errors_*.log
```

### Testing Individual Components

```bash
# Test speech recognition
python listen.py

# Test text-to-speech  
python speak.py

# Test AI brain
python brain.py

# Test wake word detection
python wake_word.py

# Test GUI overlay
python gui.py

# Test OS tools
python tools.py
```

### Common Issues

**High CPU usage:**
- Disable wake word detection
- Reduce GUI opacity/disable GUI
- Use a lighter AI model

**Slow responses:**
- Enable caching
- Enable parallel processing
- Switch to a faster AI provider

**Microphone not working:**
- Check Windows privacy settings
- Ensure microphone is default input
- Install latest PyAudio version

**Wake word false positives:**
- Reduce sensitivity (0.3-0.4)
- Choose a more unique wake word
- Improve microphone quality

## 🔐 Privacy & Security

### Data Handling

- **Conversation history**: Stored in memory only, cleared on exit
- **Logs**: Stored locally, auto-deleted after retention period
- **API calls**: Sent to chosen AI provider
- **Wake word**: Processed locally (Porcupine) or via Google (fallback)

### Privacy Best Practices

1. **Use local Ollama** for offline operation
2. **Disable logging** or use short retention periods
3. **Disable caching** for sensitive conversations
4. **Review `.env` file** - never commit to version control
5. **Clear logs manually**: Delete `logs/` directory

## 📝 Troubleshooting

### Issue: "API key not found"
**Solution**: Edit `.env` file and add your API key

### Issue: "Microphone not detected"
**Solution**: 
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue: "Wake word not activating"
**Solution**: 
- Increase sensitivity
- Speak clearly and at normal volume
- Ensure microphone is working

### Issue: GUI not showing
**Solution**:
- Check if tkinter is installed (comes with Python)
- Set `GUI_ENABLED=false` if not needed

### Issue: Slow performance
**Solution**:
- Enable performance optimizations in `.env`
- Use local Ollama instead of API
- Close other resource-intensive apps

---

## 💡 Tips & Tricks

1. **Chain commands**: "Open Chrome and search for weather"
2. **Be specific**: "Set volume to 50" instead of "lower volume"
3. **Use shortcuts**: "Time" instead of "What is the current time"
4. **Repeat activation**: If wake word fails, try speaking louder
5. **Background noise**: Works best in quiet environments

For support, check the main README.md or create an issue on GitHub.
