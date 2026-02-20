"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 20+ НЕЙРОСЕТЕЙ
Высокая скорость, консенсус большинства, без эмодзи
"""

import os
import base64
import requests
import time
from collections import Counter
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 80)
        print("АНАЛИТИЧЕСКАЯ СИСТЕМА — 20+ НЕЙРОСЕТЕЙ")
        print("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"API КЛЮЧ: найден")
        else:
            print("ОШИБКА: ключ не найден")
        
        # ⭐ 20+ МОДЕЛЕЙ С МИНИМАЛЬНЫМИ ТАЙМАУТАМИ ⭐
        self.models = [
            # Vision модели (для фото)
            {"name": "google/gemini-2.0-flash-exp:free", "vision": True, "timeout": 5, "desc": "Gemini 2.0"},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "vision": True, "timeout": 7, "desc": "Qwen3 VL"},
            {"name": "nvidia/nemotron-nano-2-vl:free", "vision": True, "timeout": 6, "desc": "NVIDIA VL"},
            
            # Сверхбыстрые модели
            {"name": "stepfun/step-3.5-flash:free", "vision": False, "timeout": 4, "desc": "Step 3.5"},
            {"name": "z-ai/glm-4.5-air:free", "vision": False, "timeout": 5, "desc": "GLM-4.5"},
            {"name": "arcee-ai/trinity-mini:free", "vision": False, "timeout": 4, "desc": "Trinity Mini"},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "vision": False, "timeout": 4, "desc": "LFM2.5"},
            
            # Универсальные модели
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "vision": False, "timeout": 6, "desc": "Llama 3.3"},
            {"name": "arcee-ai/trinity-large-preview:free", "vision": False, "timeout": 7, "desc": "Trinity Large"},
            {"name": "qwen/qwen3-235b-a22b-thinking:free", "vision": False, "timeout": 7, "desc": "Qwen3"},
            {"name": "openai/gpt-oss-120b:free", "vision": False, "timeout": 6, "desc": "GPT-OSS"},
            {"name": "deepseek/deepseek-r1:free", "vision": False, "timeout": 7, "desc": "DeepSeek R1"},
            {"name": "upstage/solar-pro-3:free", "vision": False, "timeout": 6, "desc": "Solar Pro"},
            {"name": "mistralai/devstral-2512:free", "vision": False, "timeout": 6, "desc": "Devstral"},
            {"name": "openrouter/aurora-alpha:free", "vision": False, "timeout": 6, "desc": "Aurora"},
            {"name": "openrouter/pony-alpha:free", "vision": False, "timeout": 6, "desc": "Pony"},
            {"name": "nvidia/nemotron-3-nano-30b:free", "vision": False, "timeout": 6, "desc": "Nemotron"},
            {"name": "liquidai/lfm2.5-1.2b-instruct:free", "vision": False, "timeout": 5, "desc": "LFM Instruct"}
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        print(f"МОДЕЛЕЙ ЗАГРУЖЕНО: {len(self.models)}")
        print("=" * 80)
        
        self.user_contexts = {}
        print("СИСТЕМА ГОТОВА К РАБОТЕ")
        print("=" * 80)
    
    def ask_model(self, model_config, messages):
        """Быстрый запрос к одной модели"""
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
                return result["choices"][0]["message"]["content"]
            return None
        except:
            return None
    
    def analyze_responses(self, question, responses):
        """Анализирует ответы и находит консенсус"""
        if not responses:
            return None
        
        if len(responses) == 1:
            return responses[0]
        
        # Собираем ответы для анализа
        answers_text = "\n\n".join([
            f"Ответ {i+1}:\n{r}" for i, r in enumerate(responses)
        ])
        
        analysis_prompt = f"""Вопрос: {question}

Получены следующие ответы от разных нейросетей:
{answers_text}

Проанализируй все ответы и сформируй единый итоговый ответ, который отражает общее мнение большинства. Ответ должен быть точным и полным."""

        analysis_messages = [
            {"role": "system", "content": "Ты анализируешь ответы нейросетей и находишь консенсус."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        # Используем Gemini как анализатор (самый быстрый)
        gemini = next(m for m in self.models if "gemini" in m["name"])
        return self.ask_model(gemini, analysis_messages) or responses[0]
    
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
        
        print(f"\nЗАПРОС: {message[:50]}...")
        print(f"ОПРОС {len(self.models)} МОДЕЛЕЙ...")
        
        # Собираем ответы (максимум 8-10 самых быстрых)
        responses = []
        models_tested = 0
        models_responded = 0
        
        for i, model in enumerate(self.models[:10]):  # Первые 10 самых быстрых
            print(f"  {i+1}. {model['desc']}...", end="")
            answer = self.ask_model(model, messages)
            models_tested += 1
            if answer:
                responses.append(answer)
                models_responded += 1
                print(f" OK")
            else:
                print(f" нет")
            time.sleep(0.1)  # Минимальная пауза
        
        print(f"\nИТОГ: опрошено {models_tested}, ответили {models_responded}")
        
        if not responses:
            return "Ошибка: ни одна нейросеть не ответила"
        
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
                    "content": "Найди на фото все математические примеры и реши их. Приоритет операций: умножение/деление перед сложением/вычитанием."
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
            
            print(f"\nАНАЛИЗ ФОТО: {len(self.vision_models)} vision-моделей")
            
            # Пробуем vision-модели
            for model in self.vision_models[:3]:  # Первые 3 vision
                print(f"  {model['desc']}...", end="")
                answer = self.ask_model(model, messages)
                if answer:
                    print(f" OK")
                    return answer
                print(f" нет")
            
            return "Не удалось проанализировать фото"
            
        except Exception as e:
            return f"Ошибка анализа: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
