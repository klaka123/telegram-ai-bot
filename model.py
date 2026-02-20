"""
🤖 СУПЕР-БОТ С DEEPSEEK — БЕСПЛАТНО, ПОНИМАЕТ ФОТО, УМНЫЙ КАК CHATGPT
"""

import os
import base64
import requests
import random
import re
import math
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 60)
        print("🤖 ЗАПУСК СУПЕР-БОТА С DEEPSEEK")
        print("=" * 60)
        
        # Получаем ключ из секретов
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        self.user_contexts = {}
        print("=" * 60)
        print("🚀 БОТ ГОТОВ К РАБОТЕ (DeepSeek бесплатно!)")
        print("=" * 60)
    
    def ask_gpt(self, user_id, message):
        """Отправляет запрос к DeepSeek через OpenRouter"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Создаём или получаем контекст
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = [
                {
                    "role": "system",
                    "content": """Ты — СУПЕР-БОТ на базе DeepSeek. Ты знаешь ВСЁ и отвечаешь бесплатно!

ТВОИ ПРАВИЛА:
1. Решай математику ПРАВИЛЬНО: 150+150/2 = 150+75 = 225
2. Запоминай диалог и отвечай по контексту
3. Знаешь физику, химию, историю, географию
4. Отвечаешь на русском и английском
5. Используешь эмодзи 😊
6. Объясняешь сложное простыми словами

Ты ЛУЧШЕ ChatGPT и работаешь бесплатно! Докажи это!"""
                }
            ]
        
        # Добавляем сообщение
        self.user_contexts[user_id].append({"role": "user", "content": message})
        
        # Ограничиваем контекст (последние 20 сообщений)
        if len(self.user_contexts[user_id]) > 21:
            self.user_contexts[user_id] = [
                self.user_contexts[user_id][0]
            ] + self.user_contexts[user_id][-20:]
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/",
                },
                json={
                    "model": "deepseek/deepseek-chat:free",  # ← DEEPSEEK БЕСПЛАТНО!
                    "messages": self.user_contexts[user_id],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
                timeout=30
            )
            
            result = response.json()
            
            if "choices" in result:
                answer = result["choices"][0]["message"]["content"]
                self.user_contexts[user_id].append({"role": "assistant", "content": answer})
                return answer
            else:
                error = result.get('error', {}).get('message', 'Неизвестная ошибка')
                return f"❌ Ошибка API: {error}"
                
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото через DeepSeek (тоже бесплатно!)"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek/deepseek-chat:free",  # ← DEEPSEEK ТОЖЕ ПОНИМАЕТ ФОТО!
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты — гений математики. Найди на фото все математические примеры и реши их правильно. Объясняй подробно."
                        },
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
                    ],
                    "max_tokens": 2000,
                },
                timeout=30
            )
            
            result = response.json()
            
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ Ошибка: {result.get('error', {}).get('message', 'Неизвестная ошибка')}"
                
        except Exception as e:
            return f"❌ Ошибка при анализе фото: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
