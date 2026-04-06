"""
Instagram 發布模組（支援 MiniMax AI 生成圖片）
圖片會根據內容話題生成
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
        self.customer_service_link = "https://l.threads.com/?u=https%3A%2F%2Flin.ee%2FVjQOag7%3Futm_source%3Dthreads%26utm_medium%3Dsocial%26utm_content%3Dlink_in_bio"
        
        # 根據話題對應的圖片 prompt（簡單版本，避免複雜描述導致生成失敗）
        # 富遊/RG 風格：深藍 + 金色
        self.topic_image_prompts = {
            "出金紀錄": [
                "Luxury casino theme with gold coins and money, deep blue background, 3:4",
                "Gold coins spilling from slot machine, casino rich atmosphere, deep navy blue, 3:4",
            ],
            "出金速度": [
                "Casino winning moment with gold coins, fast withdrawal concept, deep blue theme, 3:4",
                "Clock and gold coins, quick payout concept, luxury casino style, navy blue, 3:4",
            ],
            "出金頻率": [
                "Gold coins and calendar, regular withdrawal concept, casino theme, deep blue, 3:4",
                "Wallet full of gold coins, frequent rewards, luxury casino atmosphere, navy blue, 3:4",
            ],
            "出金": [
                "Gold coins and casino chips, wealth concept, deep navy blue background, 3:4",
                "Slot machine jackpot with gold coins, casino winning moment, deep blue theme, 3:4",
            ],
            "風險提醒": [
                "Responsible gambling concept, gold coins and warning sign, deep blue theme, 3:4",
                "Casino chips with caution concept, thoughtful gambling, navy blue background, 3:4",
            ],
            "心態分享": [
                "Relaxed person with casino chips, peaceful gambling mindset, blue atmosphere, 3:4",
                "Calm casino lifestyle, gold coins and relaxation, deep blue theme, 3:4",
            ],
            "風控觀念": [
                "Budget planning with casino chips, gold coins, financial control concept, navy blue, 3:4",
                "Savings piggy bank with gold coins, smart gambling finance, deep blue background, 3:4",
            ],
            "平台穩定": [
                "Secure casino platform concept, shield and gold coins, deep blue theme, 3:4",
                "Trusted online casino, verified badge with gold coins, professional navy blue, 3:4",
            ],
            "平台選擇": [
                "Best casino choice with gold trophy, deep blue winning theme, 3:4",
                "Premium casino platform, gold coins and star rating, professional blue background, 3:4",
            ],
            "優惠使用": [
                "Casino bonus reward with gift box and gold coins, promotional concept, deep blue, 3:4",
                "Gift box full of gold coins, casino bonus celebration, luxury navy blue theme, 3:4",
            ],
            "優惠真相": [
                "Casino bonus with magnifying glass, bonus evaluation concept, deep blue theme, 3:4",
                "Gold coins with transparent scale, fair bonus assessment, casino theme, navy blue, 3:4",
            ],
            "新人問題": [
                "New casino player with question mark, newcomer guide concept, deep blue theme, 3:4",
                "Casino entrance with welcome sign, new player atmosphere, gold accents, navy blue, 3:4",
            ],
            "客戶疑問": [
                "Customer support chat with gold coins, casino help concept, deep blue background, 3:4",
                "Help desk with casino theme, gold coins and assistance, professional navy blue, 3:4",
            ],
            "客戶故事": [
                "Happy casino player with gold coins, success story concept, deep blue celebration, 3:4",
                "Two people sharing casino experience, testimonial scene, luxury navy blue theme, 3:4",
            ],
            "日常分享": [
                "Casual evening with casino app, relaxed lifestyle concept, blue cozy atmosphere, 3:4",
                "Home relaxing with gold coins, casual gambling lifestyle, deep blue theme, 3:4",
            ],
        }
        
        # 通用圖片（當話題沒有對應時使用）
        self.default_image_prompts = [
            "Luxury casino theme with gold coins, deep navy blue background, elegant gambling atmosphere, 3:4",
            "Premium online casino platform, gold coins and sophisticated style, deep blue, 3:4",
            "Elegant casino night atmosphere, deep blue background with golden light, luxury gambling vibe, 3:4",
            "Professional gaming aesthetic, rich blue and gold casino theme, sophisticated atmosphere, 3:4",
            "Sleek casino entertainment design, navy blue and gold theme, modern gambling style, 3:4",
        ]
    
    def get_image_prompt_for_topic(self, topic):
        """根據話題取得對應的圖片 prompt"""
        # 嘗試找完全匹配的話題
        for key in self.topic_image_prompts:
            if key in topic:
                return random.choice(self.topic_image_prompts[key])
        
        # 嘗試部分匹配
        for key, prompts in self.topic_image_prompts.items():
            if topic in key:
                return random.choice(prompts)
        
        # 使用預設圖片
        return random.choice(self.default_image_prompts)
    
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
    
    def post_with_ai_image(self, caption, topic=None):
        """使用 MiniMax AI 生成的圖片發文到 IG"""
        # 根據話題選擇圖片 prompt
        if topic:
            prompt = self.get_image_prompt_for_topic(topic)
        else:
            prompt = random.choice(self.default_image_prompts)
        
        # 生成圖片
        print(f"🎨 生成 IG 配圖（話題：{topic}）...")
        print(f"   Prompt: {prompt[:60]}...")
        image_url = self.image_gen.generate_image(custom_prompt=prompt)
        
        if not image_url:
            print("❌ 圖片生成失敗，跳過 IG 發文")
            return None
        
        # 加入客服連結到 caption
        full_caption = f"{caption}\n\n📩 有問題可私訊：{self.customer_service_link}"
        
        # 建立容器
        print(f"📦 建立 IG 容器...")
        container_id = self.create_media_container(image_url, full_caption)
        
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
    
    # 測試不同話題的圖片
    topics = ["出金紀錄", "心態分享", "優惠使用", "風險提醒"]
    
    for topic in topics:
        print(f"\n{'='*50}")
        print(f"測試話題：{topic}")
        prompt = client.get_image_prompt_for_topic(topic)
        print(f"圖片 Prompt：{prompt[:80]}...")
