"""
MiniMax Image-01 圖片生成器
上傳到 Cloudinary 提供給 Instagram
"""
import os
import requests
import time
import hashlib
import base64
import random
from datetime import datetime

class ImageGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('MINIMAX_API_KEY')
        self.base_url = "https://api.minimaxi.com/v1"
        
        # Cloudinary 設定
        self.cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'dvtoqjedb')
        self.cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY', '132394465451299')
        self.cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET', 'bOieo35VxsC4XdKZoBB10pngmK0')
        
        # 圖片 prompt 模板（不同風格）
        self.prompts = {
            "casino": "A luxurious casino slot machine theme, golden coins, soft warm lighting, elegant atmosphere, digital art style, 16:9 aspect ratio",
            "gaming": "A modern online gaming platform interface, colorful game icons, neon lights, gaming setup, digital art, 16:9 aspect ratio",
            "lifestyle": "A person relaxing at home, enjoying online entertainment, cozy atmosphere, warm lighting, digital art style, 16:9 aspect ratio",
            "abstract": "Abstract golden patterns, luxurious casino elements, elegant geometric design, digital art, 16:9 aspect ratio",
            "minimal": "Minimalist design with gold accents, simple casino theme elements, modern aesthetic, digital art, 16:9 aspect ratio",
        }
    
    def generate_image(self, prompt_key=None, custom_prompt=None):
        """生成圖片並返回 URL"""
        if custom_prompt:
            prompt = custom_prompt
        elif prompt_key and prompt_key in self.prompts:
            prompt = self.prompts[prompt_key]
        else:
            prompt = random.choice(list(self.prompts.values()))
        
        try:
            url = f"{self.base_url}/image_generation"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "image-01",
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "num_images": 1
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            result = response.json()
            
            if result.get('base_resp', {}).get('status_code') == 0:
                image_url = result.get('data', {}).get('image_urls', [None])[0]
                if image_url:
                    print(f"✅ 圖片生成成功：{image_url[:80]}...")
                    return image_url
                else:
                    print(f"❌ 圖片 URL 為空：{result}")
                    return None
            else:
                print(f"❌ 圖片生成失敗：{result}")
                return None
                
        except Exception as e:
            print(f"❌ 圖片生成錯誤：{e}")
            return None
    
    def download_image(self, url, save_path=None):
        """下載圖片到本地"""
        if not save_path:
            # 用 hash 生成檔名
            hash_name = hashlib.md5(url.encode()).hexdigest()[:12]
            save_path = f"generated_image_{hash_name}.jpg"
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 圖片下載成功：{save_path}")
                return save_path
            else:
                print(f"❌ 下載失敗，狀態碼：{response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 下載錯誤：{e}")
            return None
    
    def upload_to_cloudinary(self, local_path):
        """上傳本地圖片到 Cloudinary，返回公開 URL"""
        try:
            url = f"https://api.cloudinary.com/v1_1/{self.cloud_name}/image/upload"
            
            timestamp = str(int(time.time()))
            params_to_sign = f"timestamp={timestamp}"
            signature = hashlib.sha1((params_to_sign + self.cloudinary_api_secret).encode()).hexdigest()
            
            with open(local_path, 'rb') as f:
                img_data = f.read()
            
            payload = {
                'file': f'data:image/jpeg;base64,{base64.b64encode(img_data).decode()}',
                'api_key': self.cloudinary_api_key,
                'timestamp': timestamp,
                'signature': signature,
            }
            
            response = requests.post(url, data=payload)
            result = response.json()
            
            if result.get('secure_url'):
                print(f"✅ Cloudinary 上傳成功：{result['secure_url'][:80]}...")
                return result['secure_url']
            else:
                print(f"❌ Cloudinary 上傳失敗：{result}")
                return None
                
        except Exception as e:
            print(f"❌ Cloudinary 上傳錯誤：{e}")
            return None

    def generate_and_download(self, prompt_key=None, custom_prompt=None):
        """生成並下載圖片"""
        url = self.generate_image(prompt_key, custom_prompt)
        if url:
            return self.download_image(url)
        return None
    
    def generate_and_upload(self, prompt_key=None, custom_prompt=None):
        """生成圖片並上傳到 Cloudinary（給 Instagram 用）"""
        minimax_url = self.generate_image(prompt_key, custom_prompt)
        if not minimax_url:
            return None
        
        local_path = self.download_image(minimax_url)
        if not local_path:
            return None
        
        cloudinary_url = self.upload_to_cloudinary(local_path)
        
        # 清理本地檔案
        try:
            os.remove(local_path)
        except:
            pass
        
        return cloudinary_url

if __name__ == "__main__":
    gen = ImageGenerator()
    
    print("測試圖片生成...")
    path = gen.generate_and_download("casino")
    print(f"\n生成的圖片路徑：{path}")
