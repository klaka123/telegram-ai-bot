"""
🤖 СУПЕР-БОТ — УПРОЩЕННАЯ ВЕРСИЯ
Одна надежная модель: Google Gemini 2.0 Flash
"""

import os
import base64
import requests
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 60)
        print("🤖 ЗАПУСК БОТА (УПРОЩЕННАЯ ВЕРСИЯ)")
        print("=" * 60)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        # ⭐ Используем только самую надежную модель
        self.model = "google/gemini-2.0-flash-exp:free"
        print(f"✅ Модель: {self.model}")
        
        self.user_contexts = {}
        print("=" * 60)
        print("🚀 БОТ ГОТОВ К РАБОТЕ!")
        print("=" * 60)
    
    def ask_model(self, messages):
        """Спрашивает модель"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
                timeout=30
            )
            
            result = response.json()
            
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                error = result.get('error', {}).get('message', 'Неизвестная ошибка')
                return f"❌ Ошибка API: {error}"
                
        except Exception as e:
            return f"❌ Ошибка подключения: {str(e)}"
    
    def get_response(self, user_id, message):
        """Получает ответ от модели"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — умный помощник. Решай математику правильно: 150+150/2 = 225. Отвечай на русском языке."},
            {"role": "user", "content": message}
        ]
        
        answer = self.ask_model(messages)
        return answer
    
    def analyze_photo(self, photo_bytes):
        """Анализирует фото"""
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {"role": "system", "content": "Ты — гений математики. Реши примеры на фото. Отвечай на русском языке."},
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
            
            answer = self.ask_model(messages)
            return answer
            
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"

brain = SuperBot()
