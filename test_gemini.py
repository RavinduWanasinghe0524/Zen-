import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")

genai.configure(api_key=api_key)

# Try to use a model
print("\n\nTesting models...")

models_to_try = ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', 'models/gemini-pro']

for model_name in models_to_try:
    try:
        print(f"\nTrying {model_name}...")
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        response = chat.send_message("What is 2+2?")
        print(f"✓ SUCCESS with {model_name}!")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:100]}")

