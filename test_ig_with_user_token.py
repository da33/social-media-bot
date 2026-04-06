"""使用 User Token 直接發 IG 圖片"""
import requests
import time

# 你的 User Token（剛才取得的）
USER_TOKEN = "EAARZBU1qsymIBRNNUGOdL7F1kAwdlBKQVaNq903cBcMuCJQOyxTaKv8ZCRWUqQ7aGcZAUo2ItZC8ZCFSY3ueZCYbJDeKd7vlHOfDZAs1zXsSkQgHhoiiCGQNB9IKZAXHZCX3mdwGgoGa2ZAHt65WvNmWQP0YAvLX28Rf2rMXVIpFChYaQFnAwZCxx8yqbVzAmmiZB7mV"
IG_ACCOUNT_ID = "17841401987677377"

# MiniMax 測試圖片 URL
IMAGE_URL = "https://hailuo-image-algeng-data.oss-cn-wulanchabu.aliyuncs.com/image_inference_output%2Ftalkie%2Fprod%2Fimg%2F2026-04-07%2Fee8b3d1e-8c42-45f8-818f-a5e2ef1ee2ad_aigc.jpeg?Expires=1775579179&OSSAccessKeyId=LTAI5tB2SwrRwAtD23etQUbC&Signature=LR6R5uzLpwS0%2ByT8fPlc3BClkEA%3D"

print("1. 建立 IG 容器...")
media_url = f"https://graph.facebook.com/v18.0/{IG_ACCOUNT_ID}/media"

media_payload = {
    "caption": "測試發文\n.\n.\n.\n#test",
    "image_url": IMAGE_URL,
    "access_token": USER_TOKEN
}

media_response = requests.post(media_url, data=media_payload)
media_result = media_response.json()

print(f"結果: {media_result}")

if "id" not in media_result:
    print("❌ 容器建立失敗")
    if "error" in media_result:
        print(f"錯誤: {media_result['error'].get('message')}")
    exit(1)

creation_id = media_result["id"]
print(f"✅ 容器建立成功！ID: {creation_id}")

# 等待
print("\n2. 等待 IG 處理...")
time.sleep(30)

# 發布
print("\n3. 發布...")
publish_url = f"https://graph.facebook.com/v18.0/{IG_ACCOUNT_ID}/media_publish"
publish_payload = {
    "creation_id": creation_id,
    "access_token": USER_TOKEN
}

publish_response = requests.post(publish_url, data=publish_payload)
publish_result = publish_response.json()
print(f"發布結果: {publish_result}")

if "id" in publish_result:
    print(f"\n✅ 發布成功！ID: {publish_result['id']}")
else:
    print(f"❌ 發布失敗")
    if "error" in publish_result:
        print(f"錯誤: {publish_result['error'].get('message')}")
