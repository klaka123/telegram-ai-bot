"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ
Февраль 2026 — Максимальная скорость, Vision для фото
"""

import os
import base64
import requests
import time
import logging
from collections import Counter
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SuperBot:
    def __init__(self):
        logging.info("=" * 80)
        logging.info("АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ")
        logging.info("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            logging.info(f"✅ API КЛЮЧ: найден (длина: {len(self.api_key)})")
        else:
            logging.error("❌ ОШИБКА: ключ не найден")
        
        # ⭐ 30+ МОДЕЛЕЙ С МИНИМАЛЬНЫМИ ТАЙМАУТАМИ ⭐
        self.models = [
            # === VISION МОДЕЛИ (ДЛЯ ФОТО) — самые быстрые ===
            {"name": "google/gemini-2.0-flash-exp:free", "vision": True, "timeout": 4, "desc": "Gemini 2.0 Flash"},
            {"name": "nvidia/nemotron-nano-2-vl:free", "vision": True, "timeout": 5, "desc": "NVIDIA Nemotron VL"},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "vision": True, "timeout": 6, "desc": "Qwen3 VL 235B"},
            {"name": "google/gemini-3-flash-preview:free", "vision": True, "timeout": 5, "desc": "Gemini 3 Flash"},
            {"name": "moonshotai/kimi-vl-a3b-thinking:free", "vision": True, "timeout": 5, "desc": "Kimi VL A3B"},
            {"name": "nvidia/nemotron-nano-9b-v2:free", "vision": True, "timeout": 6, "desc": "Nemotron Nano 9B"},
            
            # === СВЕРХБЫСТРЫЕ МОДЕЛИ ===
            {"name": "stepfun/step-3.5-flash:free", "vision": False, "timeout": 3, "desc": "Step 3.5 Flash"},
            {"name": "z-ai/glm-4.5-air:free", "vision": False, "timeout": 4, "desc": "GLM-4.5-Air"},
            {"name": "arcee-ai/trinity-mini:free", "vision": False, "timeout": 3, "desc": "Trinity Mini"},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "vision": False, "timeout": 3, "desc": "LFM2.5 Thinking"},
            {"name": "liquidai/lfm2.5-1.2b-instruct:free", "vision": False, "timeout": 3, "desc": "LFM2.5 Instruct"},
            
            # === НОВЫЕ МОЩНЫЕ МОДЕЛИ ===
            {"name": "openrouter/pony-alpha:free", "vision": False, "timeout": 6, "desc": "Pony Alpha (GLM-5)"},
            {"name": "openrouter/aurora-alpha:free", "vision": False, "timeout": 5, "desc": "Aurora Alpha"},
            {"name": "deepseek/deepseek-r1:free", "vision": False, "timeout": 6, "desc": "DeepSeek R1"},
            {"name": "qwen/qwen3-235b-a22b-thinking:free", "vision": False, "timeout": 6, "desc": "Qwen3 235B"},
            
            # === УНИВЕРСАЛЬНЫЕ МОДЕЛИ ===
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "vision": False, "timeout": 5, "desc": "Llama 3.3 70B"},
            {"name": "arcee-ai/trinity-large-preview:free", "vision": False, "timeout": 6, "desc": "Trinity Large"},
            {"name": "openai/gpt-oss-120b:free", "vision": False, "timeout": 5, "desc": "GPT-OSS 120B"},
            {"name": "openai/gpt-oss-20b:free", "vision": False, "timeout": 4, "desc": "GPT-OSS 20B"},
            {"name": "upstage/solar-pro-3:free", "vision": False, "timeout": 5, "desc": "Solar Pro 3"},
            {"name": "nvidia/nemotron-3-nano-30b:free", "vision": False, "timeout": 5, "desc": "Nemotron 3 Nano"},
            {"name": "mistralai/devstral-2512:free", "vision": False, "timeout": 5, "desc": "Devstral 2"},
            {"name": "meta-llama/llama-3.1-405b:free", "vision": False, "timeout": 7, "desc": "Llama 3.1 405B"},
            
            # === ДОПОЛНИТЕЛЬНЫЕ МОДЕЛИ ===
            {"name": "google/gemma-3-27b:free", "vision": True, "timeout": 5, "desc": "Gemma 3 27B"},
            {"name": "google/gemma-3-12b:free", "vision": True, "timeout": 4, "desc": "Gemma 3 12B"},
            {"name": "xiaomi/mimo-v2-flash:free", "vision": False, "timeout": 5, "desc": "MiMo-V2-Flash"},
            {"name": "qwen/qwen3-coder-480b:free", "vision": False, "timeout": 6, "desc": "Qwen3 Coder"},
            {"name": "mistralai/mistral-7b-v3:free", "vision": False, "timeout": 3, "desc": "Mistral 7B v3"}
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        
        logging.info(f"\n📊 ВСЕГО МОДЕЛЕЙ: {len(self.models)}")
        logging.info(f"📸 VISION-МОДЕЛЕЙ: {len(self.vision_models)} (для фото)")
        logging.info(f"⚡ СВЕРХБЫСТРЫХ (<4с): {len([m for m in self.models if m['timeout'] <= 4])}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
        logging.info("🚀 СИСТЕМА ГОТОВА К РАБОТЕ")
        logging.info("=" * 80)
    
    def ask_model(self, model_config, messages):
        """Быстрый запрос к одной модели"""
        try:
            start = time.time()
            
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
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
                timeout=model_config["timeout"]
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result["choices"][0]["message"]["content"],
                    "time": elapsed
                }
            return {"success": False}
        except Exception as e:
            logging.debug(f"Модель {model_config['desc']} не ответила: {str(e)[:50]}")
            return {"success": False}
    
    def analyze_responses(self, question, responses):
        """Анализирует ответы и находит консенсус"""
        if not responses:
            return None
        
        if len(responses) == 1:
            return responses[0]
        
        # Собираем ответы для анализа
        answers_text = "\n\n".join([
            f"Ответ {i+1}:\n{r[:200]}..." for i, r in enumerate(responses[:5])
        ])
        
        analysis_prompt = f"""Вопрос: {question}

