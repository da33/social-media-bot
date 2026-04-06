"""
Instagram 發布模組（支援 MiniMax AI 生成圖片）
"""
import requests
import time
import os
import random
from image_generator import ImageGenerator

class InstagramPublisher:
    def __init__(self, access_token=None, account_id=None):
        self.access_token = access_token or os.getenv('IG_ACCESS_TOKEN')
        self.account_id = account_id or os.getenv('IG_ACCOUNT_ID')
        self.base_url = "https://graph.instagram.com/v18.0"
        self.image_gen = ImageGenerator()
        
        # IG 圖片風格 prompt
        self.image_prompts = [
            "Luxurious casino slot machine theme with golden coins and soft warm lighting elegant atmosphere digital art style",
            "Modern online gaming platform interface with colorful game icons and neon lights gaming setup digital art",
            "Abstract golden patterns with luxurious casino elements and elegant geometric design digital art",
            "A relaxing person enjoying online entertainment at home with cozy atmosphere and warm lighting digital art",
            "Minimalist design with gold accents and simple casino theme elements modern aesthetic digital art",
        ]
    
    def create_media_container(self, image_url, caption):
        """建立媒體容器"""
        url = f"{self.base_url}/{self.account_id}/media"
        
        payload = {
            "caption": caption,
            "image_url": image_url,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        if "id" in result:
            return result["id"]
        return None
    
    def wait_for_media_ready(self, container_id, max_wait=60):
        """等待媒體處理完成"""
        url = f"{self.base_url}/{container_id}"
        params = {
            "access_token": self.access_token,
            "fields": "status,status_code"
        }
        
        for i in range(max_wait):
            response = requests.get(url, params=params)
            result = response.json()
            
            if result.get("status") == "FINISHED":
                return True
            
            time.sleep(2)
        
        return False
    
    def publish_media(self, container_id):
        """發布媒體"""
        url = f"{self.base_url}/{self.account_id}/media_publish"
        
        payload = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        if "id" in result:
            return result["id"]
        return None
    
    def post_with_ai_image(self, caption):
        """使用 MiniMax AI 生成的圖片發文到 IG"""
        # 隨機選擇一個圖片風格
        prompt = random.choice(self.image_prompts)
        
        # 生成圖片
        print(f"🎨 生成 IG 配圖...")
        image_url = self.image_gen.generate_image(custom_prompt=prompt)
        
        if not image_url:
            print("❌ 圖片生成失敗，跳過 IG 發文")
            return None
        
        # 建立容器
        print(f"📦 建立 IG 容器...")
        container_id = self.create_media_container(image_url, caption)
        
        if not container_id:
            print("❌ 容器建立失敗")
            return None
        
        # 等待處理
        print(f"⏳ 等待 IG 處理圖片...")
        if not self.wait_for_media_ready(container_id):
            print("❌ 圖片處理超時")
            return None
        
        # 發布
        print(f"🚀 發布到 IG...")
        post_id = self.publish_media(container_id)
        
        if post_id:
            print(f"✅ IG 發文成功！ID: {post_id}")
        else:
            print("❌ IG 發文失敗")
        
        return post_id

if __name__ == "__main__":
    client = InstagramPublisher()
    
    test_caption = "測試 AI 圖片 IG 發文\n.\n.\n.\n#test"
    result = client.post_with_ai_image(test_caption)
    print(f"\n結果: {result}")
