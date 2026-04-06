"""手動觸發一次發文測試"""
import os
import sys
import time

# 設定環境變數
os.environ['IG_ACCESS_TOKEN'] = 'EAARZBU1qsymIBRNNUGOdL7F1kAwdlBKQVaNq903cBcMuCJQOyxTaKv8ZCRWUqQ7aGcZAUo2ItZC8ZCFSY3ueZCYbJDeKd7vlHOfDZAs1zXsSkQgHhoiiCGQNB9IKZAXHZCX3mdwGgoGa2ZAHt65WvNmWQP0YAvLX28Rf2rMXVIpFChYaQFnAwZCxx8yqbVzAmmiZB7mV'
os.environ['IG_ACCOUNT_ID'] = '17841401987677377'
os.environ['THREADS_ACCESS_TOKEN'] = 'THAAUyK8zbIj1BUVJtVTF5bFZAtMUxEQVl6c21qc3VqMW45NFZAYM29QRVgxNGhodXNRdWdvX21QS2dUWFV0NWZALRThuamswLUUzV2pGXzlaYUJYMDZA1RFZAYOEtTSnh4MmIzdFExNHEtUkVmQTlyNlZATOVRMUzZAiajk4eklXRkQzeGd4UQZDZD'
os.environ['THREADS_USER_ID'] = '26112997131686434'
os.environ['MINIMAX_API_KEY'] = 'sk-cp-VddIVaDxNHMJ9CnaOZHfmsGuYKFeJkxrpxypFDhbD9NgNNXf8_i23ADxnrbhS0jswc1d7gsSp7j6gMfJaQ3uN-__XyM-fOzadpWQX3GS2Pn9FGYqjJekdSs'

from instagram_client import InstagramPublisher
from bots.instagram_bot_official import InstagramBotOfficial

# 測試內容
test_content = """今天出金了一下

金額不方便說

但流程很快

拿到錢的感覺還不錯

沒有問題"""

test_topic = "出金紀錄"

print("="*50)
print("手動觸發發文測試")
print("="*50)

# 1. Threads 發文
print("\n1. Threads 發文...")
threads_bot = InstagramBotOfficial()
threads_result = threads_bot.post_threads(test_content)
if threads_result:
    print(f"   ✅ Threads 成功！ID: {threads_result}")
else:
    print("   ❌ Threads 失敗")

# 2. IG 發文
print("\n2. IG 發文...")
time.sleep(5)

ig_pub = InstagramPublisher()
ig_result = ig_pub.post_with_ai_image(test_content, topic=test_topic)
if ig_result:
    print(f"   ✅ IG 成功！ID: {ig_result}")
else:
    print("   ❌ IG 失敗")

print("\n" + "="*50)
print("測試完成")
print("="*50)
