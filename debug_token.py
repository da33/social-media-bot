"""Debug Instagram Access Token"""
import requests

APP_ID = "1218345513805288"
APP_SECRET = "58f18c53de9594e3725a95caee3ea270"
TOKEN_TO_DEBUG = "IGAARUFCuQZAehBZAGFkcmxVbTlfVHdUY2VDb1hrXy1vMWpmMjRoU082TUtXSUFkZA0RiOThzUkE0b1lXRUt3TkF0dHFWQ2dpeXBjNWJjLVU3NW9ldHAwLVEyTFNSOVBENUJPcFhHWndnZAEdiUzI3YVBvbGlyYzNTVkNaX3BKOGJxcwZDZD"

print("Debug Instagram Access Token...")

url = "https://graph.facebook.com/v18.0/debug_token"
params = {
    "input_token": TOKEN_TO_DEBUG,
    "access_token": f"{APP_ID}|{APP_SECRET}"
}

response = requests.get(url, params=params)
result = response.json()

print(f"結果: {result}")

if "data" in result:
    data = result["data"]
    print(f"\n有效: {data.get('is_valid')}")
    print(f"Application ID: {data.get('app_id')}")
    print(f"創建時間: {data.get('issued_at')}")
    print(f"過期時間: {data.get('expires_at')}")
    print(f"Scopes: {data.get('scopes')}")
