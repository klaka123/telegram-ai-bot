"""
🤖 СУПЕР-БОТ — ТРИ БЫСТРЫЕ МОДЕЛИ (ФЕВРАЛЬ 2026)
Gemini 2.0 Flash + Trinity Large + Step 3.5 Flash
"""

import os
import base64
import requests
import time
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 70)
        print("🤖 ЗАПУСК ТРЁХ БЫСТРЫХ НЕЙРОСЕТЕЙ")
        print("=" * 70)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        # ⭐ ТРИ САМЫЕ БЫСТРЫЕ МОДЕЛИ ⭐
        self.models = [
            {
                "name": "google/gemini-2.0-flash-exp:free",
                "timeout": 8,
                "emoji": "⚡",
                "description": "Gemini 2.0 Flash (самая быстрая, 1M контекста)"
            },
            {
                "name": "arcee-ai/trinity-large-preview:free",
                "timeout": 10,
                "emoji": "🎯",
                "description": "Trinity Large (100% uptime, отличная математика)"
            },
            {
                "name": "stepfun/step-3.5-flash:free",
                "timeout": 8,
                "emoji": "🚀",
                "description": "Step 3.5 Flash (быстрая, стабильная)"
            }
        ]
        
        print(f"\n✅ Модель 1: {self.models[0]['description']}")
        print(f"✅ Модель 2: {self.models[1]['description']}")
        print(f"✅ Модель 3: {self.models[2]['description']}")
        
        self.user_contexts = {}
        print("=" * 70)
        print("🚀 ТРИ БЫСТРЫЕ НЕЙРОСЕТИ ГОТОВЫ!")
        print("=" * 70)
    
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
                timeout=model_config["timeout"]
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                print(f"      {model_config['emoji']} Ответ за {elapsed:.1f}с")
                return answer
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Неизвестная ошибка')
                print(f"      ❌ Ошибка: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"      ⏱️ Таймаут {model_config['timeout']}с")
            return None
        except Exception as e:
            print(f"      ❌ Ошибка")
            return None
    
    def ensemble_think(self, user_id, question, is_photo=False):
        """Три модели думают и объединяют ответы"""
        
        # Системный промпт для всех моделей
        if is_photo:
            system_prompt = """Ты — гений математики. Найди на фото все математические примеры и реши их правильно.
Отвечай кратко и по делу. Решай строго по правилам: сначала умножение/деление, потом сложение/вычитание.
Например: 150+150/2 = 150+75 = 225"""
        else:
            system_prompt = """Ты — умный помощник. Отвечай кратко и по делу.
Решай математику строго по правилам: сначала умножение/деление, потом сложение/вычитание.
Например: 150+150/2 = 150+75 = 225"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        print(f"\n🤔 Опрашиваю три быстрые нейросети...")
        
        # Опрашиваем все три модели параллельно
        answers = []
        working_models = []
        
        for i, model in enumerate(self.models, 1):
            print(f"   {i}. {model['description'][:30]}... ", end="")
            answer = self.ask_model(model, messages)
            if answer:
                answers.append(answer)
                working_models.append(model)
        
        # Анализируем результаты
        if not answers:
            return "❌ Извини, сейчас все нейросети временно недоступны. Попробуй через минуту!"
        
        if len(answers) == 1:
            return answers[0] + "\n\n_⚡ Ответ от одной нейросети_"
        
        if len(answers) == 2:
            # Объединяем два ответа через главную модель
            merge_prompt = f"""Вот два ответа от разных ИИ на вопрос: "{question}"

ОТВЕТ 1:
{answers[0]}

ОТВЕТ 2:
{answers[1]}

Объедини их в один лучший ответ. Возьми лучшее из каждого.
Ответ должен быть точным и полным."""
            
            merge_messages = [
                {"role": "system", "content": "Ты — главный аналитик."},
                {"role": "user", "content": merge_prompt}
            ]
            
            print("🔄 Объединяю два ответа...")
            final = self.ask_model(self.models[0], merge_messages)
            return final if final else answers[0]
        
        # Три ответа — объединяем через Trinity (лучшая для анализа)
        merge_prompt = f"""Вот три ответа от разных ИИ на вопрос: "{question}"

ОТВЕТ 1 (Gemini):
{answers[0]}

ОТВЕТ 2 (Trinity):
{answers[1]}

ОТВЕТ 3 (Step):
{answers[2]}

Создай ОДИН ИТОГОВЫЙ ЛУЧШИЙ ОТВЕТ.
Возьми лучшее из каждого ответа, убери повторы, исправь ошибки.
В конце добавь: "✅ Ответ проверен тремя быстрыми нейросетями"."""
        
        merge_messages = [
            {"role": "system", "content": "Ты — главный аналитик, объединяющий ответы трёх ИИ."},
            {"role": "user", "content": merge_prompt}
        ]
        
        print("🔄 Объединяю три ответа...")
        final_answer = self.ask_model(self.models[1], merge_messages)  # Trinity как анализатор
        
        return final_answer if final_answer else answers[0]
    
    def get_response(self, user_id, message):
        """Основной метод для текстовых запросов"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Создаём контекст
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
        
        self.user_contexts[user_id].append({"role": "user", "content": message})
        
        # Получаем ответ
        answer = self.ensemble_think(user_id, message, is_photo=False)
        
        self.user_contexts[user_id].append({"role": "assistant", "content": answer})
        
        # Ограничиваем историю
        if len(self.user_contexts[user_id]) > 20:
            self.user_contexts[user_id] = self.user_contexts[user_id][-20:]
        
        return answer
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            # Создаём сообщение с фото
            image_message = [
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
            
            print("\n📸 Анализирую фото тремя нейросетями...")
            
            # Пробуем все модели (Gemini и Trinity понимают фото)
            answers = []
            for model in self.models[:2]:  # Gemini и Trinity понимают фото
                print(f"   Пробую {model['description'][:20]}...")
                answer = self.ask_model(model, image_message)
                if answer:
                    answers.append(answer)
                    break  # Берём первый успешный ответ
            
            if answers:
                return answers[0] + "\n\n📸 _Проанализировано нейросетью_"
            else:
                return "❌ Не удалось проанализировать фото. Попробуй ещё раз."
            
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
