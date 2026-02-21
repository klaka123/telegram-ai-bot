"""
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ
Детальный прогресс с процентами и временем
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
        
        # 30+ МОДЕЛЕЙ
        self.models = [
            # Vision модели
            {"name": "google/gemini-2.0-flash-exp:free", "vision": True, "timeout": 5, "desc": "Gemini 2.0 Flash", "speed": 0.95},
            {"name": "nvidia/nemotron-nano-2-vl:free", "vision": True, "timeout": 6, "desc": "NVIDIA Nemotron VL", "speed": 0.85},
            {"name": "qwen/qwen3-vl-235b-a22b-thinking:free", "vision": True, "timeout": 7, "desc": "Qwen3 VL 235B", "speed": 0.8},
            {"name": "google/gemini-3-flash-preview:free", "vision": True, "timeout": 5, "desc": "Gemini 3 Flash", "speed": 0.92},
            {"name": "moonshotai/kimi-vl-a3b-thinking:free", "vision": True, "timeout": 5, "desc": "Kimi VL A3B", "speed": 0.88},
            
            # Сверхбыстрые модели
            {"name": "stepfun/step-3.5-flash:free", "vision": False, "timeout": 4, "desc": "Step 3.5 Flash", "speed": 0.98},
            {"name": "arcee-ai/trinity-mini:free", "vision": False, "timeout": 4, "desc": "Trinity Mini", "speed": 0.97},
            {"name": "liquidai/lfm2.5-1.2b-thinking:free", "vision": False, "timeout": 4, "desc": "LFM2.5 Thinking", "speed": 0.96},
            {"name": "mistralai/mistral-7b-v3:free", "vision": False, "timeout": 4, "desc": "Mistral 7B v3", "speed": 0.94},
            {"name": "z-ai/glm-4.5-air:free", "vision": False, "timeout": 4, "desc": "GLM-4.5-Air", "speed": 0.93},
            
            # Универсальные модели
            {"name": "meta-llama/llama-3.3-70b-instruct:free", "vision": False, "timeout": 6, "desc": "Llama 3.3 70B", "speed": 0.85},
            {"name": "arcee-ai/trinity-large-preview:free", "vision": False, "timeout": 7, "desc": "Trinity Large", "speed": 0.82},
            {"name": "openai/gpt-oss-120b:free", "vision": False, "timeout": 6, "desc": "GPT-OSS 120B", "speed": 0.83},
            {"name": "deepseek/deepseek-r1:free", "vision": False, "timeout": 7, "desc": "DeepSeek R1", "speed": 0.81},
            {"name": "upstage/solar-pro-3:free", "vision": False, "timeout": 6, "desc": "Solar Pro 3", "speed": 0.84},
            {"name": "qwen/qwen3-235b-a22b-thinking:free", "vision": False, "timeout": 7, "desc": "Qwen3 235B", "speed": 0.8},
            {"name": "nvidia/nemotron-3-nano-30b:free", "vision": False, "timeout": 6, "desc": "Nemotron 3 Nano", "speed": 0.82},
            {"name": "mistralai/devstral-2512:free", "vision": False, "timeout": 5, "desc": "Devstral 2", "speed": 0.86},
            {"name": "openrouter/aurora-alpha:free", "vision": False, "timeout": 5, "desc": "Aurora Alpha", "speed": 0.87},
            {"name": "openrouter/pony-alpha:free", "vision": False, "timeout": 6, "desc": "Pony Alpha", "speed": 0.84},
            {"name": "google/gemma-3-27b:free", "vision": True, "timeout": 6, "desc": "Gemma 3 27B", "speed": 0.85},
            {"name": "xiaomi/mimo-v2-flash:free", "vision": False, "timeout": 5, "desc": "MiMo-V2-Flash", "speed": 0.86},
            {"name": "liquidai/lfm2.5-1.2b-instruct:free", "vision": False, "timeout": 4, "desc": "LFM2.5 Instruct", "speed": 0.95},
        ]
        
        self.vision_models = [m for m in self.models if m["vision"]]
        logging.info(f"📊 Загружено моделей: {len(self.models)}")
        logging.info(f"📸 Vision моделей: {len(self.vision_models)}")
        logging.info("=" * 80)
        
        self.user_contexts = {}
    
    def set_bot(self, bot):
        """Устанавливает экземпляр бота"""
        self.bot_instance = bot
    
    def format_time(self, seconds):
        """Форматирует время в читаемый вид"""
        if seconds < 60:
            return f"{seconds:.1f} сек"
        else:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes} мин {secs:.0f} сек"
    
    def create_progress_bar(self, percent, width=30):
        """Создает красивый прогресс-бар"""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    def update_status(self, chat_id, message_id, stats):
        """Обновляет статусное сообщение с детальным прогрессом"""
        if not self.bot_instance:
            return
        
        try:
            # Формируем заголовок
            if stats.get('is_photo', False):
                title = "📸 АНАЛИЗ ФОТО — VISION НЕЙРОСЕТИ"
            else:
                title = "🔬 АНАЛИЗ ЗАПРОСА — 30+ НЕЙРОСЕТЕЙ"
            
            # Прогресс-бар с процентами
            percent = stats['percent']
            bar = self.create_progress_bar(percent)
            
            # Время
            elapsed = stats['elapsed']
            remaining = stats.get('remaining', 0)
            
            # Статистика ответов
            responded = len(stats['responses'])
            total = stats['total']
            waiting = total - stats['processed']
            
            # Список самых быстрых
            fast_list = ""
            if stats.get('fast_responses'):
                fast_list = "\n⚡ **САМЫЕ БЫСТРЫЕ:**\n"
                for resp in stats['fast_responses'][:5]:  # Топ-5
                    check = "✅" if resp['success'] else "⏳"
                    fast_list += f"{check} {resp['desc']}"
                    if resp.get('time'):
                        fast_list += f" ({resp['time']:.1f} сек)"
                    fast_list += "\n"
            
            # Формируем полное сообщение
            status_text = f"""
{title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **ПРОГРЕСС:** [{bar}] {percent:.1f}% ({stats['processed']}/{total})
⏱️ **ПРОШЛО:** {self.format_time(elapsed)} | **ОСТАЛОСЬ:** ~{self.format_time(remaining)}

🤖 **ОТВЕТИЛИ:** {responded} нейросетей
⏳ **ЕЩЁ ДУМАЮТ:** {waiting} нейросетей
{fast_list}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ **ОПРОШЕНО:** {stats['processed']} из {total}
⏱️ **СРЕДНЕЕ ВРЕМЯ:** {stats.get('avg_time', 0):.1f} сек на модель
            """
            
            self.bot_instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=status_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logging.debug(f"Ошибка обновления статуса: {e}")
    
    def ask_model(self, model_config, messages):
        """Запрос к модели с замером времени"""
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
                return {
                    "success": False,
                    "time": elapsed,
                    "desc": model_config["desc"]
                }
                    
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "time": model_config["timeout"],
                "desc": model_config["desc"],
                "timeout": True
            }
        except Exception as e:
            return {
                "success": False,
                "time": 0,
                "desc": model_config["desc"]
            }
    
    def get_response(self, user_id, message, chat_id=None, status_message_id=None):
        """Получение ответа с детальным прогрессом"""
        
        if not self.api_key:
            return "Ошибка: не найден API ключ OpenRouter"
        
        messages = [
            {"role": "system", "content": "Ты — аналитическая нейросеть. Отвечай кратко и точно."},
            {"role": "user", "content": message}
        ]
        
        start_time = time.time()
        
        # Берем все модели
        all_models = self.models[:15]  # Первые 15 для скорости
        total_models = len(all_models)
        processed = 0
        responses = []
        fast_responses = []
        
        for i, model in enumerate(all_models):
            processed += 1
            
            # Запрашиваем модель
            result = self.ask_model(model, messages)
            
            if result.get("success"):
                responses.append(result["answer"])
                fast_responses.append({
                    "desc": result["desc"],
                    "time": result["time"],
                    "success": True
                })
            else:
                fast_responses.append({
                    "desc": result["desc"],
                    "time": result.get("time", 0),
                    "success": False
                })
            
            # Рассчитываем статистику
            elapsed = time.time() - start_time
            percent = (processed / total_models) * 100
            
            # Прогнозируем оставшееся время
            avg_time = elapsed / processed if processed > 0 else 0
            remaining = avg_time * (total_models - processed)
            
            # Обновляем статус
            if chat_id and status_message_id and i % 2 == 0:
                stats = {
                    'processed': processed,
                    'total': total_models,
                    'percent': percent,
                    'elapsed': elapsed,
                    'remaining': remaining,
                    'responses': responses,
                    'fast_responses': fast_responses,
                    'avg_time': avg_time,
                    'is_photo': False
                }
                self.update_status(chat_id, status_message_id, stats)
        
        # Финальное обновление
        if chat_id and status_message_id:
            elapsed = time.time() - start_time
            stats = {
                'processed': total_models,
                'total': total_models,
                'percent': 100,
                'elapsed': elapsed,
                'remaining': 0,
                'responses': responses,
                'fast_responses': fast_responses,
                'avg_time': elapsed / total_models,
                'is_photo': False
            }
            self.update_status(chat_id, status_message_id, stats)
        
        if not responses:
            return "Ошибка: нейросети временно недоступны"
        
        # Формируем финальный ответ
        final_response = responses[0]  # Берем первый ответ
        final_response += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        final_response += f"📊 **Статистика:** опрошено {total_models} нейросетей, "
        final_response += f"ответили {len(responses)} за {elapsed:.1f} сек"
        
        return final_response
    
    def analyze_photo(self, photo_bytes, user_id, chat_id=None, status_message_id=None):
        """Анализ фото с детальным прогрессом"""
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
            
            start_time = time.time()
            
            # Vision модели
            vision_list = self.vision_models[:8]
            total = len(vision_list)
            processed = 0
            responses = []
            fast_responses = []
            
            for i, model in enumerate(vision_list):
                processed += 1
                
                result = self.ask_model(model, messages)
                
                if result.get("success"):
                    responses.append(result["answer"])
                    fast_responses.append({
                        "desc": result["desc"],
                        "time": result["time"],
                        "success": True
                    })
                else:
                    fast_responses.append({
                        "desc": result["desc"],
                        "time": result.get("time", 0),
                        "success": False
                    })
                
                # Обновляем статус
                elapsed = time.time() - start_time
                percent = (processed / total) * 100
                avg_time = elapsed / processed if processed > 0 else 0
                remaining = avg_time * (total - processed)
                
                if chat_id and status_message_id:
                    stats = {
                        'processed': processed,
                        'total': total,
                        'percent': percent,
                        'elapsed': elapsed,
                        'remaining': remaining,
                        'responses': responses,
                        'fast_responses': fast_responses,
                        'avg_time': avg_time,
                        'is_photo': True
                    }
                    self.update_status(chat_id, status_message_id, stats)
            
            # Финальное обновление
            if chat_id and status_message_id:
                elapsed = time.time() - start_time
                stats = {
                    'processed': total,
                    'total': total,
                    'percent': 100,
                    'elapsed': elapsed,
                    'remaining': 0,
                    'responses': responses,
                    'fast_responses': fast_responses,
                    'avg_time': elapsed / total,
                    'is_photo': True
                }
                self.update_status(chat_id, status_message_id, stats)
            
            if responses:
                final = responses[0]
                final += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
                final += f"📸 **Vision анализ:** {len(responses)} моделей за {elapsed:.1f} сек"
                return final
            return "Не удалось проанализировать фото"
            
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def clear_context(self, user_id):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

brain = SuperBot()
