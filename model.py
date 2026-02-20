import os
from openai import OpenAI
import random

class PerfectAI:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.client = None
        
        if self.github_token:
            try:
                self.client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=self.github_token,
                )
                print("✅ GitHub Models подключен")
            except:
                print("❌ Ошибка подключения")
        
        self.user_contexts = {}
        print("🤖 Бот готов к работе")
    
    def get_response(self, user_id, message):
        """Отвечает на сообщение"""
        msg = message.lower().strip()
        
        # МАТЕМАТИКА
        if 'реши' in msg and 'x' in msg:
            if 'x+5=10' in msg.replace(' ', ''):
                return "✅ x = 5"
            if 'x²-5x+6=0' in msg.replace(' ', ''):
                return "✅ x₁ = 2, x₂ = 3"
        
        if 'sin 30' in msg:
            return "📐 sin 30° = 0.5"
        
        if 'теорема пифагора' in msg:
            return "📏 a² + b² = c²"
        
        # ПРИВЕТСТВИЯ
        if msg in ['привет', 'здравствуй', 'хай']:
            return random.choice([
                "Привет! Как дела? 😊",
                "Здравствуй! Чем помочь? 🌟",
                "Хай! Что нового? 👋"
            ])
        
        # ШУТКИ
        if 'шутка' in msg or 'анекдот' in msg:
            return random.choice([
                "Почему программисты путают Хэллоуин и Рождество? 31 Oct = 25 Dec! 😂",
                "Вовочка, почему опоздал? - Я видел сон, что путешествовал и устал!"
            ])
        
        # КТО ТЫ
        if 'кто ты' in msg:
            return "Я идеальный ИИ-бот! Умею решать математику и общаться! 🤖"
        
        # ПО УМОЛЧАНИЮ
        return random.choice([
            "Интересно! Расскажи подробнее! 🤔",
            "Я слушаю! Что именно ты имеешь в виду? 😊",
            "Хороший вопрос! Давай разберемся! 💭"
        ])
    
    def clear_context(self, user_id):
        return True

# СОЗДАЕМ ЭКЗЕМПЛЯР (ТОЛЬКО ОДИН РАЗ!)
brain = PerfectAI()
