"""取得 Long-Lived Instagram Token"""
import requests

APP_ID = "1218345513805288"
APP_SECRET = "d16bd106370c20cc3ddee423606fce52"
SHORT_LIVED_TOKEN = "EAARZBU1qsymIBRKWUnKqZBjtI4LiZC6lirg1ZBVUYG7RGFX68GEwwBzYS1g33T3IABKKEYUZC71ZAR3lAe9Qfk21o1wygzSZCgOZBDvLPMmdxiommPS2Du6kgjA6i6glvEmKMSvwDsG8XUDUuXVqmIpFO0uC3khMtIjB21C57dy2MasYWrSXHbqra8g9EgZDZD"

print("交換 Token...")

# 先取得 Long-Lived Token
url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": APP_ID,
    "client_secret": APP_SECRET,
    "fb_exchange_token": SHORT_LIVED_TOKEN
}

response = requests.get(url, params=params)
result = response.json()

print(f"結果: {result}")

if "access_token" in result:
    long_lived_token = result["access_token"]
    expires_in = result.get("expires_in", "unknown")
    print(f"\n✅ Long-Lived Token 取得成功！")
    print(f"Token: {long_lived_token}")
    print(f"有效期: {expires_in} 秒 ({int(expires_in)/86400} 天)")
    
    # 測試 token
    print("\n測試 Token...")
    test_url = f"https://graph.instagram.com/v18.0/me"
    test_params = {
        "fields": "id,username,account_type",
        "access_token": long_lived_token
    }
    test_response = requests.get(test_url, params=test_params)
    test_result = test_response.json()
    print(f"測試結果: {test_result}")
