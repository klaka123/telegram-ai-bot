"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ
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
        
        if not self.api_key:
            logging.error("❌ API ключ не найден!")
        
        # Модели с короткими таймаутами
        self.models = [
            {"name": "google/gemini-2.0-flash-exp:free", "vision": True, "timeout": 5, "desc": "Gemini"},
            {"name": "nvidia/nemotron-nano-2-vl:free", "vision": True, "timeout": 6, "desc": "NVIDIA VL"},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "vision": True, "timeout": 7, "desc": "Qwen3 VL"},
            {"name": "stepfun/step-3.5-flash:free", "vision": False, "timeout": 4, "desc": "Step 3.5"},
            {"name": "arcee-ai/trinity-mini:free", "vision": False, "timeout": 4, "desc": "Trinity Mini"},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "vision": False, "timeout": 4, "desc": "LFM2.5"},
            {"name": "mistralai/mistral-7b-v3:free", "vision": False, "timeout": 4, "desc": "Mistral 7B"},
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "vision": False, "timeout": 6, "desc": "Llama 3.3"},
            {"name": "arcee-ai/trinity-large-preview:free", "vision": False, "timeout": 7, "desc": "Trinity Large"},
            {"name": "openai/gpt-oss-120b:free", "vision": False, "timeout": 6, "desc": "GPT-OSS"},
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        logging.info(f"📊 Загружено моделей: {len(self.models)}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
    
    def ask_model(self, model_config, messages):
        """Запрос к модели с таймаутом"""
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
                    "max_tokens": 400,
                },
                timeout=model_config["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result["choices"][0]["message"]["content"]
                }
            else:
                return {"success": False}
                    
        except requests.exceptions.Timeout:
            return {"success": False}
        except Exception:
            return {"success": False}
    
    def get_response(self, user_id, message):
        """Получение ответа"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        messages = [
            {"role": "system", "content": "Ты — аналитическая нейросеть. Отвечай кратко и точно. Приоритет операций: сначала умножение/деление."},
            {"role": "user", "content": message}
        ]
        
        logging.info(f"📝 Запрос: {message[:50]}...")
        
        # Быстрые модели
        fast_models = sorted(self.models, key=lambda x: x["timeout"])[:5]
        responses = []
        
        for model in fast_models:
            logging.info(f"⚡ Пробую {model['desc']}...")
            result = self.ask_model(model, messages)
            
            if result.get("success"):
                responses.append(result["answer"])
                logging.info(f"✅ {model['desc']} ответил")
                break  # Берем первый ответ - так быстрее всего
        
        if not responses:
            return "Ошибка: нейросети временно недоступны"
        
        return responses[0]
    
    def analyze_photo(self, photo_bytes, user_id):
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
            
            for model in self.vision_models[:2]:
                result = self.ask_model(model, messages)
                if result.get("success"):
                    return result["answer"]
            
            return "Не удалось проанализировать фото"
            
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
