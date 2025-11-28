"""
Simple monitoring script to check endpoint health and view logs
Run this during the quiz to monitor your application
"""
import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ENDPOINT = os.getenv('ENDPOINT', 'http://localhost:8000')
CHECK_INTERVAL = 10  # seconds

def check_health():
    """Check if the endpoint is healthy"""
    try:
        response = requests.get(f"{ENDPOINT.replace('/quiz', '')}/health", timeout=5)
        if response.status_code == 200:
            return "✅ HEALTHY"
        else:
            return f"⚠️  Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"❌ ERROR: {str(e)}"

def main():
    print("=" * 60)
    print("LLM Quiz Endpoint Monitor")
    print("=" * 60)
    print(f"Monitoring: {ENDPOINT}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = check_health()
            print(f"[{timestamp}] {status}")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

if __name__ == "__main__":
    main()
