"""
Twitter/X 自動化機器人
使用 Tweepy 實現自動發文和回覆
"""
import tweepy
import random
import time
import os

class TwitterBot:
    def __init__(self):
        self.api = self.authenticate()
        self.client = self.get_client()
        self.promotion_link = 'https://rggo5269.com/#/ag/win99'
    
    def authenticate(self):
        """認證 Twitter API v1.1"""
        consumer_key = os.getenv('TW_API_KEY')
        consumer_secret = os.getenv('TW_API_SECRET')
        access_token = os.getenv('TW_ACCESS_TOKEN')
        access_token_secret = os.getenv('TW_ACCESS_SECRET')
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        try:
            api.verify_credentials()
            print("✅ Twitter 認證成功")
            return api
        except Exception as e:
            print(f"❌ Twitter 認證失敗：{e}")
            raise
    
    def get_client(self):
        """獲取 Twitter API v2 客戶端"""
        return tweepy.Client(
            consumer_key=os.getenv('TW_API_KEY'),
            consumer_secret=os.getenv('TW_API_SECRET'),
            access_token=os.getenv('TW_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TW_ACCESS_SECRET')
        )
    
    def post_tweet(self, text):
        """發布推文"""
        try:
            # Twitter 限制 280 字
            if len(text) > 280:
                text = text[:277] + '...'
            
            response = self.client.create_tweet(text=text)
            print(f"✅ 推文發布成功：{text[:50]}...")
            
            # 隨機延遲
            delay = random.randint(60, 180)
            print(f"⏰ 等待 {delay} 秒...")
            time.sleep(delay)
            
            return response
        except Exception as e:
            print(f"❌ 推文失敗：{e}")
            return None
    
    def get_keyword_reply(self, text):
        """根據關鍵字生成回覆"""
        text = text.lower()
        
        replies = {
            '註冊': f'🎰 富遊娛樂城\n✨ 註冊：{self.promotion_link}\n🎁 送$168',
            '代理': '💰 代理招募中！\n📊 抽成5-15%\nDM我了解詳情',
            '攻略': '🎮 戰神賽特攻略\n📌 能量條半滿加注\nDM我獲取完整攻略',
            '優惠': f'🎁 新手福利\n💰 註冊送$168\n💎 首儲1000送1000\n{self.promotion_link}'
        }
        
        for keyword, reply in replies.items():
            if keyword in text:
                return reply
        
        return f'您好！富遊娛樂城客服 🎰\n需要：註冊/優惠/代理/攻略\nDM我服務！'
    
    def reply_to_mentions(self):
        """回覆提及"""
        try:
            # 獲取最近的提及
            mentions = self.api.mentions_timeline(count=10)
            
            for mention in mentions:
                # 檢查是否已回覆（簡單檢查）
                try:
                    # 生成回覆
                    reply_text = self.get_keyword_reply(mention.text)
                    reply_text = f"@{mention.user.screen_name} {reply_text}"
                    
                    # 發送回覆
                    self.api.update_status(
                        reply_text,
                        in_reply_to_status_id=mention.id,
                        auto_populate_reply_metadata=True
                    )
                    
                    print(f"✅ 已回覆 @{mention.user.screen_name}")
                    time.sleep(random.randint(30, 60))
                    
                except tweepy.TweepyException as e:
                    if 'duplicate' in str(e).lower():
                        print(f"⚠️ 已回覆過 @{mention.user.screen_name}")
                    else:
                        print(f"❌ 回覆失敗：{e}")
            
            print("✅ 提及檢查完成")
        except Exception as e:
            print(f"❌ 檢查提及失敗：{e}")
    
    def like_tweets(self, keyword, count=10):
        """點讚相關推文"""
        try:
            tweets = self.api.search_tweets(q=keyword, count=count, lang='zh')
            
            for tweet in tweets:
                try:
                    self.api.create_favorite(tweet.id)
                    print(f"✅ 已點讚：{tweet.text[:30]}...")
                    time.sleep(random.randint(30, 60))
                except:
                    pass
            
            print(f"✅ 完成點讚 {count} 個推文")
        except Exception as e:
            print(f"❌ 點讚失敗：{e}")

if __name__ == "__main__":
    # 測試
    bot = TwitterBot()
    
    # 測試發文
    test_tweet = "🔥 測試推文\n\n這是自動化系統測試"
    bot.post_tweet(test_tweet)
    
    # 測試回覆
    bot.reply_to_mentions()
