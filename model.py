"""
РЕАЛЬНЫЙ ИИ через GitHub Models
Никакой самодельной нейросети - только настоящий GPT!
"""

import os
from openai import OpenAI
import json

class RealAI:
    """
    Настоящий искусственный интеллект от GitHub
    """
    
    def __init__(self):
        # Получаем токен из секретов
        self.github_token = os.environ.get('GITHUB_TOKEN')
        if not self.github_token:
            print("❌ ОШИБКА: Нет GITHUB_TOKEN в секретах!")
            print("Добавь секрет GITHUB_TOKEN с твоим Personal Access Token")
        
        # Подключаемся к GitHub Models
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=self.github_token,
        )
        
        # Память для каждого пользователя
        self.user_contexts = {}
        
        print("🤖 Настоящий ИИ инициализирован!")
        print("   Модель: GPT-4o (бесплатно от GitHub)")
    
    def get_response(self, user_id, message):
        """
        Получает ответ от настоящего ИИ
        """
        
        # Создаем или получаем контекст пользователя
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = [
                {"role": "system", "content": """Ты дружелюбный ИИ-помощник. 
                Отвечай кратко, понятно и с юмором. 
                Помогай с любыми вопросами, особенно с математикой.
                Если спрашивают математику - решай пошагово.
                Всегда будь вежливым и позитивным."""}
            ]
        
        # Добавляем сообщение пользователя
        self.user_contexts[user_id].append({"role": "user", "content": message})
        
        # Ограничиваем контекст (последние 10 сообщений)
        if len(self.user_contexts[user_id]) > 11:
            self.user_contexts[user_id] = [self.user_contexts[user_id][0]] + self.user_contexts[user_id][-10:]
        
        try:
            # Запрос к GitHub Models
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Самая умная бесплатная модель!
                messages=self.user_contexts[user_id],
                temperature=0.7,
                max_tokens=500,
            )
            
            # Получаем ответ
            answer = response.choices[0].message.content
            
            # Сохраняем ответ в контекст
            self.user_contexts[user_id].append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            error_text = str(e)
            if "401" in error_text:
                return "❌ Ошибка токена GitHub! Проверь секрет GITHUB_TOKEN"
            elif "429" in error_text:
                return "⏳ Лимит запросов исчерпан. Подожди немного и попробуй снова."
            else:
                return f"❌ Ошибка: {error_text[:100]}"
    
    def clear_context(self, user_id):
        """Очищает контекст пользователя"""
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

# Создаем экземпляр
brain = RealAI()
