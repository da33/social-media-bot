"""
Instagram 發布模組（支援 MiniMax AI 生成圖片）
圖片會根據內容話題生成
"""
import requests
import time
import os
import random
import hashlib
from image_generator import ImageGenerator

class InstagramPublisher:
    def __init__(self, access_token=None, account_id=None):
        self.access_token = access_token or os.getenv('IG_ACCESS_TOKEN')
        self.account_id = account_id or os.getenv('IG_ACCOUNT_ID')
        self.base_url = "https://graph.facebook.com/v18.0"
        self.image_gen = ImageGenerator()
        self.customer_service_link = "https://l.threads.com/?u=https%3A%2F%2Flin.ee%2FVjQOag7%3Futm_source%3Dthreads%26utm_medium%3Dsocial%26utm_content%3Dlink_in_bio"
        
        # 根據話題對應的圖片 prompt（保持簡單避免失敗）
        self.topic_image_prompts = {
            "出金紀錄": ["Gold coins on blue background, 3:4", "Gold coins spilling, casino theme, navy blue, 3:4"],
            "出金速度": ["Gold coins and clock, fast payout, blue theme, 3:4", "Gold coins, quick withdrawal, navy blue, 3:4"],
            "出金頻率": ["Gold coins and calendar, regular withdrawal, blue, 3:4", "Wallet with gold coins, frequent rewards, navy blue, 3:4"],
            "出金": ["Gold coins and chips, casino wealth, navy blue, 3:4", "Slot machine jackpot, gold coins, blue theme, 3:4"],
            "風險提醒": ["Gold coins and warning sign, responsible gambling, blue, 3:4", "Casino chips with caution, careful gambling, navy blue, 3:4"],
            "心態分享": ["Gold coins, relaxed gambling mindset, blue theme, 3:4", "Peaceful casino lifestyle, gold coins, navy blue, 3:4"],
            "風控觀念": ["Gold coins and calculator, budget planning, blue, 3:4", "Piggy bank with gold coins, savings, navy blue, 3:4"],
            "平台穩定": ["Gold coins and shield, trusted casino, blue theme, 3:4", "Verified badge gold coins, secure platform, navy blue, 3:4"],
            "平台選擇": ["Gold trophy and coins, best casino choice, blue, 3:4", "Premium casino gold coins, top rating, navy blue, 3:4"],
            "優惠使用": ["Gold coins and gift box, casino bonus, blue theme, 3:4", "Gift with gold coins, bonus reward, navy blue, 3:4"],
            "優惠真相": ["Gold coins and magnifying glass, bonus truth, blue, 3:4", "Scale gold coins, fair bonus, navy blue theme, 3:4"],
            "新人問題": ["Gold coins and question mark, new player, blue theme, 3:4", "Casino newcomer guide, gold coins, navy blue, 3:4"],
            "客戶疑問": ["Gold coins and chat bubble, casino support, blue, 3:4", "Help desk gold coins, customer service, navy blue, 3:4"],
            "客戶故事": ["Happy player gold coins, success story, blue theme, 3:4", "Gold coins celebration, satisfied customer, navy blue, 3:4"],
            "日常分享": ["Casual gold coins, relaxed lifestyle, blue theme, 3:4", "Home casino gold coins, evening entertainment, navy blue, 3:4"],
        }
        
        self.default_image_prompts = [
            "Gold coins on blue background, luxury casino, 3:4",
            "Premium casino gold coins, sophisticated blue theme, 3:4",
            "Elegant casino night, gold coins, deep blue, 3:4",
            "Professional gaming, gold coins, navy blue theme, 3:4",
            "Sleek casino entertainment, gold coins, blue style, 3:4",
        ]
    
    def get_image_prompt_for_topic(self, topic):
        """根據話題取得對應的圖片 prompt"""
        for key in self.topic_image_prompts:
            if key in topic:
                return random.choice(self.topic_image_prompts[key])
        
        for key, prompts in self.topic_image_prompts.items():
            if topic in key:
                return random.choice(prompts)
        
        return random.choice(self.default_image_prompts)
    
    def upload_image_url(self, image_url_or_path):
        """上傳圖片到 IG，返回 media_id（支援 URL 或本地路徑）"""
        url = f"{self.base_url}/{self.account_id}/media"
        
        # 判斷是 URL 還是本地路徑
        if image_url_or_path.startswith('http'):
            # URL 方式
            payload = {
                'image_url': image_url_or_path,
                'caption': ' ',
                'access_token': self.access_token
            }
            response = requests.post(url, data=payload)
        else:
            # 本地上傳方式
            with open(image_url_or_path, 'rb') as f:
                image_data = f.read()
            
            ext = os.path.splitext(image_url_or_path)[1].lower()
            mime_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
            
            files = {
                'media': (os.path.basename(image_url_or_path), image_data, mime_type)
            }
            
            data = {
                'caption': ' ',
                'access_token': self.access_token
            }
            
            response = requests.post(url, files=files, data=data)
        
        result = response.json()
        
        if "id" in result:
            print(f"✅ IG 容器創建成功：{result['id']}")
            return result["id"]
        
        print(f"❌ IG 容器創建失敗：{result}")
        return None
    
    def update_caption(self, media_id, caption):
        """更新貼文 caption"""
        url = f"{self.base_url}/{media_id}"
        
        payload = {
            'caption': caption,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        return "id" in result
    
    def wait_for_media_ready(self, media_id, max_wait=180):
        """等待媒體處理完成"""
        url = f"{self.base_url}/{media_id}"
        params = {
            "access_token": self.access_token,
            "fields": "status,status_code"
        }
        
        print(f"⏳ 等待 IG 處理圖片（最長 {max_wait} 秒）...")
        for i in range(max_wait):
            response = requests.get(url, params=params)
            result = response.json()
            
            status = result.get("status")
            print(f"   [{i+1}/{max_wait}] 狀態: {status}")
            
            if status == "FINISHED":
                print(f"✅ 圖片處理完成")
                return True
            
            if status == "ERROR":
                print(f"❌ 圖片處理錯誤：{result}")
                return False
            
            time.sleep(3)
        
        print(f"⚠️ 等待超時，但嘗試直接發布...")
        return True  #  超時也嘗試發布
    
    def publish_media(self, media_id):
        """發布媒體"""
        url = f"{self.base_url}/{self.account_id}/media_publish"
        
        payload = {
            "creation_id": media_id,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        if "id" in result:
            return result["id"]
        return None
    
    def post_with_ai_image(self, caption, topic=None):
        """使用 MiniMax AI 生成的圖片發文到 IG"""
        if topic:
            prompt = self.get_image_prompt_for_topic(topic)
        else:
            prompt = random.choice(self.default_image_prompts)
        
        # 生成圖片並上傳到 Cloudinary
        print(f"🎨 生成 IG 配圖（話題：{topic}）...")
        print(f"   Prompt: {prompt}")
        cloudinary_url = self.image_gen.generate_and_upload(custom_prompt=prompt)
        
        if not cloudinary_url:
            print("❌ 圖片生成/上傳失敗，跳過 IG 發文")
            return None
        
        print(f"☁️ Cloudinary URL: {cloudinary_url[:80]}...")
        
        # 加入客服連結到 caption
        full_caption = f"{caption}\n\n📩 有問題可私訊：{self.customer_service_link}"
        
        # 直接用 cloudinary URL 創建容器
        print(f"📤 上傳圖片到 IG（Cloudinary URL）...")
        media_id = self.upload_image_url(cloudinary_url)
        
        if not media_id:
            print("❌ 上傳失敗")
            return None
        
        # 更新 caption
        print(f"✏️ 更新 caption...")
        self.update_caption(media_id, full_caption)
        
        # 等待處理
        print(f"⏳ 等待 IG 處理圖片...")
        if not self.wait_for_media_ready(media_id):
            print("❌ 圖片處理超時")
            return None
        
        # 發布
        print(f"🚀 發布到 IG...")
        post_id = self.publish_media(media_id)
        
        if post_id:
            print(f"✅ IG 發文成功！ID: {post_id}")
        else:
            print("❌ IG 發文失敗")
        
        return post_id

if __name__ == "__main__":
    client = InstagramPublisher()
    result = client.post_with_ai_image("測試內容", "出金紀錄")
    print(f"\n結果: {result}")
