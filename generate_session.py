#!/usr/bin/env python3
"""
生成 Instagram Session 檔案
在本地電腦運行一次，生成 session.json
"""

from instagrapi import Client
import json

def generate_session():
    print("🔐 Instagram Session 生成器\n")
    
    # 輸入帳號密碼
    username = input("請輸入 Instagram 帳號: ")
    password = input("請輸入密碼: ")
    
    print("\n⏳ 正在登入...")
    
    try:
        # 創建客戶端
        cl = Client()
        
        # 登入
        cl.login(username, password)
        
        print("✅ 登入成功！")
        
        # 獲取 session
        session = cl.get_settings()
        
        # 保存到檔案
        with open('session.json', 'w') as f:
            json.dump(session, f, indent=2)
        
        print("\n✅ Session 已保存到 session.json")
        print("📁 請將此檔案上傳到 Zeabur")
        
    except Exception as e:
        print(f"\n❌ 登入失敗: {e}")
        print("\n可能原因：")
        print("1. 帳號密碼錯誤")
        print("2. 需要兩步驟驗證")
        print("3. Instagram 要求驗證")

if __name__ == "__main__":
    generate_session()
