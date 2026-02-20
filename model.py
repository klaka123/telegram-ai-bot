"""
🤖 СУПЕР-БОТ С GPT-4o — ПОНИМАЕТ ФОТО И ТЕКСТ
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
        print("🤖 ЗАПУСК СУПЕР-БОТА С GPT-4o")
        print("=" * 60)
        
        # Получаем ключ из секретов
        self.api_key = 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
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
            print(f"   Первые символы: {self.api_key[:10]}...")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        self.user_contexts = {}
        print("=" * 60)
        print("🚀 БОТ ГОТОВ К РАБОТЕ")
        print("=" * 60)
    
    def ask_gpt(self, user_id, message):
        """Отправляет запрос к GPT-4o через OpenRouter"""
        
        if not self.api_key:
            return self.local_response(message)
        
        # Создаём или получаем контекст
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = [
                {
                    "role": "system",
                    "content": """Ты — СУПЕР-БОТ с GPT-4o. Ты знаешь ВСЁ.

ТВОИ ПРАВИЛА:
1. Решай математику ПРАВИЛЬНО: 150+150/2 = 150+75 = 225
2. Запоминай диалог и отвечай по контексту
3. Знаешь физику, химию, историю, географию
4. Отвечаешь на русском и английском
5. Используешь эмодзи 😊
6. Объясняешь сложное простыми словами

Ты ЛУЧШЕ ChatGPT! Докажи это!"""
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
                    "model": "openai/gpt-4o",
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
                return f"❌ Ошибка API: {error}\n\n{self.local_response(message)}"
                
        except Exception as e:
            return f"❌ Ошибка: {str(e)}\n\n{self.local_response(message)}"
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото через GPT-4o Vision"""
        
        if not self.api_key:
            return "❌ Нет ключа API. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4o",
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
    
    def local_response(self, message):
        """Запасные ответы на случай отсутствия API"""
        msg = message.lower().strip()
        
        # Математика с приоритетом
        if re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', msg):
            try:
                result = eval(msg)
                return f"✅ {msg} = {result}"
            except:
                pass
        
        # Приветствия
        if msg in ['привет', 'здравствуй', 'хай']:
            return "Привет! Я временно работаю в локальном режиме. Скоро подключу GPT-4o! 😊"
        
        return "⏳ Ожидаю подключения к GPT-4o..."
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
