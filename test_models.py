import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key}")

genai.configure(api_key=api_key)

models_to_try = [
    'gemini-pro',
    'models/gemini-pro', 
    'gemini-1.5-pro',
    'gemini-1.5-flash'
]

for model_name in models_to_try:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("What is 2+2?")
        print(f"✓ SUCCESS with {model_name}!")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        error_str = str(e)
        if len(error_str) > 150:
            error_str = error_str[:150] + "..."
        print(f"✗ Failed: {error_str}")
