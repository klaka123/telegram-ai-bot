"""
🤖 СУПЕР-БОТ — ФИНАЛЬНАЯ ВЕРСИЯ
Только проверенные модели: Gemini, Microsoft, Qwen
"""

import os
import base64
import requests
import time
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 60)
        print("🤖 СУПЕР-БОТ — ФИНАЛЬНАЯ ВЕРСИЯ")
        print("=" * 60)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН!")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
        
        # ⭐ ТОЛЬКО РАБОЧИЕ МОДЕЛИ ⭐
        self.models = [
            "google/gemini-2.0-flash-exp:free",     # Всегда работает
            "microsoft/phi-3.5-mini-128k-instruct:free",  # Стабильная
            "qwen/qwen2.5-vl-7b-instruct:free"      # Для фото
        ]
        
        print(f"\n✅ Модель 1: Gemini 2.0 Flash")
        print(f"✅ Модель 2: Microsoft Phi-3.5")
        print(f"✅ Модель 3: Qwen VL")
        
        self.user_contexts = {}
        print("=" * 60)
        print("🚀 БОТ ГОТОВ К РАБОТЕ!")
        print("=" * 60)
    
    def ask_model(self, model_name, messages):
        """Спрашивает одну модель"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
                timeout=30
            )
            
            result = response.json()
            return result["choices"][0]["message"]["content"] if "choices" in result else ""
        except:
            return ""
    
    def get_response(self, user_id, message):
        """Получает ответ от первой работающей модели"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — умный помощник. Решай математику правильно: 150+150/2 = 225."},
            {"role": "user", "content": message}
        ]
        
        # Пробуем модели по очереди
        for model in self.models:
            print(f"🔄 Пробую {model[:20]}...")
            answer = self.ask_model(model, messages)
            if answer:
                return answer
        
        return "❌ Все нейросети временно недоступны. Попробуй через минуту."
    
    def analyze_photo(self, photo_bytes):
        """Анализирует фото"""
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {"role": "system", "content": "Ты — гений математики. Реши примеры на фото."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Пробуем модели по очереди
            for model in self.models:
                answer = self.ask_model(model, messages)
                if answer:
                    return answer
            
            return "❌ Не удалось проанализировать фото."
            
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"

brain = SuperBot()
