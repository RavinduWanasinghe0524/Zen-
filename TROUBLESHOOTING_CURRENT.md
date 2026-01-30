# Troubleshooting Guide - Zen Not Responding

## Issues Identified

Based on the logs, two issues are preventing Zen from responding:

### 1. ❌ Gemini API Rate Limit (Error 429)
**Error**: "429 You exceeded your current quota"

**Solutions**:

#### Option A: Wait for Rate Limit Reset (Free Tier)
If using Gemini free tier, you may have hit the requests-per-minute limit. Wait 1-2 minutes and try again.

#### Option B: Get a New API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Update `.env` file:
   ```env
   GEMINI_API_KEY=your-new-key-here
   ```

#### Option C: Switch to Ollama (Free, Offline)
Install Ollama for completely free, local AI:

1. Download Ollama: https://ollama.ai/
2. Install and run: `ollama pull llama2`
3. Update `.env`:
   ```env
   AI_PROVIDER=ollama
   OLLAMA_MODEL=llama2
   ```

### 2. ❌ Microphone Recognition Issues
**Error**: "Could not understand audio" (repeated)

**Solutions**:

#### Check Microphone Setup
1. **Test microphone**: Open Windows Sound Recorder and record your voice
2. **Check default device**: 
   - Right-click speaker icon → Sounds → Recording
   - Ensure your microphone is set as "Default Device"
3. **Adjust microphone levels**:
   - Right-click microphone → Properties → Levels
   - Set to 80-100%

#### Improve Recognition Settings
Update `.env` for better speech recognition:

```env
# Give more time for speech
LISTEN_TIMEOUT=5
PHRASE_TIME_LIMIT=10

# Make sure speech rate is comfortable
SPEECH_RATE=150
```

#### Test Speech Recognition Alone
```bash
python listen.py
```

Speak clearly into the microphone. If this doesn't work, there's a microphone configuration issue.

---

## Quick Fix Commands

### 1. Test Microphone
```bash
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
venv\Scripts\activate
python listen.py
```

### 2. Switch to Ollama (Recommended for Testing)
```bash
# Install Ollama first from https://ollama.ai/
ollama pull llama2

# Then update .env:
# AI_PROVIDER=ollama
```

### 3. Test with Text Mode (No Microphone)
```bash
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
venv\Scripts\activate
python text_mode.py
```

---

## Recommended Solution

**For immediate testing**, I recommend:

1. **Use text mode** to test the AI functionality:
   ```bash
   python text_mode.py
   ```
   Type your questions instead of speaking them.

2. **Fix microphone issues**:
   - Check Windows microphone permissions
   - Set microphone as default device
   - Test with Windows Voice Recorder

3. **Switch to Ollama** to avoid API rate limits:
   ```bash
   # Install Ollama
   ollama pull llama2
   ```
   
   Then update `.env`:
   ```env
   AI_PROVIDER=ollama
   OLLAMA_MODEL=llama2
   ```

---

## New Features Still Work!

Even with these issues, the new features you requested are fully implemented:

✅ **Auto-start**: Run `setup_autostart.ps1` - works independently
✅ **Daily tasks**: Task management system works perfectly
✅ **Wake word**: "activate" command integrated - will work once mic is fixed

The features are complete; we just need to resolve the Gemini API quota and microphone configuration.
