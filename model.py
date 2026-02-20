"""
🤖 СУПЕР-БОТ — С НАДЕЖНЫМИ ТАЙМАУТАМИ
Никаких зависаний!
"""

import os
import base64
import requests
import time
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 60)
        print("🤖 ЗАПУСК БОТА (С ТАЙМАУТАМИ)")
        print("=" * 60)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН!")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
        
        # Модели по порядку
        self.models = [
            {"name": "google/gemini-2.0-flash-exp:free", "timeout": 10},
            {"name": "microsoft/phi-3.5-mini-128k-instruct:free", "timeout": 8},
            {"name": "qwen/qwen2.5-vl-7b-instruct:free", "timeout": 10}
        ]
        
        print(f"\n✅ Модель 1: Gemini 2.0 Flash (таймаут 10с)")
        print(f"✅ Модель 2: Microsoft Phi-3.5 (таймаут 8с)")
        print(f"✅ Модель 3: Qwen VL (таймаут 10с)")
        
        self.user_contexts = {}
        print("=" * 60)
        print("🚀 БОТ ГОТОВ К РАБОТЕ!")
        print("=" * 60)
    
    def ask_model(self, model_config, messages):
        """Спрашивает одну модель с таймаутом"""
        try:
            start_time = time.time()
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/",
                },
                json={
                    "model": model_config["name"],
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 800,
                },
                timeout=model_config["timeout"]  # Индивидуальный таймаут
            )
            
            elapsed = time.time() - start_time
            print(f"      Ответ за {elapsed:.1f}с")
            
            result = response.json()
            
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return None
                
        except requests.exceptions.Timeout:
            print(f"      ⏱️ Таймаут {model_config['timeout']}с")
            return None
        except Exception as e:
            print(f"      ❌ Ошибка")
            return None
    
    def get_response(self, user_id, message):
        """Получает ответ от первой ответившей модели"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        print(f"\n📨 Запрос: {message[:50]}...")
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — умный помощник. Отвечай кратко и по делу. Решай математику правильно: 150+150/2 = 225."},
            {"role": "user", "content": message}
        ]
        
        # Пробуем модели по очереди с таймаутами
        for model in self.models:
            print(f"🔄 Пробую {model['name'][:20]}...")
            answer = self.ask_model(model, messages)
            if answer:
                return answer
        
        # Если все модели не ответили
        return "❌ Ни одна нейросеть не ответила вовремя. Попробуй через минуту!"
    
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
