"""直接測試 Token 並取得 Instagram 帳號"""
import requests

TOKEN = "EAARZBU1qsymIBRKWUnKqZBjtI4LiZC6lirg1ZBVUYG7RGFX68GEwwBzYS1g33T3IABKKEYUZC71ZAR3lAe9Qfk21o1wygzSZCgOZBDvLPMmdxiommPS2Du6kgjA6i6glvEmKMSvwDsG8XUDUuXVqmIpFO0uC3khMtIjB21C57dy2MasYWrSXHbqra8g9EgZDZD"

print("測試 Token...")

# 測試 Facebook API
fb_url = "https://graph.facebook.com/v18.0/me"
fb_params = {
    "access_token": TOKEN,
    "fields": "id,name,accounts"
}
fb_response = requests.get(fb_url, params=fb_params)
print(f"Facebook API 回應: {fb_response.json()}")

# 測試 Instagram API
print("\n測試 Instagram API...")
ig_url = "https://graph.instagram.com/v18.0/me"
ig_params = {
    "access_token": TOKEN,
    "fields": "id,username,account_type,media_count"
}
ig_response = requests.get(ig_url, params=ig_params)
print(f"Instagram API 回應: {ig_response.json()}")

# 嘗試取得關聯的 Instagram 帳號
print("\n取得關聯的 Instagram 帳號...")
accounts_url = "https://graph.facebook.com/v18.0/me/accounts"
accounts_params = {
    "access_token": TOKEN
}
accounts_response = requests.get(accounts_url, params=accounts_params)
print(f"Pages 回應: {accounts_response.json()}")
