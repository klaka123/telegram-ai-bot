"""
🤖 СУПЕР-БОТ — ДИАГНОСТИЧЕСКАЯ ВЕРСИЯ
Показывает реальные ошибки OpenRouter
"""

import os
import base64
import requests
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 70)
        print("🔍 ДИАГНОСТИЧЕСКАЯ ВЕРСИЯ")
        print("=" * 70)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ НЕ НАЙДЕН!")
        
        # Единственная модель для теста
        self.model = "google/gemini-2.0-flash-exp:free"
        print(f"✅ МОДЕЛЬ: {self.model}")
        print("=" * 70)
    
    def ask_model(self, messages):
        """Прямой запрос к OpenRouter"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=15  # Не ждем долго
            )
            
            # Показываем статус ответа
            print(f"📊 Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                # Показываем реальную ошибку
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Неизвестная ошибка')
                error_code = error_data.get('error', {}).get('code', response.status_code)
                
                # Человеческое объяснение ошибки [citation:8]
                if error_code == 402:
                    return "❌ Закончились бесплатные запросы на сегодня. Лимит 50 сообщений/день для бесплатных аккаунтов. Сброс в 19:00 по Москве."
                elif error_code == 429:
                    return "❌ Слишком много запросов. Подождите немного."
                elif error_code == 404:
                    return "❌ Модель временно недоступна. Попробуйте позже."
                else:
                    return f"❌ Ошибка {error_code}: {error_msg}"
                
        except requests.exceptions.Timeout:
            return "❌ Таймаут — сервер не отвечает. Попробуйте позже."
        except Exception as e:
            return f"❌ Ошибка подключения: {str(e)}"
    
    def get_response(self, user_id, message):
        """Простой ответ"""
        if not self.api_key:
            return "❌ Добавь OPENROUTER_KEY в секреты GitHub!"
        
        messages = [
            {"role": "system", "content": "Ты помощник. Отвечай кратко."},
            {"role": "user", "content": message}
        ]
        
        return self.ask_model(messages)
    
    def analyze_photo(self, photo_bytes):
        """Анализ фото"""
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            messages = [
                {"role": "system", "content": "Реши примеры на фото."},
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
            return self.ask_model(messages)
        except Exception as e:
            return f"❌ Ошибка фото: {str(e)}"

brain = SuperBot()
