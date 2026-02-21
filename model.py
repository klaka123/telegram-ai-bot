"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 31 НЕЙРОСЕТЬ
Умный выбор моделей в зависимости от сложности вопроса
"""

import os
import base64
import requests
import time
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SuperBot:
    def __init__(self):
        logging.info("=" * 80)
        logging.info("ЗАПУСК АНАЛИТИЧЕСКОЙ СИСТЕМЫ — 31 НЕЙРОСЕТЬ")
        logging.info("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        self.bot_instance = None
        
        if not self.api_key:
            logging.error("❌ API ключ не найден!")
        
        # === ⚡ СВЕРХБЫСТРЫЕ МОДЕЛИ (до 4 сек) — для простых вопросов ===
        self.fast_models = [
            {"name": "stepfun/step-3.5-flash:free", "timeout": 4, "desc": "Step 3.5 Flash", "speed": 0.98},
            {"name": "arcee-ai/trinity-mini:free", "timeout": 4, "desc": "Trinity Mini", "speed": 0.97},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "timeout": 4, "desc": "LFM2.5 Thinking", "speed": 0.96},
            {"name": "mistralai/mistral-7b-v3:free", "timeout": 4, "desc": "Mistral 7B v3", "speed": 0.95},
            {"name": "z-ai/glm-4.5-air:free", "timeout": 4, "desc": "GLM-4.5-Air", "speed": 0.94},
            {"name": "liquidai/lfm2.5-1.2b-instruct:free", "timeout": 4, "desc": "LFM2.5 Instruct", "speed": 0.95},
        ]
        
        # === 🧠 МОЩНЫЕ УНИВЕРСАЛЬНЫЕ МОДЕЛИ — для сложных вопросов ===
        self.powerful_models = [
            {"name": "google/gemini-2.0-flash-exp:free", "timeout": 6, "desc": "Gemini 2.0 Flash", "speed": 0.9},
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "timeout": 7, "desc": "Llama 3.3 70B", "speed": 0.85},
            {"name": "arcee-ai/trinity-large-preview:free", "timeout": 8, "desc": "Trinity Large", "speed": 0.82},
            {"name": "openai/gpt-oss-120b:free", "timeout": 7, "desc": "GPT-OSS 120B", "speed": 0.83},
            {"name": "deepseek/deepseek-r1:free", "timeout": 8, "desc": "DeepSeek R1", "speed": 0.81},
            {"name": "upstage/solar-pro-3:free", "timeout": 7, "desc": "Solar Pro 3", "speed": 0.84},
            {"name": "qwen/qwen3-235b-a22b-thinking:free", "timeout": 8, "desc": "Qwen3 235B", "speed": 0.8},
            {"name": "nvidia/nemotron-3-nano-30b:free", "timeout": 7, "desc": "Nemotron 3 Nano", "speed": 0.82},
            {"name": "mistralai/devstral-2512:free", "timeout": 6, "desc": "Devstral 2", "speed": 0.86},
            {"name": "openrouter/aurora-alpha:free", "timeout": 6, "desc": "Aurora Alpha", "speed": 0.87},
            {"name": "openrouter/pony-alpha:free", "timeout": 7, "desc": "Pony Alpha", "speed": 0.84},
            {"name": "xiaomi/mimo-v2-flash:free", "timeout": 6, "desc": "MiMo-V2-Flash", "speed": 0.86},
            {"name": "qwen/qwen3-coder-480b:free", "timeout": 8, "desc": "Qwen3 Coder", "speed": 0.79},
        ]
        
        # === 📸 VISION МОДЕЛИ (для фото) ===
        self.vision_models = [
            {"name": "google/gemini-2.0-flash-exp:free", "timeout": 6, "desc": "Gemini 2.0 Flash", "vision": True},
            {"name": "nvidia/nemotron-nano-2-vl:free", "timeout": 7, "desc": "NVIDIA Nemotron VL", "vision": True},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "timeout": 8, "desc": "Qwen3 VL 235B", "vision": True},
            {"name": "google/gemini-3-flash-preview:free", "timeout": 6, "desc": "Gemini 3 Flash", "vision": True},
            {"name": "moonshotai/kimi-vl-a3b-thinking:free", "timeout": 6, "desc": "Kimi VL A3B", "vision": True},
            {"name": "google/gemma-3-27b:free", "timeout": 7, "desc": "Gemma 3 27B", "vision": True},
        ]
        
        logging.info(f"⚡ СВЕРХБЫСТРЫХ МОДЕЛЕЙ: {len(self.fast_models)}")
        logging.info(f"🧠 МОЩНЫХ МОДЕЛЕЙ: {len(self.powerful_models)}")
        logging.info(f"📸 VISION МОДЕЛЕЙ: {len(self.vision_models)}")
        logging.info(f"📊 ВСЕГО: {len(self.fast_models) + len(self.powerful_models)}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
    
    def set_bot(self, bot):
        """Устанавливает экземпляр бота"""
        self.bot_instance = bot
    
    def is_complex_question(self, text):
        """Определяет сложность вопроса"""
        # Длинные вопросы (>100 символов) считаются сложными
        if len(text) > 100:
            return True
        
        # Ключевые слова, требующие мощных моделей
        complex_keywords = [
            'объясни', 'почему', 'как работает', 'сравни', 
            'проанализируй', 'напиши код', 'формула', 
            'закон', 'теорема', 'докажи', 'research',
            'алгоритм', 'архитектура', 'концепция',
            'разница между', 'преимущества и недостатки',
            'история', 'философия', 'научный'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in complex_keywords)
    
    def format_time(self, seconds):
        """Форматирует время"""
        if seconds < 60:
            return f"{seconds:.1f} сек"
        else:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes} мин {secs:.0f} сек"
    
    def create_progress_bar(self, percent, width=25):
        """Создает прогресс-бар"""
        filled = int(width * percent / 100)
        return "█" * filled + "░" * (width - filled)
    
    def ask_model(self, model_config, messages):
        """Запрос к модели"""
        try:
            start = time.time()
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_config["name"],
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 800,
                },
                timeout=model_config["timeout"]
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result["choices"][0]["message"]["content"],
                    "time": elapsed,
                    "desc": model_config["desc"]
                }
            else:
                return {"success": False, "time": elapsed, "desc": model_config["desc"]}
                    
        except Exception as e:
            return {"success": False, "time": 0, "desc": model_config["desc"]}
    
    def get_response(self, user_id, message, chat_id=None, status_message_id=None):
        """Получение ответа с умным выбором моделей"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        # Определяем сложность вопроса
        complex_question = self.is_complex_question(message)
        
        # Системный промпт
        system_prompt = "Ты — аналитическая нейросеть. Отвечай точно и по существу. Приоритет операций: сначала умножение/деление."
        if complex_question:
            system_prompt += " Вопрос сложный, требуется развернутый ответ."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        start_time = time.time()
        
        # Выбираем модели в зависимости от сложности
        if complex_question:
            # Для сложных вопросов: быстрые (2) + мощные (6)
            models_to_use = self.fast_models[:2] + self.powerful_models[:6]
            model_type = "🧠 МОЩНЫЕ"
        else:
            # Для простых вопросов: только быстрые (6)
            models_to_use = self.fast_models[:6]
            model_type = "⚡ БЫСТРЫЕ"
        
        total_models = len(models_to_use)
        processed = 0
        responses = []
        
        logging.info(f"📝 Запрос: {message[:50]}...")
        logging.info(f"🤖 Тип: {model_type}, моделей: {total_models}")
        
        # Опрашиваем модели
        for i, model in enumerate(models_to_use):
            processed += 1
            
            result = self.ask_model(model, messages)
            
            if result.get("success"):
                responses.append({
                    "answer": result["answer"],
                    "model": result["desc"],
                    "time": result["time"]
                })
            
            # Обновляем прогресс
            if chat_id and status_message_id and i % 2 == 0:
                elapsed = time.time() - start_time
                percent = (processed / total_models) * 100
                avg_time = elapsed / processed if processed > 0 else 0
                
                bar = self.create_progress_bar(percent)
                status_text = f"""
🔬 **{'СЛОЖНЫЙ ВОПРОС' if complex_question else 'ПРОСТОЙ ВОПРОС'}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **ПРОГРЕСС:** [{bar}] {percent:.0f}% ({processed}/{total_models})
⏱️ **ПРОШЛО:** {self.format_time(elapsed)}
⚡ **ТИП МОДЕЛЕЙ:** {model_type}

✅ **НАЙДЕНО РЕШЕНИЙ:** {len(responses)}
⏳ **ОСТАЛОСЬ:** {total_models - processed}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ **СРЕДНЕЕ ВРЕМЯ:** {avg_time:.1f} сек
"""
                try:
                    self.bot_instance.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_message_id,
                        text=status_text
                    )
                except:
                    pass
        
        if not responses:
            return "Ошибка: нейросети временно недоступны"
        
        # Формируем финальный ответ
        elapsed = time.time() - start_time
        
        # Берем первый успешный ответ (самый быстрый)
        final_answer = responses[0]["answer"]
        
        # Добавляем статистику
        final_answer += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        final_answer += f"📊 **Статистика:**\n"
        final_answer += f"• Тип: {'🧠 сложный' if complex_question else '⚡ простой'}\n"
        final_answer += f"• Моделей: {len(responses)}/{total_models}\n"
        final_answer += f"• Время: {elapsed:.1f} сек\n"
        
        # Добавляем кто ответил первым
        final_answer += f"• Первый ответ: {responses[0]['model']} ({responses[0]['time']:.1f} сек)"
        
        return final_answer
    
    def analyze_photo(self, photo_bytes, user_id, chat_id=None, status_message_id=None):
        """Анализ фото (всегда vision-модели)"""
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {
                    "role": "system",
                    "content": "Найди на фото все математические примеры и реши их подробно."
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
            
            start_time = time.time()
            total = len(self.vision_models)
            processed = 0
            responses = []
            
            for i, model in enumerate(self.vision_models):
                processed += 1
                result = self.ask_model(model, messages)
                
                if result.get("success"):
                    responses.append({
                        "answer": result["answer"],
                        "model": result["desc"],
                        "time": result["time"]
                    })
                
                # Обновляем прогресс
                if chat_id and status_message_id and i % 1 == 0:
                    elapsed = time.time() - start_time
                    percent = (processed / total) * 100
                    bar = self.create_progress_bar(percent)
                    
                    status_text = f"""
📸 **VISION АНАЛИЗ ФОТО**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **ПРОГРЕСС:** [{bar}] {percent:.0f}% ({processed}/{total})
⏱️ **ПРОШЛО:** {self.format_time(elapsed)}
✅ **НАЙДЕНО РЕШЕНИЙ:** {len(responses)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ **ОБРАБОТКА ИЗОБРАЖЕНИЯ...**
"""
                    try:
                        self.bot_instance.edit_message_text(
                            chat_id=chat_id,
                            message_id=status_message_id,
                            text=status_text
                        )
                    except:
                        pass
            
            if not responses:
                return "Не удалось проанализировать фото"
            
            elapsed = time.time() - start_time
            final = responses[0]["answer"]
            final += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
            final += f"📸 **Vision анализ:**\n"
            final += f"• Моделей: {len(responses)}/{total}\n"
            final += f"• Время: {elapsed:.1f} сек\n"
            final += f"• Первый ответ: {responses[0]['model']}"
            
            return final
            
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
