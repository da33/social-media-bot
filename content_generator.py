"""
AI 內容生成器
使用 MiniMax M2.7 (Token Plan) 生成內容
支援四種人格：A實話實說/B低調專業/C隨性分享/D故事敘事
"""
import json
import random
import os
from datetime import datetime

# MiniMax Token Plan API (Anthropic compatible)
import anthropic

class AIContentGenerator:
    def __init__(self, personas_dir="personas"):
        self.personas_dir = personas_dir
        self.personas = self._load_personas()
        self.promotion_link = "https://rggo5269.com/#/ag/win99"
        
        # MiniMax Token Plan API
        self.api_key = os.getenv('MINIMAX_API_KEY')
        self.base_url = "https://api.minimaxi.com/anthropic"
        
        # 初始化 Anthropic client
        if self.api_key:
            self.client = anthropic.Anthropic(
                base_url=self.base_url,
                api_key=self.api_key
            )
        else:
            self.client = None
            print("⚠️ MINIMAX_API_KEY 未設定，使用模板生成")
        
        # 話題池
        self.topics = [
            "出金實錄", "出金速度", "出金頻率",
            "風險提醒", "心態建立", "風控觀念",
            "平台安全", "平台穩定",
            "優惠分享", "新人解惑",
            "客戶故事", "日常隨筆"
        ]
        
    def _load_personas(self):
        """載入人格設定"""
        personas = {}
        for file in os.listdir(self.personas_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.personas_dir, file), 'r', encoding='utf-8') as f:
                    persona = json.load(f)
                    personas[persona['id']] = persona
        return personas
    
    def _get_system_prompt(self, persona):
        """取得該人格的 system prompt"""
        prompts = {
            "A": f"""你是富遊娛樂的代理，你說話直接、不唬爛。

你的風格：
- 直接、不修飾、有話直說
- 句短有力，不啰嗦
- 不承諾勝率，但強調出金穩定
- 強調心態調整和風險控制

你會出金給客戶看，說實話，不騙人。

每次發文：
1. 先說重點（出金/優惠/觀念）
2. 給出具體數字或例子
3. 呼籲行動但不强迫
4. 結尾加連結：{self.promotion_link}

內容要像真人在發文，不要像機器人。""",

            "B": f"""你是富遊娛樂的代理，你說話低調但專業。

你的風格：
- 專業、克制、有深度
- 不張揚，一出聲就是乾貨
- 不說廢話
- 分析導向，用數據說話

你的內容是有深度的分析，不是情緒性的宣言。

每次發文：
1. 說重點
2. 給出分析或對比
3. 結論先行
4. 結尾加連結：{self.promotion_link}

內容要有質感，像專業人士在說話。""",

            "C": f"""你是富遊娛樂的代理，你說話輕鬆隨性。

你的風格：
- 輕鬆、隨性、生活化
- 像在跟朋友聊天
- emoji 使用多
- 句子有長有短

今天出金了就說出金，有優惠就說優惠，沒事的時候就分享一些輕鬆的遊戲觀念。

每次發文：
1. 先描述當下情境
2. 分享相關內容
3. 輕鬆呼籲
4. 結尾加連結：{self.promotion_link}

內容要像日常生活記錄，不要像行銷文案。""",

            "D": f"""你是富遊娛樂的代理，你說話有溫度。

你的風格：
- 溫暖、有畫面、敘事感強
- 喜歡用故事帶內容
- 句子中等偏長
- 有情感共鳴

你會說「今天遇到一個客人」「曾經有個人問我」「說個故事給你聽」來開始內容。

每次發文：
1. 用故事或情境開頭
2. 帶出核心內容
3. 情感共鳴
4. 結尾加連結：{self.promotion_link}

內容要有溫度，像在跟人分享經驗。"""
        }
        return prompts.get(persona['id'], prompts["A"])
    
    def _get_topic_prompt(self, topic, persona):
        """根據話題生成 user prompt"""
        topic_prompts = {
            "出金實錄": f"""生成一篇「出金實錄」貼文。

要求：
- 說今天出金了，給出具體金額和耗時
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 用「出金」「領到」「到帳」等詞
- 最後附上連結：{self.promotion_link}""",

            "出金速度": f"""生成一篇關於「出金速度」的貼文。

要求：
- 分享出金等待時間的經驗
- 給出具體數字（分鐘/小時）
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "出金頻率": f"""生成一篇關於「出金頻率」的貼文。

要求：
- 分享多久出金一次的習慣
- 建議及時收割，不要一直放著
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "風險提醒": f"""生成一篇「風險提醒」貼文。

要求：
- 強調不要借錢、設置止損、控制預算
- 不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 用「休閒」「娛樂」「控制風險」等詞
- 最後附上連結：{self.promotion_link}""",

            "心態建立": f"""生成一篇「心態建立」貼文。

要求：
- 分享正確的遊戲心態
- 不要想著上岸、翻本、一次贏大的
- 當休閒，贏了開心輸了不影響
- 不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "風控觀念": f"""生成一篇「風控觀念」貼文。

要求：
- 分享風險控制的觀念
- 不要 ALL IN、不要借 Q、不要影響生活
- 不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "平台安全": f"""生成一篇「平台安全」貼文。

要求：
- 分享選擇平台時注意的事項
- 強調出金穩定、客服靠譜、系統正常
- 不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "平台穩定": f"""生成一篇「平台穩定」貼文。

要求：
- 分享平台使用的穩定感受
- 提到系統維護、客服回應等
- 不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "優惠分享": f"""生成一篇「優惠分享」貼文。

要求：
- 分享最新優惠活動
- 說明領取方式
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "新人解惑": f"""生成一篇「新人解惑」貼文。

要求：
- 回答新手常見問題
- 如：會不會被騙、要多少本金、能不能贏錢
- 誠實回答，不承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "客戶故事": f"""生成一篇「客戶故事」貼文。

要求：
- 用故事方式分享
- 可以是客戶的經歷或自己的經歷
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}""",

            "日常隨筆": f"""生成一篇「日常隨筆」貼文。

要求：
- 輕鬆分享日常生活
- 自然帶入遊戲/平台話題
- 不要承諾勝率
- 語氣符合人格：{persona['name']} - {persona['description']}
- 150字以內
- 不要提及「賭博」「贏錢」「賺錢」
- 最後附上連結：{self.promotion_link}"""
        }
        return topic_prompts.get(topic, topic_prompts["日常隨筆"])
    
    def generate_with_ai(self, persona_id, topic):
        """使用 MiniMax M2.7 AI 生成內容"""
        if not self.client:
            return None
        
        persona = self.personas.get(persona_id)
        if not persona:
            return None
        
        try:
            system = self._get_system_prompt(persona)
            user = self._get_topic_prompt(topic, persona)
            
            response = self.client.messages.create(
                model="MiniMax-M2.7",
                max_tokens=1024,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": user
                    }
                ]
            )
            
            # 取得文字回覆
            text = ""
            for block in response.content:
                if block.type == "text":
                    text = block.text
                    break
            
            if text:
                return text.strip()
            return None
            
        except Exception as e:
            print(f"❌ AI 生成失敗：{e}")
            return None
    
    def generate_with_ai_thinking(self, persona_id, topic):
        """使用 MiniMax M2.7 AI 生成內容（帶思考過程）"""
        if not self.client:
            return None
        
        persona = self.personas.get(persona_id)
        if not persona:
            return None
        
        try:
            system = self._get_system_prompt(persona)
            user = self._get_topic_prompt(topic, persona)
            
            response = self.client.messages.create(
                model="MiniMax-M2.7",
                max_tokens=1024,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 3000
                },
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": user
                    }
                ]
            )
            
            # 取得文字回覆
            text = ""
            for block in response.content:
                if block.type == "text":
                    text = block.text
                    break
            
            if text:
                return text.strip()
            return None
            
        except Exception as e:
            print(f"❌ AI 生成失敗：{e}")
            return None
    
    def generate_post(self, persona_id=None, force_topic=None):
        """生成一篇內容（AI 優先，失敗用模板）"""
        # 選擇人格
        if persona_id:
            persona = self.personas.get(persona_id)
        else:
            persona = random.choice(list(self.personas.values()))
        
        # 選擇話題
        if force_topic:
            topic = force_topic
        else:
            topic = random.choice(self.topics)
        
        # 嘗試 AI 生成
        ai_content = self.generate_with_ai(persona['id'], topic)
        
        if ai_content:
            return {
                "persona_id": persona['id'],
                "persona_name": persona['name'],
                "topic": topic,
                "content": ai_content,
                "generated_at": datetime.now().isoformat(),
                "link": self.promotion_link,
                "source": "ai"
            }
        
        # AI 失敗，用模板
        return {
            "persona_id": persona['id'],
            "persona_name": persona['name'],
            "topic": topic,
            "content": self._get_fallback_content(topic, persona),
            "generated_at": datetime.now().isoformat(),
            "link": self.promotion_link,
            "source": "fallback"
        }
    
    def _get_fallback_content(self, topic, persona):
        """模板備用內容"""
        fallbacks = {
            "出金實錄": f"""不多說，看圖

今天出金了

金額：{random.choice(['3200', '5800', '12000', '750', '4500'])}
耗時：{random.choice(['15分鐘', '20分鐘', '5分鐘', '30分鐘', '10分鐘'])}

錢已到帳，沒有問題

要問的可以問
連結：
{self.promotion_link}""",

            "出金速度": f"""很多人問出金速度

我直接說

我出金過{random.randint(5, 20)}次

最快{random.choice(['5分鐘', '8分鐘', '10分鐘'])}
最慢{random.choice(['35分鐘', '40分鐘', '45分鐘'])}

平均大概{random.choice(['15分鐘', '20分鐘', '25分鐘'])}

這個速度我認為可以

你要自己判斷

{self.promotion_link}""",

            "出金頻率": f"""我出金大概是{random.choice(['每週', '每兩週', '每個月'])}

不一定

但有一點我堅持

贏了就要出

不要一直放在裡面滾

及時收割才是真的

{self.promotion_link}""",

            "風險提醒": f"""我說實話

我不會跟你說一定贏

但我可以告訴你

怎麼玩不會傷

① 拿的出來的錢才進
② 設置止損點
③ 不要借錢來玩

這三點做不到

我建議你不要開始

{self.promotion_link}""",

            "心態建立": f"""玩這個最重要的

我認為是心態

不要想著上岸

不要想著翻本

不要想著一次贏大的

當休閒

贏了開心

輸了也不影響生活

這才是正確的心態

{self.promotion_link}""",

            "風控觀念": f"""說一個觀念

不要 ALL IN

不要借 Q

不要影響生活

在這三個前提之下

你來玩我不反對

但如果你抱著借錢來翻本的心態

我建議你不要開始

{self.promotion_link}""",

            "平台安全": f"""我選擇富遊的原因

第一，出金正常

第二，時間穩定

第三，客服有人在

用了{random.randint(6, 18)}個月

沒有遇到那種「審核中」然後就沒有然後的情況

我可以接受

{self.promotion_link}""",

            "平台穩定": f"""富遊用了一段時間

說一下感受

優點：
✅ 出金正常
✅ 優惠真實
✅ 客服有回應

缺點：
❌ 偶爾系統維護

整體我給{random.choice(['7.5', '8', '8.5'])}分

{self.promotion_link}""",

            "優惠分享": f"""優惠資訊

✅ 新會員：註冊送體驗金
✅ 首存：{random.choice(['1000送500', '1000送1000', '500送250'])}
✅ 復利：{random.choice(['每週抽紅包', '每月加贈', 'VIP專屬'])}

看清楚條件再說

{self.promotion_link}""",

            "新人解惑": f"""新手常見問題

問：會不會被騙？
答：我自己出金{random.randint(10, 50)}次了，沒有問題

問：要多少本金？
答：{random.choice(['看你自己，我建議從小額開始', f'最低{random.choice(["500", "1000", "2000"])}', '不要借錢來玩'])}

問：能不能贏錢？
答：沒有人能保証

問了再說

{self.promotion_link}""",

            "客戶故事": f"""說一個客戶的故事

他剛開始問我出金要多久

我說大概10-20分鐘

他說：真的假的

然後他真的出金了

{random.choice(['15分鐘', '20分鐘', '12分鐘'])}後

錢到了

那個客戶現在每週都出金

不貪心

我覺得這個心態很好

{self.promotion_link}""",

            "日常隨筆": f"""今天{random.choice(['天氣不錯', '下雨天', '加班到很晚', '難得的休假'])}

有客戶問我問題

我發現很多人對這種平台有偏見

我懂，網路上被騙的太多了

但選擇比努力重要

富遊我用了{random.randint(6, 18)}個月，目前沒問題

有問題可以問我

{self.promotion_link}"""
        }
        return fallbacks.get(topic, fallbacks["日常隨筆"])
    
    def generate_daily_posts(self):
        """生成每天三篇（09:00/14:00/21:00）"""
        posts = []
        times = ["09:00", "14:00", "21:00"]
        
        for i, time_slot in enumerate(times):
            # 輪換人格
            persona_ids = list(self.personas.keys())
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
    # 測試
    gen = AIContentGenerator()
    
    print("=== 測試 AI 內容生成 ===")
    print(f"可用人格：{list(gen.personas.keys())}")
    print(f"MiniMax 客戶端：{'已連接' if gen.client else '未連接'}")
    print()
    
    print("=== 測試單篇生成 ===")
    post = gen.generate_post()
    print(f"人格：{post['persona_name']}")
    print(f"話題：{post['topic']}")
    print(f"來源：{post['source']}")
    print(f"內容：\n{post['content']}\n")
    
    print("\n=== 測試每日三篇 ===")
    daily = gen.generate_daily_posts()
    for p in daily:
        print(f"\n[{p['scheduled_time']}] {p['persona_name']} - {p['topic']} ({p['source']})")
        print(p['content'][:100] + "...")
