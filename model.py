"""
🤖 СУПЕР-БОТ — 15+ БЕСПЛАТНЫХ МОДЕЛЕЙ (ФЕВРАЛЬ 2026)
Автоматически выбирает самую быструю доступную модель
"""

import os
import base64
import requests
import time
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 80)
        print("🤖 ЗАПУСК СУПЕР-БОТА С 15+ БЕСПЛАТНЫМИ МОДЕЛЯМИ")
        print("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        # ⭐ ПОЛНЫЙ СПИСОК БЕСПЛАТНЫХ МОДЕЛЕЙ ⭐
        self.models = [
            # Vision модели (понимают фото)
            {
                "name": "google/gemini-2.0-flash-exp:free",
                "vision": True,
                "timeout": 8,
                "speed": "⚡⚡⚡⚡⚡",
                "desc": "Gemini 2.0 Flash (1M контекста, фото)"
            },
            {
                "name": "qwen/qwen3-vl-235b-a22b-thinking:free",
                "vision": True,
                "timeout": 12,
                "speed": "⚡⚡⚡",
                "desc": "Qwen3 VL 235B (видео, фото)"
            },
            {
                "name": "nvidia/nemotron-nano-2-vl:free",
                "vision": True,
                "timeout": 10,
                "speed": "⚡⚡⚡⚡",
                "desc": "NVIDIA Nemotron VL (OCR, видео)"
            },
            {
                "name": "moonshotai/kimi-vl-a3b-thinking:free",
                "vision": True,
                "timeout": 8,
                "speed": "⚡⚡⚡⚡",
                "desc": "Kimi VL A3B (лёгкая, быстрая)"
            },
            
            # Очень быстрые текстовые модели
            {
                "name": "stepfun/step-3.5-flash:free",
                "vision": False,
                "timeout": 6,
                "speed": "⚡⚡⚡⚡⚡",
                "desc": "Step 3.5 Flash (молниеносная)"
            },
            {
                "name": "z-ai/glm-4.5-air:free",
                "vision": False,
                "timeout": 7,
                "speed": "⚡⚡⚡⚡",
                "desc": "GLM-4.5-Air (быстрая)"
            },
            
            # Универсальные мощные модели
            {
                "name": "arcee-ai/trinity-large-preview:free",
                "vision": False,
                "timeout": 10,
                "speed": "⚡⚡⚡",
                "desc": "Trinity Large (100% uptime)"
            },
            {
                "name": "qwen/qwen3-235b-a22b-thinking:free",
                "vision": False,
                "timeout": 12,
                "speed": "⚡⚡",
                "desc": "Qwen3 235B (математика)"
            },
            {
                "name": "meta-llama/llama-3.3-70b-instruct:free",
                "vision": False,
                "timeout": 10,
                "speed": "⚡⚡⚡",
                "desc": "Llama 3.3 70B (мультиязычная)"
            },
            {
                "name": "openai/gpt-oss-120b:free",
                "vision": False,
                "timeout": 10,
                "speed": "⚡⚡⚡",
                "desc": "GPT-OSS 120B (открытая OpenAI)"
            },
            
            # Специализированные модели
            {
                "name": "deepseek/deepseek-r1:free",
                "vision": False,
                "timeout": 12,
                "speed": "⚡⚡",
                "desc": "DeepSeek R1 (логика)"
            },
            {
                "name": "openrouter/aurora-alpha:free",
                "vision": False,
                "timeout": 8,
                "speed": "⚡⚡⚡⚡",
                "desc": "Aurora Alpha (кодинг, агенты)"
            },
            {
                "name": "openrouter/pony-alpha:free",
                "vision": False,
                "timeout": 9,
                "speed": "⚡⚡⚡",
                "desc": "Pony Alpha (GLM-5, агенты)"
            },
            {
                "name": "upstage/solar-pro-3:free",
                "vision": False,
                "timeout": 8,
                "speed": "⚡⚡⚡⚡",
                "desc": "Solar Pro 3 (многоязычная)"
            },
            {
                "name": "arcee-ai/trinity-mini:free",
                "vision": False,
                "timeout": 6,
                "speed": "⚡⚡⚡⚡⚡",
                "desc": "Trinity Mini (очень быстрая)"
            }
        ]
        
        print(f"\n📊 ЗАГРУЖЕНО МОДЕЛЕЙ: {len(self.models)}")
        print("=" * 80)
        
        # Группируем по скорости
        fast_models = [m for m in self.models if "⚡⚡⚡⚡" in m["speed"]]
        vision_models = [m for m in self.models if m["vision"]]
        
        print(f"⚡ Сверхбыстрых: {len(fast_models)}")
        print(f"📸 С поддержкой фото: {len(vision_models)}")
        print("=" * 80)
        
        self.user_contexts = {}
        print("🚀 СУПЕР-БОТ ГОТОВ К РАБОТЕ!")
        print("=" * 80)
    
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
                print(f"      ✅ {model_config['desc'][:25]}... за {elapsed:.1f}с")
                return answer
            else:
                return None
                
        except Exception:
            return None
    
    def get_response(self, user_id, message):
        """Основной метод для текстовых запросов"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — умный помощник. Решай математику правильно: 150+150/2 = 225. Отвечай кратко и по делу."},
            {"role": "user", "content": message}
        ]
        
        print(f"\n📨 Запрос: {message[:50]}...")
        print(f"🔄 Пробую {len(self.models)} моделей по очереди...")
        
        # Пробуем модели по очереди (сначала самые быстрые)
        for i, model in enumerate(self.models, 1):
            print(f"   {i}. {model['desc'][:30]}... ", end="")
            answer = self.ask_model(model, messages)
            if answer:
                return answer
        
        return "❌ Все нейросети временно недоступны. Попробуй через минуту!"
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото (только vision-модели)"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
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
            
            print(f"\n📸 Анализирую фото {len(self.models)} vision-моделями...")
            
            # Берём только vision-модели
            vision_models = [m for m in self.models if m["vision"]]
            
            for i, model in enumerate(vision_models, 1):
                print(f"   {i}. {model['desc'][:30]}... ", end="")
                answer = self.ask_model(model, image_message)
                if answer:
                    return answer + "\n\n📸 _Проанализировано нейросетью_"
            
            return "❌ Не удалось проанализировать фото. Попробуй ещё раз."
            
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
