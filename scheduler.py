"""
社群媒體自動化排程系統
整合 AI內容生成 + Instagram/Threads + Twitter
ENI 定制版 - 四人格輪換系統
"""
import schedule
import time
import json
import random
import os
from datetime import datetime
from bots.instagram_bot_official import InstagramBotOfficial
from bots.twitter_bot import TwitterBot
from content_generator import ContentGenerator

class SocialMediaScheduler:
    def __init__(self):
        print("🤖 初始化自動化系統...")
        print("📝 使用 ENI 內容生成器（四人格輪換）...")
        
        # 初始化 AI 內容生成器
        self.ai_gen = ContentGenerator(personas_dir="personas")
        
        # 初始化平台機器人
        self.ig_bot = InstagramBotOfficial()
        self.tw_bot = TwitterBot()
        
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
        """備用內容（當 AI 生成失敗時）"""
        return [
            {
                "persona_name": "實話實說型",
                "content": f"出金了\n\n金額：{random.choice(['3200', '5800', '12000'])}\n耗時：{random.choice(['15分鐘', '20分鐘', '25分鐘'])}\n\n沒問題\n\n連結：https://rggo5269.com/#/ag/win99",
                "link": "https://rggo5269.com/#/ag/win99"
            }
        ]
    
    def post_to_threads(self, post):
        """發布到 Threads"""
        try:
            print(f"\n📱 [Threads] 準備發文...")
            print(f"   人格：{post['persona_name']}")
            print(f"   內容：{post['content'][:80]}...")
            
            self.ig_bot.post_threads(post['content'])
            return True
        except Exception as e:
            print(f"❌ Threads 發文失敗：{e}")
            return False
    
    def post_to_twitter(self, post):
        """發布到 Twitter"""
        try:
            print(f"\n🐦 [Twitter] 準備發文...")
            
            # Twitter 280字限制
            text = post['content']
            if len(text) > 280:
                text = text[:277] + '...'
            
            self.tw_bot.post_tweet(text)
            return True
        except Exception as e:
            print(f"❌ Twitter 發文失敗：{e}")
            return False
    
    def scheduled_post(self):
        """排程發文（09:00 / 14:00 / 21:00）"""
        time_slot = self.post_times[self.current_time_index]
        self.current_time_index = (self.current_time_index + 1) % len(self.post_times)
        
        print(f"\n{'='*50}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {time_slot}")
        print(f"🚀 開始發文...")
        print(f"{'='*50}")
        
        # 生成內容
        posts = self.generate_content()
        
        # 根據時段選擇內容
        if self.current_time_index == 0:
            post = posts[0]  # 第一篇（09:00 或第一個時段）
        elif self.current_time_index == 1:
            post = posts[1] if len(posts) > 1 else posts[0]
        else:
            post = posts[2] if len(posts) > 2 else posts[0]
        
        print(f"\n📝 使用內容：")
        print(f"   人格：{post['persona_name']}")
        print(f"   話題：{post.get('topic', 'N/A')}")
        print(f"   內容：\n{post['content'][:200]}...\n")
        
        # 發布到 Threads
        threads_result = self.post_to_threads(post)
        
        # 隨機延遲
        delay = random.randint(30, 90)
        print(f"\n⏰ 等待 {delay} 秒後發布到 Twitter...")
        time.sleep(delay)
        
        # 發布到 Twitter
        twitter_result = self.post_to_twitter(post)
        
        if threads_result and twitter_result:
            print(f"\n✅ {time_slot} 發文完成！")
        else:
            print(f"\n⚠️ 部分發文失敗")
        
        return threads_result, twitter_result
    
    def auto_reply(self):
        """自動回覆所有平台"""
        print(f"\n{'='*50}")
        print(f"💬 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 檢查私訊和提及...")
        print(f"{'='*50}")
        
        # Instagram/Threads 私訊
        try:
            print(f"\n📱 [Instagram/Threads] 檢查私訊...")
            self.ig_bot.auto_reply_dms()
        except Exception as e:
            print(f"❌ Instagram 回覆失敗：{e}")
        
        # Twitter 提及
        try:
            print(f"\n🐦 [Twitter] 檢查提及...")
            self.tw_bot.reply_to_mentions()
        except Exception as e:
            print(f"❌ Twitter 回覆失敗：{e}")
        
        print(f"\n✅ 回覆檢查完成！")
    
    def auto_interact(self):
        """自動互動（點讚）"""
        print(f"\n{'='*50}")
        print(f"👍 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 自動互動...")
        print(f"{'='*50}")
        
        # Instagram 點讚
        try:
            hashtags = ['戰神賽特', '老虎機', '娛樂城']
            hashtag = random.choice(hashtags)
            print(f"\n📱 [Instagram] 點讚 #{hashtag}...")
            self.ig_bot.like_recent_posts(hashtag, amount=5)
        except Exception as e:
            print(f"❌ Instagram 互動失敗：{e}")
        
        # Twitter 點讚
        try:
            keywords = ['戰神賽特', '老虎機', '線上娛樂']
            keyword = random.choice(keywords)
            print(f"\n🐦 [Twitter] 點讚 {keyword}...")
            self.tw_bot.like_tweets(keyword, count=5)
        except Exception as e:
            print(f"❌ Twitter 互動失敗：{e}")
        
        print(f"\n✅ 互動完成！")
    
    def setup_schedule(self):
        """設定排程"""
        print("\n⏰ 設定發文排程...")
        
        # 三次發文：09:00 / 14:00 / 21:00
        schedule.every().day.at("09:00").do(self.scheduled_post)
        schedule.every().day.at("14:00").do(self.scheduled_post)
        schedule.every().day.at("21:00").do(self.scheduled_post)
        
        print("✅ 發文排程：09:00, 14:00, 21:00")
        
        # 每 2 小時檢查私訊
        schedule.every(2).hours.do(self.auto_reply)
        print("✅ 回覆排程：每 2 小時")
        
        # 自動互動（可選，暫時關閉）
        # schedule.every(2).hours.do(self.auto_interact)
        print("✅ 互動排程：已關閉")
    
    def run(self):
        """運行排程系統"""
        print("\n" + "="*50)
        print("🤖 社群媒體自動化系統")
        print("   ENI 定制版 - 四人格輪換")
        print("="*50)
        print(f"📅 啟動時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 Instagram/Threads：waterboy_rix")
        print(f"🐦 Twitter：已連接")
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
        
        # 立即執行一次發文測試
        print("\n🧪 執行初始發文測試...")
        self.scheduled_post()
        
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
