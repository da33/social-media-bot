"""Debug Instagram Access Token with new secret"""
import requests

APP_SECRET = "d16bd106370c20cc3d3de423606fce52"
TOKEN = "IGAARUFCuQZAehBZAGFkcmxVbTlfVHdUY2VDb1hrX1vMWpmMjRoU082TUtXSUFkZA0RiOThzUkE0b1lXRUt3TkF0dHFWQ2dpeXBjNWJjLVU3NW9ldHAwLVEyTFNSOVBENUJPcFhHWndnZAEdiUzI3YVBvbGlyYzNTVkNaX3BKOGJxcwZDZD"

print("Debug Token...")

# Try debug with the new secret
url = "https://graph.facebook.com/v18.0/debug_token"
params = {
    "input_token": TOKEN,
    "access_token": f"1218345513805288|{APP_SECRET}"
}

response = requests.get(url, params=params)
result = response.json()

print(f"結果: {result}")

if "data" in result:
    data = result["data"]
    print(f"\n有效: {data.get('is_valid')}")
    print(f"Error: {data.get('error')}")
