# Zen Voice Assistant - Troubleshooting Guide

## 🎙️ Speech Recognition Not Accurate?

If Zen is not understanding you correctly or not doing what you tell it, try these solutions:

### Quick Fixes (Try These First)

#### 1. **Speak Clearly and Slowly**
- Speak at normal volume, not too loud or quiet
- Pronounce words clearly
- Pause briefly between words
- Don't rush your commands

#### 2. **Reduce Background Noise**
- Close windows and doors
- Turn off fans, AC, or music
- Move to a quieter room
- Use headphones with a built-in microphone

#### 3. **Check Your Microphone**
- Make sure it's not muted
- Position it 6-12 inches from your mouth
- Check Windows sound settings (Make sure it's the default device)
- Test it with Windows Voice Recorder first

#### 4. **Use Simple Commands First**
Start with these tested commands:
- "What time is it?" ← Very reliable
- "Open Notepad" ← Simple and clear
- "Hello" ← Basic test
- "Exit" ← To quit

Avoid complex sentences until accuracy improves.

---

## 🔧 Configuration Improvements

### Already Applied ✅
I've updated your `.env` file with better settings:
- Increased `LISTEN_TIMEOUT` to 8 seconds (more time to start speaking)
- Increased `PHRASE_TIME_LIMIT` to 15 seconds (for longer commands)

### Additional Adjustments You Can Make

Edit your `.env` file:

**For Better Accuracy (Slower but More Accurate):**
```env
LISTEN_TIMEOUT=10
PHRASE_TIME_LIMIT=20
```

**For Faster Response (Less Accurate):**
```env
LISTEN_TIMEOUT=3
PHRASE_TIME_LIMIT=8
```

After changing `.env`, restart Zen:
1. Press Ctrl+C to stop
2. Run `python main.py` again

---

## 🎯 Best Practices for Commands

### ✅ DO:
- "Open Notepad" ← Short and clear
- "What time is it?" ← Natural question
- "Search for cats" ← Simple search
- "Open Calculator" ← One app at a time

### ❌ DON'T:
- "Open Notepad and Calculator and Chrome" ← Too complex
- Speaking while Zen is speaking ← Wait for silence
- Mumbling or whispering ← Speak clearly
- Very long sentences ← Keep it under 10 words

---

## 🔍 Understanding What Zen Hears

Check the terminal output - you'll see lines like:
```
INFO - Recognized: [what Zen heard]
```

Compare this to what you actually said. Common issues:

**If Zen hears gibberish:**
- Microphone is too quiet → Increase mic volume in Windows
- Too much background noise → Move to quieter location

**If Zen hears partial commands:**
- You're speaking too fast → Slow down
- Microphone is too far → Move it closer

**If Zen says "Could not understand audio":**
- You're too quiet → Speak louder
- No speech detected → Check if mic is muted

---

## 💡 Pro Tips for Best Results

### 1. **Wait for "Listening..."**
Don't speak until you see this in the terminal or the GUI shows red.

### 2. **Pause After Speaking**
Give Zen 1-2 seconds to process after you finish talking.

### 3. **Repeat if Necessary**
If Zen doesn't understand, just say it again more clearly.

### 4. **Use Keyword Commands**
These work best because they don't need AI:
- "Open [app name]"
- "What time"
- "Search for [topic]"

### 5. **Microphone Quality Matters**
- Built-in laptop mics: OK
- USB microphone: Good
- Headset with mic: Best
- Bluetooth earbuds: Can be delayed

---

## 🛠️ Advanced Troubleshooting

### Test Your Microphone
```bash
python listen.py
```
This runs ONLY the speech recognition. Speak clearly and see what it recognizes.

### Check Windows Settings
1. Right-click speaker icon → Sounds
2. Recording tab
3. Select your microphone
4. Properties → Levels → Set to 80-90%
5. Advanced → Disable all enhancements

### Try Different Microphones
If available, test with:
- Headset microphone
- Phone earbuds
- External USB mic

### Enable Debug Mode
Edit `.env`:
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Then check `logs/zen_YYYYMMDD.log` for detailed info.

---

## 📊 Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| "Could not understand audio" | Speak louder, check mic |
| Hears wrong words | Speak slower, reduce noise |
| GUI not showing | Restart Zen |
| No response at all | Check internet (needs Gemini API) |
| Very slow | Check internet speed |
| Crashes often | Enable DEBUG_MODE, check logs |

---

## 🚀 Optimized Workflow

1. **Start Zen**: Run `python main.py`
2. **Wait**: Look for "Listening..." message
3. **Speak**: Say command clearly at normal pace
4. **Wait**: Let Zen process (watch GUI change colors)
5. **Listen**: Hear Zen's response
6. **Repeat**: Ready for next command

**Example Session:**
```
You: "What time is it?"
[Wait 2 seconds]
Zen: "It's 7:30 PM on Wednesday, January 29, 2026."
[Wait for "Listening..." again]
You: "Open Notepad"
[Wait 2 seconds]
Zen: "Opened Notepad successfully."
```

---

## 🎊 Still Having Issues?

### Try These Commands (Tested & Reliable):
1. "Time" ← Very short
2. "Hello" ← Even shorter
3. "What time is it" ← Full question
4. "Open Notepad" ← Action command

### Check Logs
```bash
cat logs/zen_*.log | tail -50
```

Look for error messages or recognition patterns.

### Restart Fresh
1. Stop Zen (Ctrl+C)
2. Close terminal
3. Reopen terminal
4. Run `python main.py`

---

**After trying these fixes, restart Zen and test with "What time is it?" - this should work reliably!**
