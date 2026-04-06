"""
社群媒體自動化排程系統
整合 Instagram/Threads 和 Twitter
"""
import schedule
import time
import json
import random
import os
from datetime import datetime
from bots.instagram_bot_official import InstagramBotOfficial
from bots.twitter_bot import TwitterBot

class SocialMediaScheduler:
    def __init__(self):
        print("🤖 初始化自動化系統...")
        self.ig_bot = InstagramBotOfficial()
        self.tw_bot = TwitterBot()
        self.posts = self.load_content()
        self.used_posts = []
    
    def load_content(self):
        """載入內容庫"""
        try:
            with open('content/posts.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
                print(f"✅ 載入 {len(posts)} 篇內容")
                return posts
        except FileNotFoundError:
            print("❌ 找不到 posts.json，使用預設內容")
            return self.get_default_posts()
    
    def get_default_posts(self):
        """預設內容（如果沒有 posts.json）"""
        return [
            {
                "text": "🔥【ATG戰神賽特】富遊獨家開放！\n\n💰 最高81,000倍大獎等你拿\n⚡ 96.89%超高回報率\n\n立即試玩👉 https://rggo5269.com/#/ag/win99\n\n#戰神賽特 #富遊娛樂城",
                "type": "game_promo"
            },
            {
                "text": "🏆 為什麼選擇富遊娛樂城？\n\n✅ 2025台灣娛樂城推薦第一名\n✅ 100%保證出金\n✅ 5分鐘快速到帳\n\n立即加入👉 https://rggo5269.com/#/ag/win99\n\n#富遊娛樂城 #線上娛樂城",
                "type": "brand"
            }
        ]
    
    def get_random_post(self):
        """隨機選擇一篇未使用的內容"""
        available_posts = [p for p in self.posts if p not in self.used_posts]
        
        # 如果都用完了，重置
        if not available_posts:
            self.used_posts = []
            available_posts = self.posts
        
        post = random.choice(available_posts)
        self.used_posts.append(post)
        return post
    
    def post_to_threads(self):
        """發布到 Threads"""
        try:
            post = self.get_random_post()
            print(f"\n📱 [Threads] 準備發文...")
            self.ig_bot.post_threads(post['text'])
        except Exception as e:
            print(f"❌ Threads 發文失敗：{e}")
    
    def post_to_twitter(self):
        """發布到 Twitter"""
        try:
            post = self.get_random_post()
            print(f"\n🐦 [Twitter] 準備發文...")
            
            # Twitter 限制 280 字
            text = post['text']
            if len(text) > 280:
                text = text[:277] + '...'
            
            self.tw_bot.post_tweet(text)
        except Exception as e:
            print(f"❌ Twitter 發文失敗：{e}")
    
    def post_to_all_platforms(self):
        """發布到所有平台"""
        print(f"\n{'='*50}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🚀 開始發布到所有平台...")
        print(f"{'='*50}")
        
        post = self.get_random_post()
        
        # 發布到 Threads
        try:
            print(f"\n📱 [Threads] 發布中...")
            self.ig_bot.post_threads(post['text'])
        except Exception as e:
            print(f"❌ Threads 失敗：{e}")
        
        # 隨機延遲
        delay = random.randint(30, 90)
        print(f"\n⏰ 等待 {delay} 秒後發布到 Twitter...")
        time.sleep(delay)
        
        # 發布到 Twitter
        try:
            print(f"\n🐦 [Twitter] 發布中...")
            text = post['text']
            if len(text) > 280:
                text = text[:277] + '...'
            self.tw_bot.post_tweet(text)
        except Exception as e:
            print(f"❌ Twitter 失敗：{e}")
        
        print(f"\n✅ 本次發布完成！")
    
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
        
        # 小規模測試：每天只發 2 次
        schedule.every().day.at("12:00").do(self.post_to_all_platforms)
        schedule.every().day.at("20:00").do(self.post_to_all_platforms)
        
        print("✅ 發文排程：12:00, 20:00 (測試模式)")
        
        # 每 2 小時檢查私訊（降低頻率）
        schedule.every(2).hours.do(self.auto_reply)
        print("✅ 回覆排程：每 2 小時")
        
        # 暫時關閉自動互動（測試階段）
        # schedule.every(2).hours.do(self.auto_interact)
        print("✅ 互動排程：已關閉（測試模式）")
    
    def run(self):
        """運行排程系統"""
        print("\n" + "="*50)
        print("🤖 社群媒體自動化系統")
        print("="*50)
        print(f"📅 啟動時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 Instagram/Threads：waterboy_rix")
        print(f"🐦 Twitter：已連接")
        print(f"📝 內容庫：{len(self.posts)} 篇")
        print("="*50)
        
        self.setup_schedule()
        
        print("\n✅ 系統運行中...")
        print("💡 提示：按 Ctrl+C 停止\n")
        
        # 立即執行一次發文測試
        print("🧪 執行初始發文測試...")
        self.post_to_all_platforms()
        
        # 開始排程循環
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分鐘檢查一次

if __name__ == "__main__":
    try:
        scheduler = SocialMediaScheduler()
        scheduler.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ 系統已停止")
    except Exception as e:
        print(f"\n\n❌ 系統錯誤：{e}")
