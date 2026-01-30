from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

client = genai.Client(api_key=api_key)

# Test simple generation without chat
try:
    print("\nTrying simple generation...")
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='What is 2+2? Answer briefly.'
    )
    print(f"✓ SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"\nFull error: {str(e)}")
