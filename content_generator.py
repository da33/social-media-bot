"""
內容生成器
支援四種人格：A實話實說/B低調專業/C隨性分享/D故事敘事
自動旋轉話題，避免重複
"""
import json
import random
import os
from datetime import datetime

class ContentGenerator:
    def __init__(self, personas_dir="personas"):
        self.personas_dir = personas_dir
        self.personas = self._load_personas()
        self.promotion_link = "https://rggo5269.com/#/ag/win99"
        
        # 話題池（每種人格多個話題輪換）
        self.topics = {
            "出金實錄": self._出金實錄_content,
            "出金速度": self._出金速度_content,
            "出金頻率": self._出金頻率_content,
            "風險提醒": self._風險提醒_content,
            "心態建立": self._心態建立_content,
            "平台安全": self._平台安全_content,
            "優惠分享": self._優惠分享_content,
            "新人解惑": self._新人解惑_content,
            "客戶故事": self._客戶故事_content,
            "日常隨筆": self._日常隨筆_content,
            "風控觀念": self._風控觀念_content,
            "平台穩定": self._平台穩定_content,
        }
        
    def _load_personas(self):
        """載入人格設定"""
        personas = {}
        for file in os.listdir(self.personas_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.personas_dir, file), 'r', encoding='utf-8') as f:
                    persona = json.load(f)
                    personas[persona['id']] = persona
        return personas
    
    def _出金實錄_content(self, persona):
        """出金實錄話題"""
        amounts = ["3200", "5800", "12000", "750", "4500", "8900", "2300"]
        times = ["8分鐘", "15分鐘", "5分鐘", "22分鐘", "12分鐘", "30分鐘", "10分鐘"]
        
        content = f"""
{persona['catchphrase']}

今天出金了

金額：{random.choice(amounts)}
耗時：{random.choice(times)}

錢已到帳，沒有問題

要問的可以問
連結：
{self.promotion_link}
"""
        return content.strip()
    
    def _出金速度_content(self, persona):
        """出金速度話題"""
        content = f"""
很多人問出金速度

我直接說

我出金過{random.randint(5, 20)}次

最快{random.choice(['5分鐘', '8分鐘', '10分鐘'])}
最慢{random.choice(['35分鐘', '40分鐘', '45分鐘'])}

平均下來大概是{random.choice(['15分鐘', '20分鐘', '25分鐘'])}

這個速度我認為可以

你要自己判斷

{self.promotion_link}
"""
        return content.strip()
    
    def _出金頻率_content(self, persona):
        """出金頻率話題"""
        content = f"""
我出金大概是{random.choice(['每週', '每兩週', '每個月', '看情況'])}

不一定

但有一點我堅持

贏了就要出

不要一直放在裡面滾

滾到最後都是數字而已

及時收割才是真的

{self.promotion_link}
"""
        return content.strip()
    
    def _風險提醒_content(self, persona):
        """風險提醒話題"""
        content = f"""
我說實話

我不會跟你說一定贏

這個沒有人能保証

但我可以告訴你

怎麼玩不會傷

① 拿的出來的錢才進
② 設定止損點
③ 不要借錢來玩

這三點做不到

我建議你不要開始

{self.promotion_link}
"""
        return content.strip()
    
    def _心態建立_content(self, persona):
        """心態建立話題"""
        content = f"""
玩這個最重要的

我認為是心態

不要想著上岸

不要想著翻本

不要想著一次贏大的

當休閒

贏了開心

輸了也不影響生活

這才是正確的心態

我的看法

你有你的判斷

{self.promotion_link}
"""
        return content.strip()
    
    def _平台安全_content(self, persona):
        """平台安全話題"""
        content = f"""
我選擇富遊的原因

第一，出金正常

第二，時間穩定

第三，客服有人在

用了{random.randint(6, 18)}個月

沒有遇到那種「帳號異常」

或者「審核中」然後就沒有然後的情況

我可以接受

推薦連結：
{self.promotion_link}
"""
        return content.strip()
    
    def _優惠分享_content(self, persona):
        """優惠分享話題"""
        content = f"""
優惠資訊

✅ 新會員：註冊送體驗金
✅ 首存：{random.choice(['1000送500', '1000送1000', '500送250'])}
✅ 復利：{random.choice(['每週抽紅包', '每月加贈', 'VIP專屬'])}

看清楚條件再說

有問題問我

{self.promotion_link}
"""
        return content.strip()
    
    def _新人解惑_content(self, persona):
        """新人解惑話題"""
        本金答案 = random.choice([
            '看你自己，我建議從小額開始',
            f'最低{random.choice(["500", "1000", "2000"])}',
            '不要借錢來玩'
        ])
        content = f"""
新手常見問題

問：會不會被騙？
答：我自己出金{random.randint(10, 50)}次了，沒有問題

問：要多少本金？
答：{本金答案}

問：能不能贏錢？
答：沒有人能保証，但我身邊有人贏過{random.choice(['幾千', '上萬', '幾萬'])}

問了再說

{self.promotion_link}
"""
        return content.strip()
    
    def _客戶故事_content(self, persona):
        """客戶故事話題"""
        stories = [
            f"""
說一個客戶的故事

他剛開始問我

出金要多久

我說大概10-20分鐘

他說：真的假的

然後他真的出金了

{random.choice(['15分鐘', '20分鐘', '12分鐘'])}後

他跟我說：到了

那個客戶現在每週都出金

不貪心

我覺得這個心態很好
""",
            f"""
曾經有個人問我

是不是保證能贏

我說不是

他說那你推個屁

我說

我不保証你贏

但我能保証

你贏了可以正常拿到錢

這個我做不到就不用做了

後來他想了幾天

還是來了

現在每個月穩定出金

這個是真的
""",
            f"""
今天遇到一個客人

一來就問我

你們平台會不會出不了金

我說你先出去金一次就知道了

他打了{random.choice(['3000', '5000', '8000'])}进帐

贏了{random.choice(['1200', '2500', '4000'])}

申請出金

{random.choice(['18分鐘', '25分鐘', '15分鐘'])}

錢到了

他說：喔還真的可以

我說不然勒

{self.promotion_link}
"""
        ]
        return random.choice(stories)
    
    def _日常隨筆_content(self, persona):
        """日常隨筆話題"""
        content = f"""
今天{random.choice(['天氣不錯', '下雨天', '加班到很晚', '難得的休假', '睡到自然醒'])}

上來說幾句

有客戶問我問題

我發現很多人

對這種平台有偏見

我懂

網路上被騙的太多了

但選擇比努力重要

選對平台可以省很多麻煩

富遊我用了{random.randint(6, 18)}個月

目前為止沒問題

有問題可以問我

{self.promotion_link}
"""
        return content.strip()
    
    def _風控觀念_content(self, persona):
        """風控觀念話題"""
        content = f"""
說一個觀念

不要 ALL IN

不要借 Q

不要影響生活

在這三個前提之下

你來玩我不反對

但如果你抱著借錢來翻本的心態

我建議你不要開始

我不喜歡那種

贏了說我神

輸了說我騙人的客戶

找我就是圖一個安心

{self.promotion_link}
"""
        return content.strip()
    
    def _平台穩定_content(self, persona):
        """平台穩定話題"""
        content = f"""
富遊用了一段時間

說一下感受

優點：
✅ 出金正常
✅ 優惠真實
✅ 客服有回應

缺點：
❌ 偶爾系統維護（大概一個月一次）
❌ 有些遊戲高峰期會卡

整體我給{random.choice(['7.5', '8', '8.5'])}分

扣的分数是因為我不是那種會推薦爛東西的人

{self.promotion_link}
"""
        return content.strip()
    
    def generate_post(self, persona_id=None, force_topic=None):
        """
        生成一篇內容
        persona_id: 指定人格，None則隨機
        force_topic: 強制指定話題，None則隨機
        """
        # 選擇人格
        if persona_id:
            persona = self.personas.get(persona_id)
        else:
            persona = random.choice(list(self.personas.values()))
        
        # 選擇話題
        if force_topic:
            topic_func = self.topics.get(force_topic)
        else:
            topic_func = random.choice(list(self.topics.values()))
        
        # 生成內容
        content = topic_func(persona)
        
        return {
            "persona_id": persona['id'],
            "persona_name": persona['name'],
            "topic": topic_func.__name__.replace('_', ''),
            "content": content,
            "generated_at": datetime.now().isoformat(),
            "link": self.promotion_link
        }
    
    def generate_daily_posts(self):
        """生成每天三篇（09:00/14:00/21:00）"""
        posts = []
        times = ["09:00", "14:00", "21:00"]
        
        for i, time_slot in enumerate(times):
            # 輪換人格，避免連續同一個
            persona_ids = list(self.personas.keys())
            # A->B->C->D 輪換，或者隨機但避免重複
            if i == 0:
                persona_id = persona_ids[datetime.now().weekday() % 4]
            else:
                remaining = [p for p in persona_ids if p != posts[-1]['persona_id']] if posts else persona_ids
                persona_id = random.choice(remaining)
            
            post = self.generate_post(persona_id)
            post['scheduled_time'] = times[i]
            posts.append(post)
        
        return posts

if __name__ == "__main__":
    gen = ContentGenerator()
    
    print("=== 測試單篇生成 ===")
    post = gen.generate_post()
    print(f"人格：{post['persona_name']}")
    print(f"話題：{post['topic']}")
    print(f"內容：\n{post['content']}\n")
    
    print("\n=== 測試每日三篇 ===")
    daily = gen.generate_daily_posts()
    for p in daily:
        print(f"\n[{p['scheduled_time']}] {p['persona_name']} - {p['topic']}")
        print(p['content'][:100] + "...")
