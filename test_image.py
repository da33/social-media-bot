"""測試 MiniMax 圖片生成"""
import requests

MINIMAX_API_KEY = "sk-cp-VddIVaDxNHMJ9CnaOZHfmsGuYKFeJkxrpxypFDhbD9NgNNXf8_i23ADxnrbhS0jswc1d7gsSp7j6gMfJaQ3uN-__XyM-fOzadpWQX3GS2Pn9FGYqjJekdSs"

url = "https://api.minimaxi.com/v1/image_generation"

headers = {
    "Authorization": f"Bearer {MINIMAX_API_KEY}",
    "Content-Type": "application/json"
}

# 測試不同的 prompt
prompts = [
    "Gold coins and casino chips on blue background, 3:4",
    "Luxury casino theme with gold coins, 3:4",
    "Casino slot machine with gold coins, 3:4",
]

for i, prompt in enumerate(prompts):
    print(f"\n測試 {i+1}: {prompt[:50]}...")
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "3:4",
        "num_images": 1
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    result = response.json()
    
    if result.get('base_resp', {}).get('status_code') == 0:
        if result.get('data', {}).get('image_urls'):
            print(f"✅ 成功！URL: {result['data']['image_urls'][0][:60]}...")
            break
        else:
            print(f"⚠️ 成功但 failed={result.get('metadata', {}).get('failed_count')}, success={result.get('metadata', {}).get('success_count')}")
    else:
        print(f"❌ 失敗: {result.get('base_resp', {}).get('status_msg', 'unknown error')}")
