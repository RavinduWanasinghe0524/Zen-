# Zen AI Assistant - Quick Reference Card

## System Status: ✓ OPERATIONAL

**Last Verified:** February 13, 2026  
**Test Results:** 32/32 Passed  
**Python Version:** 3.11.9  
**AI Provider:** Gemini

---

## Quick Start

```bash
# Start the assistant
python main.py

# Or use batch file
start_zen.bat
```

---

## Voice Commands

### System Control
- "What time is it?"
- "Open Chrome / Notepad / Calculator"
- "What's my CPU usage?"
- "Set volume to 50"
- "Shutdown computer" (requires confirmation)

### AI Conversations
- "Tell me a joke"
- "What's the weather like?"
- "Explain [topic]"
- "Search for [query]"

### Memory & Tasks
- "Remember that I like coffee"
- "What do you remember about coffee?"
- "What are my tasks for today?"
- "Add a task: meeting at 3pm"

### Exit
- "Exit" / "Goodbye" / "Quit"

---

## GUI Controls

- **▼** - Minimize window
- **◐** - Change theme (cycles through 4 themes)
- **✕** - Close GUI
- **Drag** - Click and drag anywhere to move

---

## Themes Available

1. **Cyber Blue** (default) - Electric blue holographic
2. **Neural Purple** - Purple/pink gradient
3. **Quantum Orange** - Orange/gold energy
4. **Dark Matter** - Monochrome white/cyan

---

## Configuration (.env)

```env
# AI Provider
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here

# GUI Settings
GUI_ENABLED=true
GUI_MODE=neural
GUI_THEME=cyber_blue

# Voice Settings
SPEECH_RATE=180
SPEECH_VOLUME=0.9

# Optional Features
WAKE_WORD_ENABLED=false
ENABLE_VISION=false
NEURAL_VOICE_ENABLED=false
```

---

## Troubleshooting

### Quick Fixes
1. **No response?** - Check microphone permissions
2. **API errors?** - Verify `.env` has correct API key
3. **GUI not showing?** - Set `GUI_ENABLED=true` in `.env`
4. **Slow response?** - Increase `PHRASE_TIME_LIMIT` in `.env`

### Run System Test
```bash
python test_system.py
```

### Check Logs
```bash
# View latest log file
Get-ChildItem logs | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

---

## Advanced Features (Optional)

### Enable Wake Word
```env
WAKE_WORD_ENABLED=true
WAKE_WORD=zen
```
Then say "Zen" or "Activate" to wake the assistant!

### Enable AI Vision
```env
ENABLE_VISION=true
VISION_PROVIDER=gemini
```
Then ask: "What's on my screen?"

### Enable Neural Voice
```env
NEURAL_VOICE_ENABLED=true
NEURAL_VOICE_PROVIDER=openai
```
Requires OpenAI API key for premium voice quality.

---

## File Locations

- **Config:** `.env`
- **Tasks:** `tasks_data.json`
- **Logs:** `logs/` directory
- **Main:** `main.py`

---

## Support

- **Full Docs:** [README.md](file:///c:/Users/ASUS/Desktop/New%20folder/Business/AI%20assistant/README.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](file:///c:/Users/ASUS/Desktop/New%20folder/Business/AI%20assistant/TROUBLESHOOTING.md)
- **Advanced:** [ADVANCED.md](file:///c:/Users/ASUS/Desktop/New%20folder/Business/AI%20assistant/ADVANCED.md)
- **Auto-start:** [AUTOSTART_GUIDE.md](file:///c:/Users/ASUS/Desktop/New%20folder/Business/AI%20assistant/AUTOSTART_GUIDE.md)

---

**Ready to go! Just run:** `python main.py`
