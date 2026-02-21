"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ
С улучшенной обработкой таймаутов и ошибок
"""

import os
import base64
import requests
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SuperBot:
    def __init__(self):
        logging.info("=" * 80)
        logging.info("ЗАПУСК АНАЛИТИЧЕСКОЙ СИСТЕМЫ")
        logging.info("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if not self.api_key:
            logging.error("❌ API ключ не найден!")
        
        # Модели с очень короткими таймаутами
        self.models = [
            # Vision модели
            {"name": "google/gemini-2.0-flash-exp:free", "vision": True, "timeout": 5, "desc": "Gemini"},
            {"name": "nvidia/nemotron-nano-2-vl:free", "vision": True, "timeout": 6, "desc": "NVIDIA VL"},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "vision": True, "timeout": 7, "desc": "Qwen3 VL"},
            
            # Сверхбыстрые модели
            {"name": "stepfun/step-3.5-flash:free", "vision": False, "timeout": 4, "desc": "Step 3.5"},
            {"name": "arcee-ai/trinity-mini:free", "vision": False, "timeout": 4, "desc": "Trinity Mini"},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "vision": False, "timeout": 4, "desc": "LFM2.5"},
            {"name": "mistralai/mistral-7b-v3:free", "vision": False, "timeout": 4, "desc": "Mistral 7B"},
            
            # Универсальные модели
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "vision": False, "timeout": 6, "desc": "Llama 3.3"},
            {"name": "arcee-ai/trinity-large-preview:free", "vision": False, "timeout": 7, "desc": "Trinity Large"},
            {"name": "openai/gpt-oss-120b:free", "vision": False, "timeout": 6, "desc": "GPT-OSS"},
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        logging.info(f"📊 Загружено моделей: {len(self.models)}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
    
    def ask_model(self, model_config, messages):
        """Запрос к модели с жестким таймаутом"""
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
                    "max_tokens": 400,
                },
                timeout=model_config["timeout"]  # Критично важно!
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result["choices"][0]["message"]["content"],
                    "time": elapsed
                }
            else:
                # Обработка специфических кодов ошибок OpenRouter [citation:1]
                error_data = response.json()
                error_code = error_data.get('error', {}).get('code', response.status_code)
                
                if error_code == 402:
                    logging.error("❌ Недостаточно кредитов OpenRouter")
                    return {"success": False, "error": "no_credits"}
                elif error_code == 429:
                    logging.warning("⚠️ Rate limit exceeded")
                    return {"success": False, "error": "rate_limit"}
                elif error_code == 408:
                    logging.warning("⏱️ Request timeout")
                    return {"success": False, "error": "timeout"}
                else:
                    return {"success": False}
                    
        except requests.exceptions.Timeout:
            logging.debug(f"⏱️ Таймаут {model_config['timeout']}с для {model_config['desc']}")
            return {"success": False, "error": "timeout"}
        except Exception as e:
            logging.debug(f"❌ Ошибка {model_config['desc']}: {str(e)[:50]}")
            return {"success": False}
    
    def get_response(self, user_id, message):
        """Быстрый опрос моделей с жесткими лимитами"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — аналитическая нейросеть. Отвечай кратко и точно. Приоритет операций: сначала умножение/деление."},
            {"role": "user", "content": message}
        ]
        
        logging.info(f"📝 Запрос: {message[:50]}...")
        
        # Берем только самые быстрые модели (первые 5)
        fast_models = sorted(self.models, key=lambda x: x["timeout"])[:5]
        responses = []
        credits_error = False
        
        for model in fast_models:
            logging.info(f"  ⚡ {model['desc']}...", end="")
            result = self.ask_model(model, messages)
            
            if result.get("success"):
                responses.append(result["answer"])
                logging.info(f" ✅ ({result.get('time', 0):.1f}с)")
            elif result.get("error") == "no_credits":
                credits_error = True
                logging.info(f" ❌ нет кредитов")
                break  # Дальше пробовать бессмысленно
            else:
                logging.info(f" ❌")
        
        if credits_error:
            return "Ошибка: закончились кредиты OpenRouter. Пополните баланс на openrouter.ai/settings/credits"
        
        if not responses:
            return "Ошибка: нейросети временно недоступны. Попробуйте через минуту."
        
        # Берем первый ответ (самый быстрый)
        return responses[0]
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализ фото с таймаутом"""
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
            
            # Берем только vision-модели
            for model in self.vision_models[:2]:  # Первые 2
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
