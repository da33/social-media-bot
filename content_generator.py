"""
AI 內容生成器
ENI 定制版 - 單一帳號系統
waterboy_rix - 富遊娛樂推廣
"""
import json
import random
import os
from datetime import datetime

import anthropic

class AIContentGenerator:
    def __init__(self):
        self.account_name = "waterboy_rix"
        self.promotion_link = "https://rggo5269.com/#/ag/win99"
        self.customer_service_link = "https://lin.ee/VjQOag7"
        
        # MiniMax Token Plan API
        self.api_key = os.getenv('MINIMAX_API_KEY')
        self.base_url = "https://api.minimaxi.com/anthropic"
        
        if self.api_key:
            self.client = anthropic.Anthropic(
                base_url=self.base_url,
                api_key=self.api_key
            )
        else:
            self.client = None
            print("⚠️ MINIMAX_API_KEY 未設定")
        
        # 內容方向池 - 5大類
        self.content_directions = [
            {
                "id": "出金",
                "name": "出金實錄",
                "description": "強調出金保證，真實記錄",
                "examples": ["出金紀錄", "出金速度", "出金安全性", "出金頻率"]
            },
            {
                "id": "平台",
                "name": "平台觀察",
                "description": "強調穩定安全，專業分析",
                "examples": ["平台穩定", "出金安全性", "平台選擇"]
            },
            {
                "id": "優惠",
                "name": "優惠分享",
                "description": "強調福利活動，真實使用",
                "examples": ["優惠整理", "優惠使用", "優惠評估"]
            },
            {
                "id": "觀念",
                "name": "遊戲觀念",
                "description": "強調心態經驗，負責任娛樂",
                "examples": ["心態分享", "風控觀念", "遊戲選擇"]
            },
            {
                "id": "服務",
                "name": "客戶互動",
                "description": "強調問答互動，新手幫助",
                "examples": ["新人FAQ", "經驗分享", "問答回覆"]
            }
        ]
        
        # 說話風格 - 4種輪換
        self.styles = [
            {
                "name": "直接型",
                "persona": "普通上班族，有話就說",
                "voice": "直接、不囉嗦、有話就說，像跟朋友聊天"
            },
            {
                "name": "專業型", 
                "persona": "低調專業人士，分析事情",
                "voice": "專業、淡定、有深度，像內行人聊天"
            },
            {
                "name": "輕鬆型",
                "persona": "輕鬆生活的人，隨性分享",
                "voice": "輕鬆、生活化、有日常感，像發IG story"
            },
            {
                "name": "故事型",
                "persona": "喜歡說故事的人，有溫度",
                "voice": "溫暖、有畫面、用故事帶出重點"
            }
        ]
        
        # 所有話題的 prompt 模板
        self.topic_prompts = {
            "出金紀錄": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你出金的情況：

要求：
- 3-5句話，100-150字
- 說今天/這次出金的事實
- 不誇張，不承諾「一定」「保證」
- 不催人「快來」「立即」「限時」
- 說「我」的故事，不說「你應該」

範例开头：「今天出金了...」「上次出金...」「我出金通常...」

現在開始用{voice}的風格寫：""",

            "出金速度": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你觀察到的出金速度：

要求：
- 3-5句話，100-150字
- 說你的實際觀察，不是推銷
- 可以說「通常」「大概」「有時候」
- 不要說精確數字如「5分鐘」「10分鐘」
- 不催人，不喊口號

範例开头：「出金速度我觀察是...」「通常出金要...」

現在開始用{voice}的風格寫：""",

            "出金安全性": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你對出金安全的看法：

要求：
- 3-5句話，100-150字
- 說「我重視」「我關心」
- 不說「保證」「一定」「絕對」
- 不催人，不喊口號

範例开头：「出金安全這塊...」「我最在乎的是...」

現在開始用{voice}的風格寫：""",

            "出金頻率": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你通常怎麼出金：

要求：
- 3-5句話，100-150字
- 說「我通常」「我習慣」
- 不是建議別人，是分享自己
- 不說「應該」「最好」

範例开头：「我出金沒有固定時間...」「我習慣...」

現在開始用{voice}的風格寫：""",

            "平台穩定": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你觀察到的平台穩定性：

要求：
- 3-5句話，100-150字
- 說實際感受，不是背書
- 可以提具體觀察（客服、回應速度）
- 不要攻擊其他平台

範例开头：「用了一段時間...」「平台穩定這塊...」

現在開始用{voice}的風格寫：""",

            "出金安全性": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說出金安全的哪個面向：

要求：
- 3-5句話，100-150字
- 說你的考量
- 說「我重視」不是「你應該」

範例开头：「出金安全我最在乎的是...」

現在開始用{voice}的風格寫：""",

            "優惠整理": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要整理你知道的一兩個優惠：

要求：
- 3-5句話，100-150字
- 說「有」「目前知道」
- 說明適用情況，不吹噓
- 不說「快來」「限時」「錯過可惜」

範例开头：「目前知道的優惠...」「優惠這塊...」

現在開始用{voice}的風格寫：""",

            "優惠使用": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你實際用過的優惠：

要求：
- 3-5句話，100-150字
- 說「我用了」「我用過」
- 說實際結果，不誇大
- 不說「保證」「一定」

範例开头：「優惠我實際用過...」「之前用過一個優惠...」

現在開始用{voice}的風格寫：""",

            "優惠評估": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你對優惠的看法：

要求：
- 3-5句話，100-150字
- 說「我覺得」「個人認為」
- 不吹噓，不說「最優惠」「性價比最高」

範例开头：「優惠好不好...」「我對優惠的看法是...」

現在開始用{voice}的風格寫：""",

            "心態分享": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你玩這個的心態：

要求：
- 3-5句話，100-150字
- 說「我」的心態
- 說「娛樂」「休閒」
- 不說「投資」「賺錢」「翻身」

範例开头：「我玩這個的心態是...」「老實說...」

現在開始用{voice}的風格寫：""",

            "風控觀念": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你的風險控制方式：

要求：
- 3-5句話，100-150字
- 說「我」的做法
- 不說「你應該」「一定要」

範例开头：「我自己的做法是...」「風險控制這塊...」

現在開始用{voice}的風格寫：""",

            "遊戲選擇": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說說你平常玩什麼、怎麼選：

要求：
- 3-5句話，100-150字
- 說「我通常」「我喜歡」
- 不說「必中」「高命中率」

範例开头：「遊戲選擇這塊...」「我通常玩...」

現在開始用{voice}的風格寫：""",

            "新人FAQ": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要回答一個新手常見問題：

要求：
- 3-5句話，100-150字
- 說「新手常問...」「通常會問...」
- 回答一個問題，不長篇大論
- 不說「保證」「一定」

範例开头：「新手最常問的是...」「通常被問到...」

現在開始用{voice}的風格寫：""",

            "經驗分享": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要說一段你的經歷：

要求：
- 3-5句話，100-150字
- 說「我曾經」「有一次」
- 用故事帶出重點
- 不要說教

範例开头：「之前有一次...」「我曾經...」

現在開始用{voice}的風格寫：""",

            "問答回覆": """你是一個{style}的富遊用戶。

你的角色：{persona}

現在要假設有人問你問題並回答：

要求：
- 3-5句話，100-150字
- 直接回答，話不多
- 不加「點連結」「快來」
- 自然的對話感

範例开头：「如果有人問我...」「問我的人通常...」

現在開始用{voice}的風格寫："""
        }
        
    def generate_content(self, topic=None, style=None):
        """生成一篇內容"""
        # 選擇話題
        if topic is None:
            all_topics = list(self.topic_prompts.keys())
            topic = random.choice(all_topics)
        
        # 選擇風格
        if style is None:
            style_info = random.choice(self.styles)
        else:
            style_info = next((s for s in self.styles if s["name"] == style), self.styles[0])
        
        # 建立 prompt
        prompt = self.topic_prompts.get(topic, self.topic_prompts["出金紀錄"])
        prompt = prompt.format(
            style=style_info["persona"],
            persona=style_info["persona"],
            voice=style_info["voice"]
        )
        
        # AI 生成
        if self.client:
            try:
                response = self.client.messages.create(
                    model="MiniMax-M2.7",
                    max_tokens=512,
                    system="你是一個真實的富遊娛樂用戶，說話自然，不像業務員。\n\n原則：\n- 只說事實，不說「保證」「一定」「穩贏」\n- 不催人「快來」「現在」「限時」\n- 不喊口號「首存就送」「獎金翻倍」\n- 說「我」的經歷，不說「你應該」\n\n你就是一個普通人在分享，別人看到就看到了。",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                content = ""
                for block in response.content:
                    if block.type == "text":
                        content = block.text
                        break
                
                if content:
                    return {
                        "topic": topic,
                        "style": style_info["name"],
                        "content": content.strip(),
                        "source": "ai"
                    }
            except Exception as e:
                print(f"❌ AI 生成失敗：{e}")
        
        # Fallback
        return {
            "topic": topic,
            "style": style_info["name"],
            "content": self._fallback_content(topic),
            "source": "fallback"
        }
    
    def _fallback_content(self, topic):
        """備用內容"""
        fallbacks = {
            "出金紀錄": "今天出了一筆，流程還算順。有問題可以問我。",
            "出金速度": "出金速度我觀察是這樣的，不快不慢，正常範圍。",
            "出金安全性": "出金安全這塊我最在乎，目前用起來還行。",
            "出金頻率": "出金沒有固定時間，看情況。有問題問我。",
            "平台穩定": "用了一段時間，沒有大問題。起碼我這邊是這樣。",
            "優惠整理": "目前知道有首存優惠，詳情可以問我。",
            "優惠使用": "優惠我用過，用起來還可以，不特別吹噓。",
            "優惠評估": "優惠好不好用過才知道，我用過的還可以。",
            "心態分享": "休閒而已，平常心。贏了開心，輸了也不影響生活。",
            "風控觀念": "我的做法是設定預算，超了就停，很簡單。",
            "遊戲選擇": "我通常玩自己喜歡的，不特別推薦什麼。",
            "新人FAQ": "有問題直接問我，我盡量回答。",
            "經驗分享": "我的經驗是：先了解再說，不要衝動。",
            "問答回覆": "問什麼我就答什麼，直接說。",
        }
        return fallbacks.get(topic, "今天就這樣，沒什麼特別的。")
    
    def generate_daily_content(self, count=3):
        """生成一天要發的內容（count = 發文次數）"""
        posts = []
        
        # 確保每次用不同的話題和風格
        used_topics = []
        used_styles = []
        
        topic_pool = list(self.topic_prompts.keys())
        style_pool = [s["name"] for s in self.styles]
        
        for i in range(count):
            # 選擇還沒用過的話題
            available_topics = [t for t in topic_pool if t not in used_topics]
            if not available_topics:
                available_topics = topic_pool
                used_topics = []
            
            topic = random.choice(available_topics[:5])  # 每次從前5個選
            used_topics.append(topic)
            
            # 選擇還沒用過的風格
            available_styles = [s for s in style_pool if s not in used_styles]
            if not available_styles:
                available_styles = style_pool
                used_styles = []
            
            style = random.choice(available_styles[:3])  # 每次從前3個選
            used_styles.append(style)
            
            post = self.generate_content(topic=topic, style=style)
            post["slot"] = i + 1
            posts.append(post)
        
        return posts

if __name__ == "__main__":
    gen = AIContentGenerator()
    
    print("=== 單一帳號 waterboy_rix ===\n")
    
    print("=== 測試單篇生成 ===")
    post = gen.generate_content()
    print(f"話題：{post['topic']}")
    print(f"風格：{post['style']}")
    print(f"內容：\n{post['content']}\n")
    print(f"來源：{post['source']}")
    
    print("\n=== 測試一天內容（三篇） ===")
    daily = gen.generate_daily_content(3)
    for p in daily:
        print(f"\n【第{p['slot']}篇】{p['topic']} - {p['style']}風格")
        print(p['content'][:100] + '...')
