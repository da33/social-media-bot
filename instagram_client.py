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
        
        # 根據話題對應的圖片 prompt（高品質版本）
        self.topic_image_prompts = {
            "出金紀錄": [
                "Elegant stack of golden coins on premium dark blue velvet background, soft studio lighting, luxury fintech aesthetic, shallow depth of field, photorealistic, 4:5 ratio",
                "Glittering gold coins arranged in neat rows, dark navy background with subtle bokeh, professional product photography, cinematic lighting, 4:5"
            ],
            "出金速度": [
                "Golden coin falling into elegant glass jar, motion blur effect, dark blue gradient background, premium finance imagery, clean composition, 4:5",
                "Speed motion of gold coins, clock element subtly integrated, deep blue backdrop, professional photography style, 4:5"
            ],
            "出金頻率": [
                "Monthly calendar with golden coins, clean minimalist design, navy blue and gold color scheme, modern fintech aesthetic, 4:5",
                "Elegant savings jar filled with gold coins, warm soft lighting, dark blue background, professional lifestyle photography, 4:5"
            ],
            "出金": [
                "Luxurious golden coins on premium dark fabric, soft spotlight, high-end casino aesthetic, photorealistic, 4:5 ratio",
                "Stacked gold coins with subtle sparkle, dark blue gradient background, professional product shot, 4:5"
            ],
            "風險提醒": [
                "Golden coins with subtle warning element, clean minimalist design, navy blue and gold palette, responsible gambling theme, professional aesthetic, 4:5",
                "Elegant balance scale with gold coins, dark blue backdrop, professional infographic style, 4:5"
            ],
            "心態分享": [
                "Peaceful person relaxing with golden coins nearby, warm ambient lighting, dark blue background, lifestyle fintech aesthetic, 4:5",
                "Calm lifestyle scene with gold coins, soft shadows, navy blue tones, professional photography, 4:5"
            ],
            "風控觀念": [
                "Golden coins in transparent safe jar, calculator nearby, clean desk setup, navy blue accent, professional finance aesthetic, 4:5",
                "Organized budgeting scene with gold coins, minimalist design, dark blue palette, professional lifestyle, 4:5"
            ],
            "平台穩定": [
                "Golden shield with checkmark, secure lock element, dark blue gradient background, trust and security theme, professional design, 4:5",
                "Verified badge with gold coins, premium dark blue backdrop, security and reliability aesthetic, 4:5"
            ],
            "平台選擇": [
                "Golden trophy surrounded by gold coins, award winning concept, dark blue background, premium casino aesthetic, 4:5",
                "Top-rated luxury items with gold coins, ranking chart element, navy blue professional theme, 4:5"
            ],
            "優惠使用": [
                "Gift box opening with golden glow, bonus reward concept, dark blue festive background, premium unboxing aesthetic, 4:5",
                "Luxury gift with gold coins, celebration confetti subtle, navy blue palette, professional promotional style, 4:5"
            ],
            "優惠真相": [
                "Magnifying glass examining golden coins, transparent truth concept, dark blue investigative background, professional aesthetic, 4:5",
                "Balanced scale comparing gold coins, fair evaluation concept, navy blue minimalist design, 4:5"
            ],
            "新人問題": [
                "Golden coins with question mark, clean educational design, dark blue friendly background, welcoming fintech aesthetic, 4:5",
                "Help icon with gold coins, supportive design, navy blue professional palette, 4:5"
            ],
            "客戶疑問": [
                "Chat bubbles with golden coins, customer support concept, dark blue modern background, professional service aesthetic, 4:5",
                "Support desk with gold coins, friendly service scene, navy blue professional theme, 4:5"
            ],
            "客戶故事": [
                "Happy lifestyle moment with gold coins, celebration subtle, dark blue warm background, professional lifestyle photography, 4:5",
                "Success moment with golden coins, achievement concept, navy blue backdrop, premium aesthetic, 4:5"
            ],
            "日常分享": [
                "Cozy evening scene with gold coins nearby, warm ambient lighting, dark blue lifestyle aesthetic, professional photography, 4:5",
                "Relaxed lifestyle moment, gold coins as accent, navy blue modern interior, professional lifestyle, 4:5"
            ],
        }
        
        self.default_image_prompts = [
            "Luxury golden coins on premium dark blue velvet, soft studio lighting, high-end fintech aesthetic, photorealistic, 4:5",
            "Elegant gold coins arrangement, deep navy gradient background, professional product photography, cinematic lighting, 4:5",
            "Premium golden coins on sophisticated dark fabric, spotlight effect, luxury casino aesthetic, 4:5",
            "Clean minimalist gold coins composition, navy blue and gold color scheme, modern fintech design, 4:5",
            "Glittering gold coins, dark blue backdrop, professional studio lighting, luxury aesthetic, 4:5",
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
