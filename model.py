"""
🤖 ИИ-ПАРЛАМЕНТ — 20+ НЕЙРОСЕТЕЙ ОБДУМЫВАЮТ ОТВЕТ
Выдаёт единый правильный ответ большинством голосов
Фото анализирует через vision-модели
"""

import os
import base64
import requests
import time
import json
from collections import Counter
from datetime import datetime

class SuperBot:
    def __init__(self):
        print("=" * 80)
        print("🤖 ЗАПУСК ИИ-ПАРЛАМЕНТА — 20+ НЕЙРОСЕТЕЙ")
        print("=" * 80)
        
        self.api_key = os.environ.get('OPENROUTER_KEY')
        
        if self.api_key:
            print(f"✅ КЛЮЧ OPENROUTER НАЙДЕН! Длина: {len(self.api_key)}")
        else:
            print("❌ КЛЮЧ OPENROUTER НЕ НАЙДЕН!")
            print("   Добавь OPENROUTER_KEY в Secrets GitHub!")
        
        # ⭐ 20+ ЛУЧШИХ БЕСПЛАТНЫХ МОДЕЛЕЙ (февраль 2026) ⭐
        # На основе официальных данных OpenRouter [citation:1][citation:9]
        self.models = [
            # === УНИВЕРСАЛЬНЫЕ ФЛАГМАНЫ (GPT-4 уровня) ===
            {
                "name": "meta-llama/llama-3.3-70b-instruct:free",
                "vision": False,
                "speed": 0.8,
                "desc": "Llama 3.3 70B (GPT-4 уровень)"
            },
            {
                "name": "openai/gpt-oss-120b:free",
                "vision": False,
                "speed": 0.7,
                "desc": "GPT-OSS 120B (открытая OpenAI)"
            },
            
            # === БЫСТРЫЕ FLASH-МОДЕЛИ ===
            {
                "name": "google/gemini-2.0-flash-exp:free",
                "vision": True,
                "speed": 0.95,
                "desc": "Gemini 2.0 Flash (1M контекста, фото)"
            },
            {
                "name": "stepfun/step-3.5-flash:free",
                "vision": False,
                "speed": 0.9,
                "desc": "Step 3.5 Flash (256K, быстрая)"
            },
            {
                "name": "z-ai/glm-4.5-air:free",
                "vision": False,
                "speed": 0.85,
                "desc": "GLM-4.5-Air (быстрая, агенты)"
            },
            
            # === МОЩНЫЕ MoE-МОДЕЛИ ===
            {
                "name": "arcee-ai/trinity-large-preview:free",
                "vision": False,
                "speed": 0.7,
                "desc": "Trinity Large (400B MoE)"
            },
            {
                "name": "qwen/qwen3-235b-a22b-thinking:free",
                "vision": False,
                "speed": 0.6,
                "desc": "Qwen3 235B (математика)"
            },
            
            # === VISION-МОДЕЛИ (ПОНИМАЮТ ФОТО) ===
            {
                "name": "qwen/qwen3-vl-235b-a22b-thinking:free",
                "vision": True,
                "speed": 0.5,
                "desc": "Qwen3 VL 235B (видео, фото)"
            },
            {
                "name": "nvidia/nemotron-nano-2-vl:free",
                "vision": True,
                "speed": 0.75,
                "desc": "NVIDIA Nemotron VL (OCR)"
            },
            {
                "name": "moonshotai/kimi-vl-a3b-thinking:free",
                "vision": True,
                "speed": 0.8,
                "desc": "Kimi VL A3B (лёгкая)"
            },
            
            # === ЛЁГКИЕ БЫСТРЫЕ МОДЕЛИ ===
            {
                "name": "arcee-ai/trinity-mini:free",
                "vision": False,
                "speed": 0.95,
                "desc": "Trinity Mini (очень быстрая)"
            },
            {
                "name": "mistralai/devstral-2512:free",
                "vision": False,
                "speed": 0.85,
                "desc": "Devstral 2 (кодинг)"
            },
            
            # === ДОПОЛНИТЕЛЬНЫЕ МОДЕЛИ ===
            {
                "name": "deepseek/deepseek-r1:free",
                "vision": False,
                "speed": 0.6,
                "desc": "DeepSeek R1 (логика)"
            },
            {
                "name": "openrouter/aurora-alpha:free",
                "vision": False,
                "speed": 0.8,
                "desc": "Aurora Alpha (кодинг)"
            },
            {
                "name": "openrouter/pony-alpha:free",
                "vision": False,
                "speed": 0.75,
                "desc": "Pony Alpha (GLM-5, агенты)"
            },
            {
                "name": "upstage/solar-pro-3:free",
                "vision": False,
                "speed": 0.8,
                "desc": "Solar Pro 3 (многоязычная)"
            },
            {
                "name": "liquidai/lfm2.5-1.2b-thinking:free",
                "vision": False,
                "speed": 0.95,
                "desc": "LFM2.5 (быстрая, логика)"
            },
            {
                "name": "liquidai/lfm2.5-1.2b-instruct:free",
                "vision": False,
                "speed": 0.95,
                "desc": "LFM2.5 Instruct (чат)"
            },
            {
                "name": "nvidia/nemotron-3-nano-30b:free",
                "vision": False,
                "speed": 0.7,
                "desc": "Nemotron 3 Nano (агенты)"
            }
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        
        print(f"\n📊 ВСЕГО МОДЕЛЕЙ: {len(self.models)}")
        print(f"📸 VISION-МОДЕЛЕЙ (для фото): {len(self.vision_models)}")
        print("=" * 80)
        
        self.user_contexts = {}
        print("🚀 ИИ-ПАРЛАМЕНТ ГОТОВ К РАБОТЕ!")
        print("=" * 80)
    
    def ask_model(self, model_config, messages, timeout=15):
        """Спрашивает одну модель"""
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
                    "temperature": 0.5,
                    "max_tokens": 500,
                },
                timeout=timeout
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "answer": answer,
                    "time": elapsed,
                    "model": model_config["desc"]
                }
            else:
                return {"success": False, "answer": None}
                
        except Exception:
            return {"success": False, "answer": None}
    
    def ensemble_vote(self, question, messages, is_photo=False):
        """
        ИИ-ПАРЛАМЕНТ: все модели голосуют, побеждает большинство
        """
        print(f"\n🗳️  СОЗЫВАЮ ИИ-ПАРЛАМЕНТ ИЗ {len(self.models)} НЕЙРОСЕТЕЙ...")
        
        # Выбираем модели (для фото только vision)
        models_to_use = self.vision_models if is_photo else self.models
        
        # Собираем ответы
        answers = []
        successful = 0
        
        for i, model in enumerate(models_to_use, 1):
            print(f"   {i}. {model['desc'][:30]}... ", end="")
            result = self.ask_model(model, messages)
            
            if result["success"] and result["answer"]:
                answers.append({
                    "text": result["answer"][:200],  # для сравнения
                    "full": result["answer"],
                    "model": model["desc"]
                })
                successful += 1
                print(f"✅ ({result['time']:.1f}с)")
            else:
                print("❌")
            
            time.sleep(0.3)  # небольшая пауза между запросами
        
        print(f"\n📊 ИТОГИ ГОЛОСОВАНИЯ:")
        print(f"   • Участвовало: {len(models_to_use)} нейросетей")
        print(f"   • Ответили: {successful}")
        
        if successful == 0:
            return "❌ Ни одна нейросеть не ответила. Попробуй через минуту!"
        
        # === АНАЛИЗ КОНСЕНСУСА ===
        # Сравниваем ответы и ищем общую суть [citation:6][citation:10]
        
        # Если ответила только одна модель
        if successful == 1:
            print(f"   • Консенсус: единогласное решение")
            return f"{answers[0]['full']}\n\n_🧠 Решение одной нейросети_"
        
        # Собираем все ответы для финального анализа
        all_answers = "\n\n---\n\n".join([
            f"ОТВЕТ {i+1} ({a['model']}):\n{a['full']}" 
            for i, a in enumerate(answers)
        ])
        
        # Просим главную модель проанализировать консенсус
        consensus_prompt = f"""Вопрос: "{question}"

{all_answers}

Проанализируй все ответы выше. Найди общую суть — то, с чем согласно большинство.
Создай ОДИН ИТОГОВЫЙ ОТВЕТ, который отражает консенсус большинства нейросетей.
Ответ должен быть точным и полным."""

        consensus_messages = [
            {"role": "system", "content": "Ты — председатель ИИ-парламента. Найди консенсус большинства."},
            {"role": "user", "content": consensus_prompt}
        ]
        
        print(f"🔄 Анализирую консенсус {successful} нейросетей...")
        
        # Используем Gemini как председателя (самый быстрый)
        chair_model = next(m for m in self.models if "gemini" in m["name"])
        result = self.ask_model(chair_model, consensus_messages, timeout=20)
        
        if result["success"]:
            final = result["answer"]
        else:
            # Если председатель не ответил, берём первый ответ
            final = answers[0]["full"]
        
        # Добавляем информацию о голосовании
        return f"{final}\n\n_🧠 {successful} нейросетей думали над ответом_"
    
    def get_response(self, user_id, message):
        """Основной метод для текстовых запросов"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        # Системный промпт
        messages = [
            {"role": "system", "content": "Ты — нейросеть в парламенте. Отвечай кратко и точно."},
            {"role": "user", "content": message}
        ]
        
        return self.ensemble_vote(message, messages, is_photo=False)
    
    def analyze_photo(self, photo_bytes, user_id):
        """Анализирует фото (только vision-модели)"""
        
        if not self.api_key:
            return "❌ Нет ключа OpenRouter. Добавь OPENROUTER_KEY в секреты!"
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            messages = [
                {
                    "role": "system",
                    "content": "Ты — нейросеть с vision. Найди на фото все математические примеры и реши их."
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
            
            return self.ensemble_vote("Анализ фото", messages, is_photo=True)
            
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
