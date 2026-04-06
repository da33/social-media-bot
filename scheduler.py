"""
社群媒體自動化排程系統
整合 AI內容生成 + Instagram/Threads + AI生成圖片
ENI 定制版 - 四人格輪換系統
"""
import schedule
import time
import random
import os
from datetime import datetime
from content_generator import AIContentGenerator
from instagram_client import InstagramPublisher

class SocialMediaScheduler:
    def __init__(self):
        print("🤖 初始化自動化系統...")
        print("📝 使用 ENI 內容生成器（四人格輪換 + AI 圖片）...")
        
        # 初始化 AI 內容生成器
        self.ai_gen = AIContentGenerator(personas_dir="personas")
        
        # 初始化 IG 發布器
        self.ig_publisher = InstagramPublisher()
        
        # 排程配置
        self.post_times = ["09:00", "14:00", "21:00"]
        self.current_time_index = 0
        
        print("✅ 系統初始化完成")
    
    def generate_content(self):
        """使用 AI 生成內容"""
        try:
            posts = self.ai_gen.generate_daily_posts()
            return posts
        except Exception as e:
            print(f"❌ AI 內容生成失敗：{e}")
            return self.get_fallback_posts()
    
    def get_fallback_posts(self):
        """備用內容"""
        return [
            {
                "persona_name": "實話實說型",
                "content": "今天出了一筆，具體金額就不說了。流程走完大概等了一下下，不算久。就這樣。",
                "link": "https://rggo5269.com/#/ag/win99"
            }
        ]
    
    def post_to_threads(self, post):
        """發布到 Threads"""
        try:
            print(f"\n📱 [Threads] 準備發文...")
            print(f"   人格：{post['persona_name']}")
            print(f"   內容：{post['content'][:80]}...")
            
            # TODO: 串接 Threads API
            # 目前 Threads API 需要 OAuth，這裡先略過
            print(f"   ⚠️ Threads API 串接待完成")
            return True
        except Exception as e:
            print(f"❌ Threads 發文失敗：{e}")
            return False
    
    def post_to_ig(self, post):
        """發布到 Instagram（帶 AI 生成的圖片）"""
        try:
            print(f"\n📸 [Instagram] 準備發文...")
            print(f"   人格：{post['persona_name']}")
            print(f"   內容：{post['content'][:80]}...")
            
            # 組合 caption（不加連結，避免被 IG 審查）
            caption = post['content']
            
            # 使用 AI 生成圖片並發布
            result = self.ig_publisher.post_with_ai_image(caption)
            
            if result:
                print(f"✅ IG 發文成功！ID: {result}")
                return True
            else:
                print("❌ IG 發文失敗")
                return False
                
        except Exception as e:
            print(f"❌ IG 發文失敗：{e}")
            return False
    
    def scheduled_post(self):
        """排程發文"""
        time_slot = self.post_times[self.current_time_index]
        self.current_time_index = (self.current_time_index + 1) % len(self.post_times)
        
        print(f"\n{'='*50}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {time_slot}")
        print(f"🚀 開始發文...")
        print(f"{'='*50}")
        
        # 生成內容
        posts = self.generate_content()
        
        # 根據時段選擇內容
        if self.current_time_index == 1:
            post = posts[0]
        elif self.current_time_index == 2:
            post = posts[1] if len(posts) > 1 else posts[0]
        else:
            post = posts[2] if len(posts) > 2 else posts[0]
        
        print(f"\n📝 使用內容：")
        print(f"   人格：{post['persona_name']}")
        print(f"   話題：{post.get('topic', 'N/A')}")
        print(f"   內容：\n{post['content'][:200]}...\n")
        
        # 發布到 Threads（純文字）
        threads_result = self.post_to_threads(post)
        
        # 隨機延遲
        delay = random.randint(30, 90)
        print(f"\n⏰ 等待 {delay} 秒後發布到 IG...")
        time.sleep(delay)
        
        # 發布到 IG（AI 生成圖片）
        ig_result = self.post_to_ig(post)
        
        if threads_result and ig_result:
            print(f"\n✅ {time_slot} 發文完成！")
        else:
            print(f"\n⚠️ 部分發文失敗")
        
        return threads_result, ig_result
    
    def setup_schedule(self):
        """設定排程"""
        print("\n⏰ 設定發文排程...")
        
        # 三次發文：09:00 / 14:00 / 21:00
        schedule.every().day.at("09:00").do(self.scheduled_post)
        schedule.every().day.at("14:00").do(self.scheduled_post)
        schedule.every().day.at("21:00").do(self.scheduled_post)
        
        print("✅ 發文排程：09:00, 14:00, 21:00")
    
    def run(self):
        """運行排程系統"""
        print("\n" + "="*50)
        print("🤖 社群媒體自動化系統")
        print("   ENI 定制版 - 四人格 + AI 圖片")
        print("="*50)
        print(f"📅 啟動時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📸 Instagram：AI 生成圖片 + 自動發文")
        print(f"📱 Threads：純文字發文")
        print(f"🤖 AI 內容生成：開啟")
        print(f"👥 人格：實話實說 / 低調專業 / 隨性分享 / 故事敘事")
        print(f"⏰ 發文時間：09:00 / 14:00 / 21:00")
        print("="*50)
        
        self.setup_schedule()
        
        print("\n✅ 系統運行中...")
        print("💡 提示：按 Ctrl+C 停止\n")
        
        # 測試內容生成
        print("🧪 測試 AI 內容生成...")
        posts = self.generate_content()
        for i, p in enumerate(posts):
            print(f"\n[{i+1}] {p['persona_name']} - {p.get('topic', 'N/A')}")
            print(f"    {p['content'][:100]}...")
        
        # 測試 IG 發文（可選）
        print("\n🧪 測試 IG AI 圖片發文...")
        print("（這會真的發文到 Instagram，確認串接正常）")
        # self.test_ig_post()
        
        # 開始排程循環
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    try:
        scheduler = SocialMediaScheduler()
        scheduler.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ 系統已停止")
    except Exception as e:
        print(f"\n\n❌ 系統錯誤：{e}")
        raise
