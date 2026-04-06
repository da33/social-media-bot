"""取得可用於 Instagram 的 Long-Lived Token"""
import requests

APP_ID = "1218345513805288"
APP_SECRET = "d16bd106370c20cc3ddee423606fce52"
PAGE_TOKEN = "EAARZBU1qsymIBRNNUGOdL7F1kAwdlBKQVaNq903cBcMuCJQOyxTaKv8ZCRWUqQ7aGcZAUo2ItZC8ZCFSY3ueZCYbJDeKd7vlHOfDZAs1zXsSkQgHhoiiCGQNB9IKZAXHZCX3mdwGgoGa2ZAHt65WvNmWQP0YAvLX28Rf2rMXVIpFChYaQFnAwZCxx8yqbVzAmmiZB7mV"

print("交換 Page Token 為 Long-Lived Token...")

# 交換為 long-lived token
url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": APP_ID,
    "client_secret": APP_SECRET,
    "fb_exchange_token": PAGE_TOKEN
}

response = requests.get(url, params=params)
result = response.json()

print(f"交換結果: {result}")

if "access_token" in result:
    long_lived_token = result["access_token"]
    expires_in = result.get("expires_in", "unknown")
    print(f"\n✅ Long-Lived Token 取得成功！")
    print(f"Token: {long_lived_token}")
    print(f"有效期: {expires_in} 秒 ({int(expires_in)/86400} 天)")
    
    # 用 long-lived token 測試 Instagram API
    print("\n測試 Instagram API...")
    ig_url = f"https://graph.instagram.com/v18.0/17841401987677377"
    ig_params = {
        "fields": "id,username,account_type,media_count",
        "access_token": long_lived_token
    }
    ig_response = requests.get(ig_url, params=ig_params)
    ig_result = ig_response.json()
    print(f"Instagram 測試結果: {ig_result}")
