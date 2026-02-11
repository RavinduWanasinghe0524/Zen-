"""
List available Gemini models
"""
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

# List models endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("\nFetching available models...")
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        if 'models' in result:
            print("Available models:")
            for model in result['models']:
                name = model.get('name', 'Unknown')
                display_name = model.get('displayName', 'Unknown')
                methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    print(f"  ✓ {name} ({display_name})")
        else:
            print("No models found")
            print(json.dumps(result, indent=2))
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")
