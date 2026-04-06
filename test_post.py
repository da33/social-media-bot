"""
測試發文腳本 - 立即發一篇到 Threads
"""
import sys
sys.path.append('/app')

from bots.instagram_bot_official import InstagramBotOfficial

# 初始化
bot = InstagramBotOfficial()

# 測試發文
test_post = """🔥 富遊娛樂城自動化系統測試

✅ 系統已成功部署
🤖 24小時自動運營中

立即體驗👉 https://rggo5269.com/#/ag/win99

#富遊娛樂城 #系統測試"""

print("📱 準備發布到 Threads...")
result = bot.post_threads(test_post)

if result:
    print(f"✅ 發文成功！Post ID: {result}")
else:
    print("❌ 發文失敗")
