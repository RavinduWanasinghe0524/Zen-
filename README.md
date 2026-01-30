# 🎙️ Zen Voice Assistant

A powerful, modular desktop voice assistant for Windows that combines speech recognition, AI intelligence, and OS automation capabilities. Inspired by JARVIS from Marvel.

## ✨ Features

- **🎤 Voice Input**: Natural speech recognition using your microphone
- **🔊 Voice Output**: Clear text-to-speech responses
- **🧠 AI Intelligence**: Powered by OpenAI, Google Gemini, or local Ollama models
- **🛠️ OS Automation**: Open applications, search the web, get system info, and more
- **💬 Contextual Conversations**: Maintains conversation history for natural interactions
- **⚙️ Configurable**: Easy configuration via environment variables
- **🚀 Auto-Start**: Automatically starts on Windows boot
- **📋 Daily Tasks**: Manage and get voice announcements of your daily tasks
- **🎙️ Wake Words**: Say "Zen" or "Activate" to wake the assistant


## 🏗️ Architecture

The project follows a modular structure:

```
zen/
├── main.py           # Main orchestration and conversation loop
├── listen.py         # Speech-to-Text (microphone input)
├── speak.py          # Text-to-Speech (audio output)
├── brain.py          # AI integration and conversation management
├── tools.py          # OS automation functions
├── config.py         # Configuration management
├── requirements.txt  # Python dependencies
└── .env             # Environment variables (create this)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows 10/11
- Working microphone
- Internet connection (for cloud AI providers)

### Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyAudio** (if pip fails, download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)):
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

5. **Create configuration file**:
   ```bash
   python config.py
   ```

6. **Edit `.env` file** with your settings:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your-api-key-here
   ```

### Getting an API Key

#### Google Gemini (Recommended - Free Tier)
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

#### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create a new API key
4. Copy the key to your `.env` file

#### Ollama (Local - No API Key Needed)
1. Download and install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama2`
3. Set `AI_PROVIDER=ollama` in `.env`

## 🎮 Usage

### Running Zen

```bash
python main.py
```

## 🎯 New Features

### 🚀 Auto-Start on Windows Boot

See [AUTOSTART_GUIDE.md](AUTOSTART_GUIDE.md) for complete instructions.

**Quick Setup:**
```powershell
powershell -ExecutionPolicy Bypass -File setup_autostart.ps1
```

This configures Windows Task Scheduler to start Zen automatically when you log in.

### 📋 Daily Task Management

Manage your daily tasks with voice commands:

**Add a task:**
```
"Add a task meeting at 3pm"
```

**Check your tasks:**
```
"What are my tasks for today?"
```

**Via Python (advanced):**
```python
from daily_tasks import DailyTaskManager
tm = DailyTaskManager()
tm.add_task("Task name", "Description", "2026-02-01", "high")
```

### 🎙️ Wake Word Activation

Enable wake word mode in `.env`:
```env
WAKE_WORD_ENABLED=true
```

Then say "Zen", "Activate", or "Hey Zen" to activate the assistant!

## 🎮 Usage


**Daily Tasks:**
- "What are my tasks for today?"
- "Add a task [description]"
- "Show all tasks"

**System Commands:**
- "Open Notepad"
- "Open Calculator"
- "Open Chrome"
- "What time is it?"
- "What's the system status?"
- "Search for Python tutorials"

**AI Conversations:**
- "Tell me a joke"
- "What's the capital of France?"
- "Explain quantum computing"
- "Write a poem about nature"

**Exit:**
- "Exit"
- "Goodbye"
- "Quit"

**Wake Words (when wake word mode enabled):**
- "Zen"
- "Hey Zen"
- "Activate"
- "Hey Activate"


### Testing Individual Components

Test speech recognition:
```bash
python listen.py
```

Test text-to-speech:
```bash
python speak.py
```

Test AI brain:
```bash
python brain.py
```

Test system tools:
```bash
python tools.py
```

## ⚙️ Configuration

Edit `.env` file to customize settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider: openai, gemini, or ollama | gemini |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `SPEECH_RATE` | Speech speed (words per minute) | 150 |
| `SPEECH_VOLUME` | Volume level (0.0 to 1.0) | 0.9 |
| `LISTEN_TIMEOUT` | Seconds to wait for speech | 5 |
| `MAX_HISTORY_LENGTH` | Conversation memory length | 10 |

## 🛠️ Available Tools

### OS Automation

- `open_application(app_name)` - Launch Windows applications
- `get_current_time()` - Get current date and time
- `search_web(query)` - Search on Google
- `get_system_info()` - CPU, memory, and system stats
- `set_volume(level)` - Adjust system volume (0-100)
- `shutdown_system()` - Shutdown computer (with 30s warning)
- `restart_system()` - Restart computer (with 30s warning)

## 🔧 Troubleshooting

### Microphone not working
- Check microphone permissions in Windows Settings
- Ensure microphone is set as default input device
- Test microphone with Windows Voice Recorder

### PyAudio installation failed
- Download the appropriate wheel file from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Install with: `pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl` (adjust for your Python version)

### API errors
- Verify your API key is correct in `.env`
- Check your internet connection
- Ensure you have API credits/quota remaining

### Speech recognition errors
- Speak clearly and at normal pace
- Reduce background noise
- Adjust `LISTEN_TIMEOUT` in `.env`

## 🚧 Future Enhancements

- [x] Wake word detection ("Hey Zen", "Activate") ✅
- [x] GUI with visual feedback ✅
- [x] Daily task management ✅
- [x] Auto-start on Windows boot ✅
- [ ] More OS automation tools
- [ ] Plugin system for custom tools
- [ ] Multi-language support
- [ ] Voice cloning for personalized responses
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] System tray integration


## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

Built with:
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- [OpenAI API](https://platform.openai.com/)
- [Google Gemini](https://ai.google.dev/)
- [Ollama](https://ollama.ai/)

---

**Made with ❤️ for voice assistant enthusiasts**
