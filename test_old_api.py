import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

# Test with old API
try:
    print("\nTesting with old google.generativeai package...")
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content("What is 2+2? Answer briefly.")
    print(f"✓ SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
