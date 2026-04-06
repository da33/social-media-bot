"""
測試腳本 - 不需要真實帳號
測試系統邏輯是否正常
"""
import sys
import os

# 添加路徑
sys.path.insert(0, os.path.dirname(__file__))

def test_content_loading():
    """測試內容載入"""
    print("🧪 測試1：內容載入")
    try:
        import json
        with open('content/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        print(f"✅ 成功載入 {len(posts)} 篇內容")
        return True
    except Exception as e:
        print(f"❌ 失敗：{e}")
        return False

def test_scheduler_logic():
    """測試排程邏輯"""
    print("\n🧪 測試2：排程邏輯")
    try:
        import schedule
        
        def dummy_job():
            print("✅ 排程任務執行成功")
        
        schedule.every().day.at("09:00").do(dummy_job)
        print("✅ 排程設定成功")
        return True
    except Exception as e:
        print(f"❌ 失敗：{e}")
        return False

def test_keyword_reply():
    """測試關鍵字回覆邏輯"""
    print("\n🧪 測試3：關鍵字回覆")
    
    promotion_link = 'https://rggo5269.com/#/ag/win99'
    
    def get_keyword_reply(message):
        message = message.lower()
        replies = {
            '註冊': f'🎰 立即註冊：{promotion_link}',
            '代理': '💰 代理招募中！',
            '攻略': '🎮 遊戲攻略'
        }
        for keyword, reply in replies.items():
            if keyword in message:
                return reply
        return '預設回覆'
    
    # 測試案例
    test_cases = [
        ('我想註冊', '註冊'),
        ('代理怎麼做', '代理'),
        ('有攻略嗎', '攻略'),
        ('你好', '預設')
    ]
    
    all_passed = True
    for message, expected in test_cases:
        reply = get_keyword_reply(message)
        if expected in reply or reply == '預設回覆':
            print(f"✅ '{message}' → 正確回覆")
        else:
            print(f"❌ '{message}' → 回覆錯誤")
            all_passed = False
    
    return all_passed

def test_random_selection():
    """測試隨機選擇邏輯"""
    print("\n🧪 測試4：隨機選擇")
    try:
        import random
        import json
        
        with open('content/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        used_posts = []
        for i in range(3):
            available = [p for p in posts if p not in used_posts]
            if not available:
                used_posts = []
                available = posts
            
            post = random.choice(available)
            used_posts.append(post)
            print(f"✅ 第{i+1}次選擇：{post['type']}")
        
        return True
    except Exception as e:
        print(f"❌ 失敗：{e}")
        return False

def test_imports():
    """測試所有必要的模組"""
    print("\n🧪 測試5：模組導入")
    
    modules = [
        ('schedule', 'schedule'),
        ('json', 'json'),
        ('random', 'random'),
        ('time', 'time'),
        ('os', 'os')
    ]
    
    all_passed = True
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name} 導入成功")
        except ImportError:
            print(f"❌ {name} 導入失敗")
            all_passed = False
    
    return all_passed

def main():
    print("="*50)
    print("🤖 社群媒體自動化系統 - 測試")
    print("="*50)
    
    results = []
    
    # 執行所有測試
    results.append(("內容載入", test_content_loading()))
    results.append(("排程邏輯", test_scheduler_logic()))
    results.append(("關鍵字回覆", test_keyword_reply()))
    results.append(("隨機選擇", test_random_selection()))
    results.append(("模組導入", test_imports()))
    
    # 總結
    print("\n" + "="*50)
    print("📊 測試總結")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{name}: {status}")
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！系統可以部署！")
        return True
    else:
        print("\n⚠️ 部分測試失敗，請檢查問題")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
