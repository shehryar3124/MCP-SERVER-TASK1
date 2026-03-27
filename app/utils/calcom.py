import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# 🔥 Get project root path
env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# 🔥 Load .env from root
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv("CALCOM_BASE_URL")
API_KEY = os.getenv("CALCOM_API_KEY")

print("BASE_URL:", BASE_URL)
print("API_KEY:", API_KEY)

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get(path: str):
    response = requests.get(f"{BASE_URL}{path}", headers=headers)
    response.raise_for_status()
    return response.json()

def post(path: str, data: dict):
    response = requests.post(f"{BASE_URL}{path}", json=data, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)  # 🔥 IMPORTANT

    response.raise_for_status()
    return response.json()