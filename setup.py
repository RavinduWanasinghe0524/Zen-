"""
Quick Setup Guide for Zen Voice Assistant
Run this script to get your API key and configure Zen quickly.
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          ZEN VOICE ASSISTANT - QUICK SETUP                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Welcome! Let's get Zen up and running in just a few steps.

STEP 1: Get a Free Gemini API Key
──────────────────────────────────────────────────────────────
1. Open your browser and visit:
   https://aistudio.google.com/app/apikey

2. Sign in with your Google account (it's free!)

3. Click "Create API Key" 

4. Copy the API key that appears

STEP 2: Configure Zen
──────────────────────────────────────────────────────────────
""")

# Get API key from user
api_key = input("Paste your Gemini API key here: ").strip()

if api_key and api_key != "your-gemini-api-key-here":
    # Update .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace the placeholder with actual API key
        content = content.replace('GEMINI_API_KEY=your-gemini-api-key-here', 
                                 f'GEMINI_API_KEY={api_key}')
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("""
✅ Configuration Complete!

Your Zen assistant is ready to use!

STEP 3: Run Zen
──────────────────────────────────────────────────────────────
To start Zen, run:

    python main.py

Then just speak into your microphone!

Try saying:
  - "Hello Zen"
  - "What time is it?"
  - "Open Notepad"
  - "Tell me a joke"

Enjoy your voice assistant! 🎙️
""")
    except Exception as e:
        print(f"\n⚠️ Error updating .env file: {e}")
        print("\nPlease manually edit the .env file and replace:")
        print(f"  GEMINI_API_KEY=your-gemini-api-key-here")
        print(f"with:")
        print(f"  GEMINI_API_KEY={api_key}")
else:
    print("""
⚠️ No API key provided.

Please run this script again or manually edit the .env file
and replace 'your-gemini-api-key-here' with your actual API key.

To get an API key, visit: https://aistudio.google.com/app/apikey
""")
