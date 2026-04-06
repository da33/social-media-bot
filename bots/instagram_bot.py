"""
Instagram/Threads 自動化機器人
使用 Instagrapi 實現自動發文和回覆
"""
from instagrapi import Client
import json
import random
import time
import os

class InstagramBot:
    def __init__(self):
        self.cl = Client()
        self.username = os.getenv('IG_USERNAME', 'waterboy_rix')
        self.password = os.getenv('IG_PASSWORD')
        self.promotion_link = 'https://rggo5269.com/#/ag/win99'
        self.login()
    
    def login(self):
        """登入 Instagram/Threads"""
        try:
            # 嘗試從 session 恢復
            session_file = 'session.json'
            if os.path.exists(session_file):
                self.cl.load_settings(session_file)
                self.cl.login(self.username, self.password)
                print("✅ 從 session 恢復登入成功")
            else:
                self.cl.login(self.username, self.password)
                self.cl.dump_settings(session_file)
                print("✅ Instagram 登入成功")
        except Exception as e:
            print(f"❌ 登入失敗：{e}")
            raise
    
    def post_thread(self, text):
        """發布 Threads 貼文"""
        try:
            # Threads 使用 Instagram API
            media = self.cl.post_thread(text)
            print(f"✅ Threads 發文成功：{text[:50]}...")
            
            # 隨機延遲（模擬真人）
            delay = random.randint(60, 180)
            print(f"⏰ 等待 {delay} 秒...")
            time.sleep(delay)
            
            return media
        except Exception as e:
            print(f"❌ Threads 發文失敗：{e}")
            return None
    
    def post_photo(self, image_path, caption):
        """發布 Instagram 圖片貼文"""
        try:
            media = self.cl.photo_upload(image_path, caption)
            print(f"✅ Instagram 發文成功：{caption[:50]}...")
            
            # 隨機延遲
            delay = random.randint(60, 180)
            time.sleep(delay)
            
            return media
        except Exception as e:
            print(f"❌ Instagram 發文失敗：{e}")
            return None
    
    def get_keyword_reply(self, message):
        """根據關鍵字獲取回覆"""
        message = message.lower()
        
        # 關鍵字回覆映射
        replies = {
            '註冊': f'🎰 歡迎來到富遊娛樂城！\n\n✨ 立即註冊：{self.promotion_link}\n🎁 註冊送$168 + 首儲1000送1000\n\n有問題隨時問我！',
            '連結': f'👉 富遊註冊連結：{self.promotion_link}\n\n新手福利超豐富！',
            '代理': '💰 富遊代理招募中！\n📊 玩家充值抽成 5-15%\n✅ 月入10萬+不是夢\n\n私訊我「代理資料」了解詳情！',
            '攻略': '🎮 戰神賽特爆分攻略\n📌 能量條半滿時加注\n📌 聖甲蟲出現抓緊機會\n\n更多攻略私訊我！',
            '優惠': f'🎁 富遊新手福利\n💰 註冊送$168\n💎 首儲1000送1000\n\n立即領取：{self.promotion_link}',
            '出金': '💰 富遊100%保證出金！\n✅ 5分鐘內到帳\n🔒 過億資本額保障\n\n放心玩！'
        }
        
        # 檢查關鍵字
        for keyword, reply in replies.items():
            if keyword in message:
                return reply
        
        # 預設回覆
        return f'您好！我是富遊娛樂城客服 🎰\n\n請告訴我您需要：\n• 註冊、連結\n• 優惠、活動\n• 代理、賺錢\n• 攻略、技巧\n\n我會立即為您服務！'
    
    def reply_dm(self, thread_id, message):
        """回覆私訊"""
        try:
            self.cl.direct_send(message, thread_ids=[thread_id])
            print(f"✅ 回覆私訊成功")
            time.sleep(random.randint(30, 60))
        except Exception as e:
            print(f"❌ 回覆失敗：{e}")
    
    def auto_reply_dms(self):
        """自動回覆私訊"""
        try:
            # 獲取最近的私訊
            threads = self.cl.direct_threads(amount=20)
            
            for thread in threads:
                # 獲取最後一條訊息
                if thread.messages:
                    last_message = thread.messages[0]
                    
                    # 如果不是自己發的，且未讀
                    if not last_message.is_sent_by_viewer:
                        message_text = last_message.text or ''
                        
                        # 生成回覆
                        reply = self.get_keyword_reply(message_text)
                        
                        # 發送回覆
                        self.reply_dm(thread.id, reply)
                        
                        print(f"✅ 已回覆用戶：{thread.users[0].username}")
            
            print("✅ 私訊檢查完成")
        except Exception as e:
            print(f"❌ 檢查私訊失敗：{e}")
    
    def like_recent_posts(self, hashtag, amount=10):
        """點讚相關貼文"""
        try:
            medias = self.cl.hashtag_medias_recent(hashtag, amount=amount)
            
            for media in medias:
                self.cl.media_like(media.id)
                print(f"✅ 已點讚：{media.caption_text[:30]}...")
                time.sleep(random.randint(30, 60))
            
            print(f"✅ 完成點讚 {amount} 個貼文")
        except Exception as e:
            print(f"❌ 點讚失敗：{e}")

if __name__ == "__main__":
    # 測試
    bot = InstagramBot()
    
    # 測試發文
    test_post = "🔥 測試貼文\n\n這是自動化系統測試"
    bot.post_thread(test_post)
    
    # 測試回覆
    bot.auto_reply_dms()
