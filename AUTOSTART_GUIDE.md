# Auto-Start Setup Guide for Windows

This guide explains how to configure Zen Voice Assistant to automatically start when Windows boots.

## Quick Setup

### Step 1: Install Zen Assistant
Make sure Zen is properly installed with all dependencies:
```bash
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run Auto-Start Setup
Open PowerShell (no admin required) and run:
```powershell
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
powershell -ExecutionPolicy Bypass -File setup_autostart.ps1
```

This will create a Windows Task Scheduler task that automatically runs Zen when you log in.

### Step 3: Configure Behavior (Optional)
Edit your `.env` file to customize startup behavior:
```env
# Auto-start configuration
AUTO_START_ENABLED=true
ANNOUNCE_TASKS_ON_STARTUP=true
START_MINIMIZED=false

# Wake word configuration (for voice activation)
WAKE_WORD_ENABLED=true
WAKE_WORD=zen
```

## What Happens on Startup?

When you log in to Windows:
1. Zen Assistant starts automatically (10 second delay)
2. Greets you with a welcome message
3. Announces your daily tasks (if `ANNOUNCE_TASKS_ON_STARTUP=true`)
4. Starts listening for wake words ("zen" or "activate")

## Managing Tasks

### Voice Commands
- **"What are my tasks for today?"** - Get a summary of today's tasks
- **"Add a task [description]"** - Add a new task
- **"Show all tasks"** - List all pending tasks

### Command Line
You can also manage tasks directly:
```bash
python -c "from daily_tasks import DailyTaskManager; tm = DailyTaskManager(); tm.add_task('Task name', 'Description', '2026-02-01', 'high')"
```

## Wake Word Usage

Say any of these to activate Zen:
- "Zen"
- "Hey Zen"
- "Activate"
- "Hey Activate"

## Disabling Auto-Start

To remove auto-start:
```powershell
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
powershell -ExecutionPolicy Bypass -File setup_autostart.ps1 -Uninstall
```

Or manually delete the task from Task Scheduler:
1. Open Task Scheduler (Win+R, type `taskschd.msc`)
2. Find "ZenVoiceAssistant" in the list
3. Right-click and delete

## Troubleshooting

### Zen doesn't start on login
1. Check Task Scheduler: Win+R → `taskschd.msc`
2. Find "ZenVoiceAssistant" task
3. Right-click → Run to test manually
4. Check task history for errors

### Virtual environment not found
Make sure you have created the virtual environment:
```bash
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Microphone doesn't work
- Check Windows microphone permissions
- Ensure microphone is set as default device
- Test with Windows Voice Recorder

### Tasks not announced
Check your `.env` file:
```env
ANNOUNCE_TASKS_ON_STARTUP=true
```

## Advanced Configuration

### Change Startup Delay
Edit `setup_autostart.ps1` and modify this line:
```powershell
$trigger.Delay = "PT10S"  # 10 seconds (PT15S for 15 seconds, etc.)
```

### Run as Administrator
For elevated privileges, modify the PowerShell script:
```powershell
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
```

## Manual Startup (Alternative)

If you prefer not to use Task Scheduler, you can manually start Zen:

**Windows:**
Double-click `start_zen.bat`

**Command Line:**
```bash
cd "c:\Users\ASUS\Desktop\New folder\Business\AI assistant"
venv\Scripts\activate
python main.py
```

## Configuration Reference

### .env Settings
```env
# Daily Tasks
DAILY_TASK_FILE=tasks_data.json
ANNOUNCE_TASKS_ON_STARTUP=true
AUTO_START_ENABLED=true
START_MINIMIZED=false

# Wake Word
WAKE_WORD_ENABLED=true
WAKE_WORD=zen
WAKE_WORD_SENSITIVITY=0.5

# GUI
GUI_ENABLED=true
GUI_MODE=neural
GUI_THEME=cyber_blue
```

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review `TROUBLESHOOTING.md`
3. Test individual components:
   ```bash
   python listen.py    # Test microphone
   python speak.py     # Test TTS
   python wake_word.py # Test wake word detection
   python daily_tasks.py # Test task management
   ```
