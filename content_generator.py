"""
AI 內容生成器
使用 MiniMax M2.7 (Token Plan) 生成內容
ENI 定制版 - 像真人一樣說話，不推銷
"""
import json
import random
import os
from datetime import datetime

import anthropic

class AIContentGenerator:
    def __init__(self, personas_dir="personas"):
        self.personas_dir = personas_dir
        self.personas = self._load_personas()
        self.promotion_link = "https://rggo5269.com/#/ag/win99"
        self.customer_service_link = "https://l.threads.com/?u=https%3A%2F%2Flin.ee%2FVjQOag7%3Futm_source%3Dthreads%26utm_medium%3Dsocial%26utm_content%3Dlink_in_bio"
        
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
            print("⚠️ MINIMAX_API_KEY 未設定，使用模板生成")
        
        # 話題池
        self.topics = [
            "出金紀錄", "出金速度", "出金頻率",
            "風險提醒", "心態分享", "風控觀念",
            "平台穩定", "平台選擇",
            "優惠使用", "優惠真相",
            "新人問題", "客戶疑問",
            "客戶故事", "日常分享"
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
            "A": f"""你是一個普通人在說話，不是業務員。

你說話的原則：
- 想到什麼說什麼，不預設你在「推廣」
- 不說「保證」「一定」「穩贏」「必勝」
- 不催人：「快來」「現在」「立即」「限時」
- 不喊口號：「首存就送」「獎金翻倍」
- 別人問你才回答，不主動拉人

你只是一個用了一段時間的人，覺得還不錯，純分享。

說話風格：直接、不啰嗦、有話就說
不要像在寫文案
要像在跟朋友聊天""",

            "B": f"""你是一個低調的人在說話，不張揚。

你的原則：
- 說重點，不說廢話
- 不推銷，不催人
- 不說「點這裡」「快來」「立即」
- 分析事情，不推廣產品

你分享的是「經驗」和「觀察」，不是「推文」。

說話風格：專業、淡定、有深度
要像內行人在聊，不是業務員在喊""",

            "C": f"""你是一個輕鬆的人在說話，很隨性。

你的原則：
- 像平常發限時動態一样隨意
- 今天想到什麼就說什麼
- 不會特地「推廣」什麼
- 別人剛好看到就看到了

你只是在記錄生活，剛好跟這個平台有関係。

說話風格：輕鬆、生活化、有日常感
要像在發IG story，不是在打廣告""",

            "D": f"""你是一個有溫度的人在說話，喜歡講故事。

你的原則：
- 用故事带出內容，不直接說產品好
- 說自己的經歷，不說「你應該」
- 不承諾結果，不催人行動
- 讓别人自己判斷

你只是在說「我遇到過一件事」，而不是「我要推薦你」。

說話風格：溫暖、故事感、有畫面
要像在寫散文，不是在寫業配"""
        }
        return prompts.get(persona['id'], prompts["A"])
    
    def _get_topic_prompt(self, topic, persona):
        """根據話題生成 user prompt"""
        topic_prompts = {
            "出金紀錄": f"""隨便說說今天出金的情況。

的重點：
- 今天出金了，說一下事實（金額、時間）
- 順帶提一下，沒有特別意思
- 想到什麼說什麼

不要：
- 不要加「快來」「立即」「限時」

大約100字，像在跟朋友說：「喔對了，今天出了一筆」""",

            "出金速度": f"""有人問你出金速度，你來說說。

的重點：
- 說你實際觀察到的
- 不用數字說大話
- 說你的實際感受

不要：
- 不要說「5分鐘到帳」「最快」這種精確數字
- 不要拿這個當賣點

大約100字，像在回答問題不是在打廣告""",

            "出金頻率": f"""說一下你通常怎麼出金。

的重點：
- 分享你的習慣
- 為什麼這樣出金
- 純個人經驗

不要：
- 不要教人「應該」怎麼出金
- 不要說「這樣最划算」

大約100字，像在聊天不是在給建議""",

            "風險提醒": f"""說一個你認為玩這個要注意的事。

的重點：
- 說你自己的觀察或經歷
- 不是在警告別人
- 說「我曾經...」或「我身邊有人...」

不要：
- 不要像在說教
- 不要列點123

大約100字，像在跟朋友分享不是在當老師""",

            "心態分享": f"""說說你對這個東西的看法。

的重點：
- 你抱著什麼心態在玩
- 這個心態讓你怎麼樣
- 純粹分享你的想法

不要：
- 不要說「你應該怎樣」
- 不要說「這樣才能贏」

大約100字，像在寫日記不是在寫教學""",

            "風控觀念": f"""說一個你認為重要的觀念。

的重點：
- 不用強迫推銷
- 只是覺得這個觀念重要
- 說「我選擇...」不是「你應該...」

不要：
- 不要說「一定要」「必須」

大約100字，像在討論不是在規定""",

            "平台穩定": f"""說說你觀察到的平台情況。

的重點：
- 你用起來的實際感受
- 有沒有什麼問題
- 純描述，不是在幫平台背書

不要：
- 不要拿這個當號召
- 不要說「選擇我們」

大約100字，像在跟人討論不是在做比較""",

            "平台選擇": f"""說說當初為什麼用這個平台。

的重點：
- 你當初在考虑什麼
- 後來為什麼決定用
- 純個人經驗

不要：
- 不要說「推薦給你」
- 不要說「你應該用」

大約100字，像在說故事不是在拉客""",

            "優惠使用": f"""說一個你用過的優惠。

的重點：
- 說你實際使用的經過
- 有沒有遇到問題
- 純分享經驗

不要：
- 不要說「現在還有」「快來拿」
- 不要拿這個當號召

大約100字，像在聊天不是在發傳單""",

            "優惠真相": f"""說說你對這些優惠的真實看法。

的重點：
- 你覺得優惠好不好
- 你會怎麼用
- 說實話，不吹嘘

不要：
- 不要說「CP值最高」「最優惠」

大約100字，像在給建議不是在推銷""",

            "新人問題": f"""如果新人問你問題，你會怎麼回答。

的重點：
- 說你通常怎麼回
- 你的標準答案
- 不是在寫FAQ

不要：
- 不要列出1234的重點
- 不要像在寫教程

大約100字，像在聊天不是在做簡報""",

            "客戶疑問": f"""有人問你問題，你來回答。

的重點：
- 針對一個問題回答
- 說你真實的想法
- 不用特地做內容

不要：
- 不要順便推銷
- 不要加連結

大約100字，像在回答私訊不是在寫推文""",

            "客戶故事": f"""說一個你遇到的故事。

的重點：
- 用故事帶出內容
- 說別人的經歷
- 不說「你應該」

不要：
- 不要說「這個故事告訴我們」
- 不要做道德總結

大約150字，像在說故事不是在講道""",

            "日常分享": f"""今天隨便說點什麼。

的重點：
- 想到什麼說什麼
- 可以帶一點這個平台
- 可以完全不帶
- 純粹日常

不要：
- 不要特地想標題
- 不要想結構

大約100字，像在發呆時打的文字""",
        }
        return topic_prompts.get(topic, topic_prompts["日常分享"])
    
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
        """生成一篇內容"""
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
        """模板備用內容（更自然的版本）"""
        fallbacks = {
            "出金紀錄": f"""今天出了一筆，具體金額就不說了。流程走完大概等了一下下，不算久。就這樣。""",

            "出金速度": f"""有人問我出金要多久，我說不一定，有時候快有時候慢，看情況。我自己是不會特別等就是了。""",

            "出金頻率": f"""我出金沒有固定時間，看心情。看帳面數字差不多了就出，大概就這樣。""",

            "風險提醒": f"""我只能說，進去的錢不要影響生活。其他的你自己判斷。""",

            "心態分享": f"""玩這個最重要的，我覺得是不要想太多。平常心，贏了開心输了也不影響情緒就好了。""",

            "風控觀念": f"""我自己的做法是，先想好最多能接受虧多少。超過了就不玩了，很簡單。""",

            "平台穩定": f"""目前用起來還行，沒有什麼大問題。至少我這邊是這樣。""",

            "平台選擇": f"""當初會用這個，純粹是覺得適合。符不符合你，我不確定。""",

            "優惠使用": f"""優惠的話，用了幾個，整體說，常用的就那幾個，其他的沒特別感覺。""",

            "優惠真相": f"""優惠這種東西，我自己是覺得，用得到就用，用不到就算了。不要為了用而用。""",

            "新人問題": f"""新手常問的問題，我都是直接說實話。能接受就來，不能就算了。""",

            "客戶疑問": f"""被問過很多奇奇怪怪的問題，有的真的不知道怎麼回答。想了半天就說：你實際去試就知道了。""",

            "客戶故事": f"""之前遇到一個人，問了很多問題，最後就說：好那我試試。後來也沒再說什麼了。""",

            "日常分享": f"""今天就這樣，沒什麼特別的。想到什麼就說什麼。""",
        }
        return fallbacks.get(topic, fallbacks["日常分享"])
    
    def generate_daily_posts(self):
        """生成每天三篇"""
        posts = []
        times = ["09:00", "14:00", "21:00"]
        
        for i, time_slot in enumerate(times):
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
    gen = AIContentGenerator()
    
    print("=== 測試單篇生成 ===")
    post = gen.generate_post()
    print(f"人格：{post['persona_name']}")
    print(f"話題：{post['topic']}")
    print(f"內容：\n{post['content']}\n")
    
    print("\n=== 測試每日三篇 ===")
    daily = gen.generate_daily_posts()
    for p in daily:
        print(f"\n[{p['scheduled_time']}] {p['persona_name']} - {p['topic']}")
        print(p['content'])
