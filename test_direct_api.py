"""
Test Gemini API directly with REST call
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

# Direct REST API call
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

headers = {
    'Content-Type': 'application/json',
}

data = {
    "contents": [{
        "parts": [{
            "text": "Hello! What is 2+2? Answer very briefly."
        }]
    }]
}

print("\nTesting direct REST API call...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"✓ SUCCESS!")
        print(f"Response: {text}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")
