"""
Instagram/Threads 官方 API 機器人
使用 Meta Graph API，不會被封 IP
"""
import requests
import json
import time
import os

class InstagramBotOfficial:
    def __init__(self):
        # Instagram 憑證
        self.ig_access_token = os.getenv('IG_ACCESS_TOKEN', 'IGAARUFCuQZAehBZAFk1c2h2S2xwZAVU3REFldjFfdVJFSU0zSlVVVHZA3ZA3JIaklrWGRnUXJuVzJJWnd0a2FLVXFNWWV3ZATQ4aDRMTmZAYV2NxRjlTLTdscGF3Y0ZAxUmV6STB1ZAlR5LXR2SmlRbWp5UnNDVTV3')
        self.ig_user_id = os.getenv('IG_USER_ID', '25120682830939078')
        
        # Threads 憑證
        self.threads_access_token = os.getenv('THREADS_ACCESS_TOKEN', 'THAAUyK8zbIj1BUVJtVTF5bFZAtMUxEQVl6c21qc3VqMW45NFZAYM29QRVgxNGhodXNRdWdvX21QS2dUWFV0NWZALRThuamswLUUzV2pGXzlaYUJYMDZA1RFZAYOEtTSnh4MmIzdFExNHEtUkVmQTlyNlZATOVRMUzZAiajk4eklXRkQzeGd4UQZDZD')
        self.threads_user_id = os.getenv('THREADS_USER_ID', '26112997131686434')
        
        self.promotion_link = 'https://rggo5269.com/#/ag/win99'
        
        print("✅ Instagram/Threads 官方 API 初始化成功")
    
    def post_threads(self, text):
        """發布 Threads 貼文（官方 API）"""
        try:
            # Step 1: 創建容器
            url = f"https://graph.threads.net/v1.0/{self.threads_user_id}/threads"
            
            payload = {
                'media_type': 'TEXT',
                'text': text,
                'access_token': self.threads_access_token
            }
            
            response = requests.post(url, data=payload)
            result = response.json()
            
            if 'id' not in result:
                print(f"❌ 創建容器失敗：{result}")
                return None
            
            creation_id = result['id']
            print(f"✅ 容器創建成功：{creation_id}")
            
            # Step 2: 發布貼文
            publish_url = f"https://graph.threads.net/v1.0/{self.threads_user_id}/threads_publish"
            
            publish_payload = {
                'creation_id': creation_id,
                'access_token': self.threads_access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_payload)
            publish_result = publish_response.json()
            
            if 'id' in publish_result:
                print(f"✅ Threads 發文成功：{text[:50]}...")
                return publish_result['id']
            else:
                print(f"❌ 發布失敗：{publish_result}")
                return None
                
        except Exception as e:
            print(f"❌ Threads 發文失敗：{e}")
            return None
    
    def post_instagram(self, image_url, caption):
        """發布 Instagram 圖片貼文（官方 API）"""
        try:
            # Step 1: 創建容器
            url = f"https://graph.facebook.com/v18.0/{self.ig_user_id}/media"
            
            payload = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.ig_access_token
            }
            
            response = requests.post(url, data=payload)
            result = response.json()
            
            if 'id' not in result:
                print(f"❌ 創建容器失敗：{result}")
                return None
            
            creation_id = result['id']
            print(f"✅ 容器創建成功：{creation_id}")
            
            # Step 2: 發布貼文
            publish_url = f"https://graph.facebook.com/v18.0/{self.ig_user_id}/media_publish"
            
            publish_payload = {
                'creation_id': creation_id,
                'access_token': self.ig_access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_payload)
            publish_result = publish_response.json()
            
            if 'id' in publish_result:
                print(f"✅ Instagram 發文成功：{caption[:50]}...")
                return publish_result['id']
            else:
                print(f"❌ 發布失敗：{publish_result}")
                return None
                
        except Exception as e:
            print(f"❌ Instagram 發文失敗：{e}")
            return None
    
    def get_threads_insights(self, post_id):
        """獲取 Threads 貼文數據"""
        try:
            url = f"https://graph.threads.net/v1.0/{post_id}/insights"
            
            params = {
                'metric': 'views,likes,replies,reposts,quotes',
                'access_token': self.threads_access_token
            }
            
            response = requests.get(url, params=params)
            result = response.json()
            
            print(f"📊 貼文數據：{result}")
            return result
            
        except Exception as e:
            print(f"❌ 獲取數據失敗：{e}")
            return None

if __name__ == "__main__":
    # 測試
    bot = InstagramBotOfficial()
    
    # 測試發 Threads
    test_text = """🔥 測試貼文

這是使用官方 API 的自動化系統測試

#富遊娛樂城 #測試"""
    
    bot.post_threads(test_text)
