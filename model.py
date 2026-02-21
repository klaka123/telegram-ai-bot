"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 31 НЕЙРОСЕТЬ
Максимальная скорость для простых вопросов
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
        logging.info("ЗАПУСК АНАЛИТИЧЕСКОЙ СИСТЕМЫ")
        logging.info("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        self.bot_instance = None
        
        if not self.api_key:
            logging.error("❌ API ключ не найден!")
        
        # === ⚡ СВЕРХБЫСТРЫЕ МОДЕЛИ (1-2 сек) ===
        self.fast_models = [
            {"name": "stepfun/step-3.5-flash:free", "timeout": 2, "desc": "Step 3.5 Flash"},
            {"name": "arcee-ai/trinity-mini:free", "timeout": 2, "desc": "Trinity Mini"},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "timeout": 2, "desc": "LFM2.5 Thinking"},
            {"name": "mistralai/mistral-7b-v3:free", "timeout": 2, "desc": "Mistral 7B v3"},
            {"name": "z-ai/glm-4.5-air:free", "timeout": 2, "desc": "GLM-4.5-Air"},
            {"name": "liquidai/lfm2.5-1.2b-instruct:free", "timeout": 2, "desc": "LFM2.5 Instruct"},
        ]
        
        # === 🧠 МОЩНЫЕ МОДЕЛИ (для сложных вопросов) ===
        self.powerful_models = [
            {"name": "google/gemini-2.0-flash-exp:free", "timeout": 8, "desc": "Gemini 2.0 Flash"},
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "timeout": 10, "desc": "Llama 3.3 70B"},
            {"name": "arcee-ai/trinity-large-preview:free", "timeout": 10, "desc": "Trinity Large"},
            {"name": "openai/gpt-oss-120b:free", "timeout": 8, "desc": "GPT-OSS 120B"},
            {"name": "deepseek/deepseek-r1:free", "timeout": 10, "desc": "DeepSeek R1"},
            {"name": "upstage/solar-pro-3:free", "timeout": 8, "desc": "Solar Pro 3"},
            {"name": "qwen/qwen3-235b-a22b-thinking:free", "timeout": 10, "desc": "Qwen3 235B"},
            {"name": "nvidia/nemotron-3-nano-30b:free", "timeout": 8, "desc": "Nemotron 3 Nano"},
            {"name": "mistralai/devstral-2512:free", "timeout": 6, "desc": "Devstral 2"},
            {"name": "openrouter/aurora-alpha:free", "timeout": 6, "desc": "Aurora Alpha"},
            {"name": "openrouter/pony-alpha:free", "timeout": 8, "desc": "Pony Alpha"},
            {"name": "xiaomi/mimo-v2-flash:free", "timeout": 6, "desc": "MiMo-V2-Flash"},
            {"name": "qwen/qwen3-coder-480b:free", "timeout": 10, "desc": "Qwen3 Coder"},
        ]
        
        # === 📸 VISION МОДЕЛИ ===
        self.vision_models = [
            {"name": "google/gemini-2.0-flash-exp:free", "timeout": 8, "desc": "Gemini 2.0 Flash"},
            {"name": "nvidia/nemotron-nano-2-vl:free", "timeout": 8, "desc": "NVIDIA Nemotron VL"},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "timeout": 10, "desc": "Qwen3 VL 235B"},
            {"name": "google/gemini-3-flash-preview:free", "timeout": 8, "desc": "Gemini 3 Flash"},
            {"name": "moonshotai/kimi-vl-a3b-thinking:free", "timeout": 6, "desc": "Kimi VL A3B"},
            {"name": "google/gemma-3-27b:free", "timeout": 8, "desc": "Gemma 3 27B"},
        ]
        
        logging.info(f"⚡ СВЕРХБЫСТРЫХ: {len(self.fast_models)}")
        logging.info(f"🧠 МОЩНЫХ: {len(self.powerful_models)}")
        logging.info(f"📸 VISION: {len(self.vision_models)}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
    
    def set_bot(self, bot):
        self.bot_instance = bot
    
    def is_complex_question(self, text):
        """Определяет сложность вопроса"""
        if len(text) > 150:
            return True
        
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
    
    def ask_model(self, model_config, messages):
        """Запрос к модели"""
        try:
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
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result["choices"][0]["message"]["content"],
                    "desc": model_config["desc"]
                }
            return {"success": False}
                    
        except Exception:
            return {"success": False}
    
    def update_progress(self, chat_id, message_id, current, total, model_type, responses_count):
        """Обновляет прогресс-бар"""
        if not self.bot_instance:
            return
        
        try:
            percent = int((current / total) * 100)
            bar_length = 20
            filled = int(bar_length * percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            status_text = f"""
🔬 **АНАЛИЗ {'СЛОЖНОГО' if model_type == '🧠' else 'ПРОСТОГО'} ЗАПРОСА**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **ПРОГРЕСС:** [{bar}] {percent}% ({current}/{total})
⚡ **ТИП МОДЕЛЕЙ:** {'🧠 МОЩНЫЕ' if model_type == '🧠' else '⚡ БЫСТРЫЕ'}
✅ **НАЙДЕНО РЕШЕНИЙ:** {responses_count}
"""
            self.bot_instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=status_text
            )
        except:
            pass
    
    def get_response(self, user_id, message, chat_id=None, status_message_id=None):
        """Получение ответа"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        # Определяем сложность
        complex_question = self.is_complex_question(message)
        
        # Системный промпт
        system_prompt = "Ты — аналитическая нейросеть. Отвечай точно и по существу. Приоритет операций: сначала умножение/деление."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Выбираем модели
        if complex_question:
            # Сложные: сначала быстрые (для скорости), потом мощные
            models_to_try = self.fast_models[:2] + self.powerful_models[:6]
            model_type = "🧠"
            type_name = "МОЩНЫЕ"
        else:
            # Простые: только сверхбыстрые
            models_to_try = self.fast_models[:3]
            model_type = "⚡"
            type_name = "БЫСТРЫЕ"
        
        total = len(models_to_try)
        processed = 0
        responses = []
        
        # Опрашиваем модели
        for i, model in enumerate(models_to_try):
            processed += 1
            
            # Обновляем прогресс
            if chat_id and status_message_id:
                self.update_progress(chat_id, status_message_id, processed, total, model_type, len(responses))
            
            # Запрашиваем модель
            result = self.ask_model(model, messages)
            
            if result.get("success"):
                responses.append({
                    "answer": result["answer"],
                    "model": result["desc"]
                })
                # Для простых вопросов берем первый ответ
                if not complex_question and len(responses) == 1:
                    # Удаляем статусное сообщение
                    if chat_id and status_message_id:
                        try:
                            self.bot_instance.delete_message(chat_id, status_message_id)
                        except:
                            pass
                    return responses[0]["answer"]
        
        # Для сложных вопросов ждем все ответы и берем лучший
        if responses:
            # Удаляем статусное сообщение
            if chat_id and status_message_id:
                try:
                    self.bot_instance.delete_message(chat_id, status_message_id)
                except:
                    pass
            return responses[0]["answer"]
        
        return "Ошибка: нейросети временно недоступны"
    
    def analyze_photo(self, photo_bytes, user_id, chat_id=None, status_message_id=None):
        """Анализ фото"""
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {
                    "role": "system",
                    "content": "Найди на фото все математические примеры и реши их."
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
            
            models_to_try = self.vision_models[:4]
            total = len(models_to_try)
            processed = 0
            responses = []
            
            for i, model in enumerate(models_to_try):
                processed += 1
                
                if chat_id and status_message_id:
                    percent = int((processed / total) * 100)
                    bar_length = 20
                    filled = int(bar_length * percent / 100)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    
                    status_text = f"""
📸 **АНАЛИЗ ФОТО**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **ПРОГРЕСС:** [{bar}] {percent}% ({processed}/{total})
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
                
                result = self.ask_model(model, messages)
                if result.get("success"):
                    responses.append(result["answer"])
            
            if chat_id and status_message_id:
                try:
                    self.bot_instance.delete_message(chat_id, status_message_id)
                except:
                    pass
            
            if responses:
                return responses[0]
            return "Не удалось проанализировать фото"
            
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
