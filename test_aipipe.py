"""
Test AIpipe token
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

print("=" * 70)
print("TESTING AIPIPE TOKEN")
print("=" * 70)
print()

if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env")
    print("Add your AIpipe token to .env file")
    exit(1)

if not base_url:
    print("⚠️  WARNING: OPENAI_BASE_URL not set")
    print("Add: OPENAI_BASE_URL=https://api.aipipe.com/v1")
    exit(1)

print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
print(f"Base URL: {base_url}")
print()

print("Testing AIpipe API...")
print("-" * 70)

try:
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Test with a simple request
    response = client.chat.completions.create(
        model="gpt-4",  # AIpipe supports gpt-4
        messages=[{"role": "user", "content": "Say 'Hello from AIpipe!'"}],
        max_tokens=10
    )
    
    # Handle different response formats
    if isinstance(response, str):
        result = response
    else:
        result = response.choices[0].message.content
    
    print(f"✅ SUCCESS! AIpipe is working")
    print(f"Response: {result}")
    print()
    print("Your AIpipe token is valid and has credits!")
    print()
    print("Next steps:")
    print("1. Update Render environment variables:")
    print(f"   - OPENAI_API_KEY = {api_key[:20]}...")
    print(f"   - OPENAI_BASE_URL = {base_url}")
    print("2. Redeploy your service")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    if "401" in str(e) or "unauthorized" in str(e).lower():
        print("⚠️  Invalid AIpipe token!")
        print()
        print("Solutions:")
        print("1. Check your AIpipe token")
        print("2. Make sure you copied it correctly")
        print("3. Verify it's not expired")
    elif "404" in str(e):
        print("⚠️  Wrong base URL!")
        print()
        print("Make sure OPENAI_BASE_URL is set to:")
        print("https://api.aipipe.com/v1")
    else:
        print("Check the error message above")

print()
print("=" * 70)
