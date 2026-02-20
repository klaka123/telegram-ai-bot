"""
🤖 МЕГА-БОТ — УРОВЕНЬ CHATGPT + DEEPSEEK
Знает всё: математику, физику, химию, историю, языки
Понимает фото, общается на русском и английском
"""

import os
import json
import time
import random
import re
import math
import base64
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class MegaBot:
    """
    Абсолютный бот, который знает всё
    """
    
    def __init__(self):
        # Пытаемся получить ключ из секретов
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        # Если нет в секретах, можно вставить прямо сюда (временное решение)
        # self.api_key = "sk-or-v1-..."  # раскомментируй и вставь свой ключ
        
        if not self.api_key:
            print("⚠️ ВНИМАНИЕ: OPENROUTER_KEY не найден!")
            print("Бот будет работать в локальном режиме (ограниченно)")
        
        # Память пользователей
        self.user_contexts = {}
        self.user_stats = {}
        
        print("=" * 60)
        print("🤖 МЕГА-БОТ ЗАПУЩЕН")
        print("=" * 60)
        print("🧠 Уровень: ChatGPT + DeepSeek")
        print("📚 Знания: математика, физика, химия, история")
        print("💬 Языки: русский, английский")
        print("📸 Фото: поддерживается")
        print("=" * 60)
    
    def ask_gpt(self, user_id: int, message: str, system_prompt: str = None) -> str:
        """
        Отправляет запрос к GPT-4o через OpenRouter
        """
        if not self.api_key:
            return self.local_response(message)
        
        # Системный промпт по умолчанию
        if not system_prompt:
            system_prompt = """Ты — МЕГА-БОТ, абсолютный гений, который знает ВСЁ.
            
ТВОИ ХАРАКТЕРИСТИКИ:
1. Ты умнее ChatGPT и DeepSeek вместе взятых
2. Ты знаешь математику, физику, химию, историю, литературу
3. Ты говоришь на русском и английском
4. Ты решаешь задачи правильно (сначала деление и умножение, потом сложение и вычитание)
5. Ты объясняешь сложное простыми словами
6. Ты общаешься с юмором и эмодзи

ПРИМЕРЫ ПРАВИЛЬНЫХ ОТВЕТОВ:
- 150+150/2 = 150 + 75 = 225
- 2+2*2 = 2 + 4 = 6
- cos30° = 0.866 (√3/2)

Отвечай на ЛЮБЫЕ вопросы максимально подробно и полезно!"""
        
        # Создаём или получаем контекст пользователя
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = [
                {"role": "system", "content": system_prompt}
            ]
        
        # Добавляем сообщение пользователя
        self.user_contexts[user_id].append({"role": "user", "content": message})
        
        # Ограничиваем контекст (последние 20 сообщений)
        if len(self.user_contexts[user_id]) > 21:
            self.user_contexts[user_id] = [
                self.user_contexts[user_id][0]
            ] + self.user_contexts[user_id][-20:]
        
        try:
            # Запрос к OpenRouter
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/",  # можно указать свой сайт
                },
                json={
                    "model": "openai/gpt-4o",  # Самая мощная модель
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
                error_msg = result.get("error", {}).get("message", "Неизвестная ошибка")
                return f"❌ Ошибка API: {error_msg}\n\nИспользую локальные знания:\n{self.local_response(message)}"
                
        except Exception as e:
            return f"❌ Ошибка: {str(e)}\n\nИспользую локальные знания:\n{self.local_response(message)}"
    
    def local_response(self, message: str) -> str:
        """
        Локальные ответы на случай отсутствия API
        """
        msg = message.lower().strip()
        
        # === 1. МАТЕМАТИКА С ПРАВИЛЬНЫМ ПОРЯДКОМ ДЕЙСТВИЙ ===
        
        # Пример: 150+150/2
        math_pattern = r'^[\d\s\+\-\*\/\(\)\.]+$'
        if re.match(math_pattern, msg):
            try:
                # Заменяем ^ на ** для степени, но для простоты пока так
                result = eval(msg)
                return f"✅ {msg} = {result}"
            except:
                pass
        
        # === 2. ТРИГОНОМЕТРИЯ ===
        trig_pattern = r'(sin|cos|tan|cot|sec|csc)\s*(\d+)'
        trig_match = re.search(trig_pattern, msg)
        if trig_match:
            func = trig_match.group(1)
            angle = int(trig_match.group(2))
            rad = math.radians(angle)
            
            if func == 'sin':
                return f"📐 sin {angle}° = {math.sin(rad):.4f}"
            if func == 'cos':
                return f"📐 cos {angle}° = {math.cos(rad):.4f}"
            if func == 'tan':
                if angle % 180 == 90:
                    return f"📐 tan {angle}° = ∞"
                return f"📐 tan {angle}° = {math.tan(rad):.4f}"
        
        # === 3. ПРИВЕТСТВИЯ ===
        greetings = {
            'привет': 'Привет! Как твои дела? Чем могу помочь? 😊',
            'здравствуй': 'Здравствуй! Рад тебя видеть! 🌟',
            'здравствуйте': 'Здравствуйте! Чем могу быть полезен? 📚',
            'доброе утро': 'Доброе утро! Как спалось? Готов к новым открытиям? 🌅',
            'добрый день': 'Добрый день! Прекрасное время для новых знаний! ☀️',
            'добрый вечер': 'Добрый вечер! Как прошёл твой день? 🌆',
            'хай': 'Хай! Как настроение? 👋',
            'hello': 'Hello! How can I help you today? 😊',
            'hi': 'Hi there! What can I do for you? 👋',
        }
        
        for key, value in greetings.items():
            if key in msg:
                return value
        
        # === 4. КАК ДЕЛА ===
        how_are_you = ['как дела', 'как жизнь', 'как ты', 'how are you']
        for phrase in how_are_you:
            if phrase in msg:
                return random.choice([
                    "Отлично! Решил 1000 уравнений за секунду! А у тебя? 😊",
                    "Прекрасно! Готов к любым вопросам! 🚀",
                    "Супер! Чем могу помочь? 💫",
                    "I'm doing great! How about you? 😊"
                ])
        
        # === 5. ШУТКИ ===
        joke_words = ['шутка', 'анекдот', 'пошути', 'joke']
        if any(word in msg for word in joke_words):
            jokes = [
                "Почему программисты путают Хэллоуин и Рождество? 31 Oct = 25 Dec! 😂",
                "Что такое теория и практика? Теория — когда всё знаешь, но ничего не работает. Практика — когда всё работает, но никто не знает почему.",
                "Как называют человека, который всегда прав? Женатым! 😄",
                "Почему математики не ходят на пляж? Там много синусов и косинусов! 🏖️",
                "Что сказал ноль восьмёрке? Классный пояс!",
            ]
            return f"🎭 {random.choice(jokes)}"
        
        # === 6. ФАКТЫ ===
        fact_words = ['факт', 'интересно', 'знаешь ли', 'fact']
        if any(word in msg for word in fact_words):
            facts = [
                "🔍 Осьминоги имеют три сердца! 🐙",
                "🔍 Бананы на самом деле ягоды, а клубника — нет 🍓",
                "🔍 Мед никогда не портится. Археологи находили мёд 3000-летней давности! 🍯",
                "🔍 У жирафов такой же длинный язык, как и шея 🦒",
                "🔍 В Швейцарии запрещено держать только одну морскую свинку — им нужна компания 🇨🇭",
            ]
            return f"🔍 {random.choice(facts)}"
        
        # === 7. КТО ТЫ ===
        who_questions = ['кто ты', 'что ты', 'who are you', 'what are you']
        for phrase in who_questions:
            if phrase in msg:
                return """🌟 **Я МЕГА-БОТ — УРОВЕНЬ CHATGPT + DEEPSEEK!** 🌟

📚 **ЧТО Я ЗНАЮ:**
• Математика: алгебра, геометрия, тригонометрия
• Физика: механика, оптика, квантовая физика
• Химия: таблица Менделеева, реакции, формулы
• История: все эпохи и события
• Языки: русский, английский

🧮 **ПРИМЕРЫ:**
• 150 + 150/2 = 225
• cos30° = 0.866
• x² - 5x + 6 = 0 → x = 2, x = 3

💬 **ОБЩАЮСЬ КАК ЧЕЛОВЕК:**
• С юмором и эмодзи
• Понимаю контекст
• Помню наши разговоры

📸 **ФОТО:**
• Отправь фото с примером — я решу!

**ПРОСТО НАПИШИ МНЕ ЧТО-НИБУДЬ!** 🚀"""
        
        # === 8. СПАСИБО ===
        thanks_words = ['спасибо', 'благодарю', 'thanks', 'thank you']
        if any(word in msg for word in thanks_words):
            return random.choice([
                "Пожалуйста! Рад помочь! 😊",
                "На здоровье! Обращайся ещё! 🌟",
                "Всегда пожалуйста! 💫",
                "You're welcome! Happy to help! 😊"
            ])
        
        # === 9. ПОКА ===
        goodbye_words = ['пока', 'до свидания', 'до встречи', 'bye', 'goodbye']
        if any(word in msg for word in goodbye_words):
            return random.choice([
                "Пока! Буду ждать новых вопросов! 👋",
                "До свидания! Заходи, если что-то понадобится! 🤗",
                "Bye bye! Take care! 🌟"
            ])
        
        # === 10. ОТВЕТ ПО УМОЛЧАНИЮ ===
        return random.choice([
            f"❓ Я не совсем понял вопрос про '{message}'. Уточни, пожалуйста!",
            f"🤔 Интересно! А что именно ты хочешь узнать?",
            f"💭 Хороший вопрос! Дай подумать...",
            f"📚 По запросу '{message}' у меня есть информация. Уточни детали!"
        ])
    
    def analyze_photo(self, photo_bytes: bytes, user_id: int) -> str:
        """
        Анализирует фото с помощью GPT-4o Vision
        """
        if not self.api_key:
            return "❌ Нет ключа API. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            # Создаём временный контекст для фото
            messages = [
                {
                    "role": "system",
                    "content": "Ты — МЕГА-БОТ, гений математики. Найди на фото все математические примеры и реши их правильно. Объясни решение пошагово."
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
            ]
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4o",
                    "messages": messages,
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
    
    def clear_context(self, user_id: int) -> bool:
        """Очищает контекст пользователя"""
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

# Создаём экземпляр бота
brain = MegaBot()