Получены следующие ответы от разных нейросетей:
{answers_text}

Проанализируй все ответы и сформируй единый итоговый ответ, который отражает общее мнение большинства. Ответ должен быть точным и полным."""

        analysis_messages = [
            {"role": "system", "content": "Ты анализируешь ответы нейросетей и находишь консенсус."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        # Используем Gemini как анализатор
        gemini = next((m for m in self.models if "gemini-2.0" in m["name"]), self.models[0])
        result = self.ask_model(gemini, analysis_messages)
        return result["answer"] if result["success"] else responses[0]
    
    def get_response(self, user_id, message):
        """Получение ответа от системы"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        # Системный промпт для всех моделей
        system_prompt = "Ты — аналитическая нейросеть. Отвечай кратко и точно. Приоритет операций: сначала умножение/деление, затем сложение/вычитание."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        logging.info(f"\n📝 ЗАПРОС: {message[:50]}...")
        logging.info(f"🔄 ОПРОС {len(self.models)} МОДЕЛЕЙ...")
        
        # Сначала пробуем сверхбыстрые модели
        fast_models = [m for m in self.models if m["timeout"] <= 4]
        responses = []
        models_responded = 0
        
        # Быстрый проход по сверхбыстрым моделям
        for model in fast_models[:10]:
            logging.info(f"  ⚡ {model['desc']}...", end="")
            result = self.ask_model(model, messages)
            if result["success"]:
                responses.append(result["answer"])
                models_responded += 1
                logging.info(f" ✅ ({result['time']:.1f}с)")
            else:
                logging.info(f" ❌")
        
        # Если мало ответов, добавляем остальные
        if models_responded < 3:
            other_models = [m for m in self.models if m not in fast_models][:5]
            for model in other_models:
                logging.info(f"  {model['desc']}...", end="")
                result = self.ask_model(model, messages)
                if result["success"]:
                    responses.append(result["answer"])
                    models_responded += 1
                    logging.info(f" ✅")
                else:
                    logging.info(f" ❌")
        
        logging.info(f"\n📊 ИТОГ: ответили {models_responded} моделей")
        
        if not responses:
            return "Ошибка: нейросети временно недоступны"
        
        # Анализируем консенсус
        final_answer = self.analyze_responses(message, responses)
        
        if models_responded > 1:
            return f"{final_answer}\n\n*Проанализировано {models_responded} нейросетями*"
        else:
            return final_answer
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализ фотографии (только vision-модели)"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {
                    "role": "system",
                    "content": "Найди на фото все математические примеры и реши их. Приоритет операций: умножение/деление перед сложением/вычитанием. Отвечай кратко и точно."
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
            
            logging.info(f"\n📸 АНАЛИЗ ФОТО: {len(self.vision_models)} vision-моделей")
            
            # Пробуем vision-модели по скорости
            vision_sorted = sorted(self.vision_models, key=lambda x: x["timeout"])
            
            for model in vision_sorted[:4]:
                logging.info(f"  {model['desc']}...", end="")
                result = self.ask_model(model, messages)
                if result["success"]:
                    logging.info(f" ✅")
                    return result["answer"]
                logging.info(f" ❌")
            
            return "Не удалось проанализировать фото"
            
        except Exception as e:
            return f"Ошибка анализа: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
