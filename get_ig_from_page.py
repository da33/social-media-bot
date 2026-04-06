"""使用 Page Token 取得 Instagram 帳號"""
import requests

PAGE_ID = "105912875759206"
PAGE_TOKEN = "EAARZBU1qsymIBRNNUGOdL7F1kAwdlBKQVaNq903cBcMuCJQOyxTaKv8ZCRWUqQ7aGcZAUo2ItZC8ZCFSY3ueZCYbJDeKd7vlHOfDZAs1zXsSkQgHhoiiCGQNB9IKZAXHZCX3mdwGgoGa2ZAHt65WvNmWQP0YAvLX28Rf2rMXVIpFChYaQFnAwZCxx8yqbVzAmmiZB7mV"

print("使用 Page Token 取得 Instagram 帳號...")

# 取得關聯的 Instagram 帳號
url = f"https://graph.facebook.com/v18.0/{PAGE_ID}"
params = {
    "fields": "instagram_business_account",
    "access_token": PAGE_TOKEN
}

response = requests.get(url, params=params)
result = response.json()

print(f"結果: {result}")

if "instagram_business_account" in result:
    ig_id = result["instagram_business_account"]["id"]
    print(f"\n✅ 找到 Instagram Business Account ID: {ig_id}")
    
    # 取得 Instagram 詳細資訊
    ig_url = f"https://graph.instagram.com/v18.0/{ig_id}"
    ig_params = {
        "fields": "id,username,account_type,media_count",
        "access_token": PAGE_TOKEN
    }
    ig_response = requests.get(ig_url, params=ig_params)
    ig_result = ig_response.json()
    print(f"Instagram 詳細資訊: {ig_result}")
else:
    print("\n❌ 找不到關聯的 Instagram Business Account")
    print("需要在 Meta Business Suite 將 Instagram 帳號與 Facebook Page 連接")
