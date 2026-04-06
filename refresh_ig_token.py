"""刷新 Instagram Long-Lived Access Token"""
import requests

APP_ID = "1218345513805288"
APP_SECRET = "d16bd106370c20cc3d3de423606fce52"
CURRENT_TOKEN = "IGAARUFCuQZAehBZAGFkcmxVbTlfVHdUY2VDb1hrX1vMWpmMjRoU082TUtXSUFkZA0RiOThzUkE0b1lXRUt3TkF0dHFWQ2dpeXBjNWJjLVU3NW9ldHAwLVEyTFNSOVBENUJPcFhHWndnZAEdiUzI3YVBvbGlyYzNTVkNaX3BKOGJxcwZDZD"

print("刷新 Instagram Long-Lived Access Token...")

url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": APP_ID,
    "client_secret": APP_SECRET,
    "fb_exchange_token": CURRENT_TOKEN
}

response = requests.get(url, params=params)
result = response.json()

print(f"結果: {result}")

if "access_token" in result:
    new_token = result["access_token"]
    expires_in = result.get("expires_in", "unknown")
    print(f"\n✅ Token 刷新成功！")
    print(f"新 Token: {new_token}")
    print(f"有效期: {expires_in} 秒 ({int(expires_in)/86400} 天)")
