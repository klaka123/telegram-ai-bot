"""
🤖 СУПЕР-КОМБО ИЗ ТРЁХ НЕЙРОСЕТЕЙ
Llama 3.3 + Gemini 2.0 + Qwen VL = ИДЕАЛЬНЫЙ ОТВЕТ!
"""

import os
import base64
import requests
import time
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 70)
        print("🤖 ЗАПУСК СУПЕР-КОМБО ИЗ ТРЁХ НЕЙРОСЕТЕЙ")
        print("=" * 70)
        
        # Получаем ключ из секретов
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        # Три лучшие бесплатные модели
        self.models = [
            "meta-llama/llama-3.3-70b-instruct:free",  # #1 Главный аналитик
            "google/gemini-2.0-flash-exp:free",        # #2 Проверяющий
            "qwen/qwen2.5-vl-7b-instruct:free"         # #3 Специалист по деталям
        ]
        
        print(f"\n🔹 Модель 1: {self.models[0]} (Llama 3.3)")
        print(f"🔹 Модель 2: {self.models[1]} (Gemini 2.0)")
        print(f"🔹 Модель 3: {self.models[2]} (Qwen VL)")
        print("\n🔄 Режим: ТРИ ИИ ОБДУМЫВАЮТ И ВЫДАЮТ ОДИН ОТВЕТ")
        
        self.user_contexts = {}
        print("=" * 70)
        print("🚀 СУПЕР-КОМБО ГОТОВО К РАБОТЕ!")
        print("=" * 70)
    
    def ask_one_model(self, model_name, messages):
        """Спрашивает одну конкретную модель"""
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
            
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return f"[Ошибка {model_name}]"
                
        except Exception as e:
            return f"[Ошибка {model_name}: {str(e)}]"
    
    def ensemble_think(self, user_id, question):
        """
        ТРИ ИИ ОБДУМЫВАЮТ ВОПРОС И ВЫДАЮТ ОДИН ОТВЕТ
        """
        
        # Системный промпт для всех
        system_prompt = """Ты — часть команды из трёх ИИ. Мы вместе думаем над вопросом.
Отвечай кратко, по существу, но максимально полезно.
Твоя задача — дать лучший ответ, который потом объединят с ответами других ИИ."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        print(f"\n🤔 Опрашиваю три нейросети...")
        
        # Опрашиваем все три модели
        answers = []
        for i, model in enumerate(self.models, 1):
            print(f"   {i}. {model[:20]}... ", end="")
            answer = self.ask_one_model(model, messages)
            answers.append(answer)
            print(f"✅ ({len(answer)} символов)")
            time.sleep(0.5)  # Небольшая пауза между запросами
        
        # Теперь просим первую модель объединить ответы
        merge_prompt = f"""Вот три ответа от разных ИИ на вопрос: "{question}"

ОТВЕТ 1 (Llama 3.3):
{answers[0]}

ОТВЕТ 2 (Gemini 2.0):
{answers[1]}

ОТВЕТ 3 (Qwen VL):
{answers[2]}

Твоя задача: проанализируй все три ответа и создай ОДИН ИТОГОВЫЙ ЛУЧШИЙ ОТВЕТ.
Возьми лучшее из каждого, убери повторы, исправь ошибки.
Ответ должен быть полным, точным и понятным."""
        
        merge_messages = [
            {"role": "system", "content": "Ты — главный аналитик, объединяющий ответы трёх ИИ."},
            {"role": "user", "content": merge_prompt}
        ]
        
        print("🔄 Объединяю ответы трёх ИИ...")
        final_answer = self.ask_one_model(self.models[0], merge_messages)
        
        return final_answer
    
    def ask_gpt(self, user_id, message):
        """Основной метод - использует ансамбль из трёх ИИ"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Создаём контекст
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
        
        # Добавляем сообщение в историю
        self.user_contexts[user_id].append({"role": "user", "content": message})
        
        # Получаем ответ от ансамбля
        answer = self.ensemble_think(user_id, message)
        
        # Сохраняем ответ в историю
        self.user_contexts[user_id].append({"role": "assistant", "content": answer})
        
        # Ограничиваем историю (последние 10 сообщений)
        if len(self.user_contexts[user_id]) > 20:
            self.user_contexts[user_id] = self.user_contexts[user_id][-20:]
        
        return answer
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото через три ИИ"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            # Создаём сообщение с фото для всех моделей
            image_message = [
                {
                    "role": "system",
                    "content": "Ты — гений математики. Найди на фото все математические примеры и реши их."
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
            
            print("\n📸 Анализирую фото тремя нейросетями...")
            
            # Опрашиваем все три модели
            answers = []
            for i, model in enumerate(self.models, 1):
                print(f"   {i}. {model[:20]}... ", end="")
                answer = self.ask_one_model(model, image_message)
                answers.append(answer)
                print(f"✅")
                time.sleep(0.5)
            
            # Объединяем ответы
            merge_prompt = f"""Вот три ответа от разных ИИ на анализ фотографии:

ОТВЕТ 1 (Llama 3.3):
{answers[0]}

ОТВЕТ 2 (Gemini 2.0):
{answers[1]}

ОТВЕТ 3 (Qwen VL):
{answers[2]}

Создай ОДИН ИТОГОВЫЙ ОТВЕТ, объединив лучшее из всех трёх.
Если на фото есть примеры - реши их правильно.
Если есть геометрические фигуры - опиши их."""
            
            merge_messages = [
                {"role": "system", "content": "Ты — главный аналитик, объединяющий ответы трёх ИИ."},
                {"role": "user", "content": merge_prompt}
            ]
            
            print("🔄 Объединяю ответы трёх ИИ...")
            final_answer = self.ask_one_model(self.models[0], merge_messages)
            
            return final_answer
            
        except Exception as e:
            return f"❌ Ошибка при анализе фото: {str(e)}"
    
    def clear_context(self, user_id):
        """Очищает контекст пользователя"""
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

# Создаём экземпляр супер-комбо
brain = SuperBot()
