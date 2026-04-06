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
        
        # 根據話題對應的圖片風格（富遊/RG 風格：深藍 + 金色）
        self.topic_image_prompts = {
            "出金紀錄": [
                "Gold coins spilling from slot machine, deep navy blue background, luxurious casino atmosphere, golden light effects, professional digital art, 4:5 aspect ratio",
                "Person withdrawing money from ATM at casino, gold coins scattered around, deep blue and gold color theme, professional digital art, 4:5",
            ],
            "出金速度": [
                "Clock with gold coins, fast forward concept, deep navy blue background, casino theme, time pressure visualization, digital art, 4:5",
                "Speed meter with golden needle, casino luxury background, deep blue and gold theme, fast withdrawal concept, digital art, 4:5",
            ],
            "出金頻率": [
                "Calendar with gold coins, monthly schedule concept, deep navy blue background, casino elements, professional digital art, 4:5",
                "Wallet filling with gold coins, recurring income concept, deep blue and gold branding, casino luxury feel, digital art, 4:5",
            ],
            "出金": [
                "Gold coins and banknote, casino wealth concept, deep navy blue and gold theme, professional digital art, 4:5 aspect ratio",
                "Slot machine paying out gold coins, casino winning moment, deep blue background with golden glow, digital art, 4:5",
            ],
            "風險提醒": [
                "Person thinking carefully at casino, blue mood lighting, gold accents, responsible gambling theme, digital art, 4:5",
                "Warning sign with gold coins, careful gambling concept, deep navy blue background, professional warning atmosphere, digital art, 4:5",
            ],
            "心態分享": [
                "Person relaxing at home peacefully, smartphone showing casino app, cozy blue evening atmosphere, gold accents, digital art, 4:5",
                "Calm meditation pose with casino chips, balance lifestyle concept, deep blue and gold theme, peaceful gambling mindset, digital art, 4:5",
            ],
            "風控觀念": [
                "Calculator with casino chips, budget planning concept, deep navy blue background, gold accents, professional digital art, 4:5",
                "Piggy bank with gold coins, savings concept, casino theme, deep blue and gold color scheme, digital art, 4:5",
            ],
            "平台穩定": [
                "Strong building with casino logo, stable platform concept, deep navy blue and gold architecture, professional digital art, 4:5",
                "Shield with gold checkmark, verified casino platform, security concept, deep blue background, professional digital art, 4:5",
            ],
            "平台選擇": [
                "Compare different casino platforms, deep blue comparison interface, gold trophy on top, professional digital art, 4:5",
                "Finger pointing at winning platform, choice concept, deep navy blue background, gold winner spotlight, digital art, 4:5",
            ],
            "優惠使用": [
                "Gift box with gold ribbon, casino bonus reward, deep navy blue background, promotional atmosphere, digital art, 4:5",
                "Gold bonus coins with gift bow, special offer concept, deep blue and gold celebration theme, digital art, 4:5",
            ],
            "優惠真相": [
                "Magnifying glass examining casino bonus terms, gold coins under examination, deep blue detective theme, professional digital art, 4:5",
                "Scale balancing casino rewards, realistic bonus evaluation concept, deep navy blue and gold theme, professional digital art, 4:5",
            ],
            "新人問題": [
                "New player entering luxury casino, confused but curious expression, deep navy blue entrance, gold door lights, welcoming digital art, 4:5",
                "Question mark above new player head at casino, deep blue background, gold question mark, newcomer guidance concept, digital art, 4:5",
            ],
            "客戶疑問": [
                "Customer service chat bubble with gold question mark, casino support concept, deep navy blue background, professional digital art, 4:5",
                "Person asking question at casino desk, customer inquiry concept, deep blue and gold theme, professional atmosphere, digital art, 4:5",
            ],
            "客戶故事": [
                "Two people at casino sharing experience, conversation story concept, deep navy blue lounge atmosphere, gold accents, digital art, 4:5",
                "Customer testimonial scene at casino, satisfied player with thumb up, gold reward, deep blue background, professional digital art, 4:5",
            ],
            "日常分享": [
                "Person casually browsing casino app at coffee shop, relaxed lifestyle concept, cozy evening atmosphere, blue and gold theme, digital art, 4:5",
                "Casual evening at home with smartphone, entertainment lifestyle, cozy blue lighting, gold casino elements, relaxed digital art, 4:5",
            ],
        }
        
        # 通用圖片（當話題沒有對應時使用）
        self.default_image_prompts = [
            "Luxurious casino lifestyle, deep navy blue and gold theme, elegant gambling atmosphere, professional digital art, 4:5 aspect ratio",
            "Modern online entertainment platform, blue and gold branding, sophisticated casino elements, premium feel, digital art, 4:5",
            "Elegant casino night atmosphere, deep blue background with golden light, slot machine silhouette, high-end gambling vibe, digital art, 4:5",
            "Professional gaming platform aesthetic, rich blue and gold color scheme, casino chips and cards, luxurious yet trustworthy, digital art, 4:5",
            "Sleek casino entertainment design, navy blue and gold theme, golden light effects, modern gambling atmosphere, digital art, 4:5",
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
