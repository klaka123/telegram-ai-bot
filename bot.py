"""
Telegram бот с умной нейросетью
Версия 3.0 - Понимает текст и фото
"""

import os
import telebot
from telebot import types
from model import brain
import random
from datetime import datetime

# Токен из секретов GitHub
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Статистика
users_stats = {}
bot_start_time = datetime.now()

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💬 Поговорить', '📊 Статистика')
    markup.row('📸 Прислать фото', '❓ Помощь')
    
    welcome = """
🧠 **УМНАЯ НЕЙРОСЕТЬ v3.0**

Привет! Я нейросеть, которая:
✅ Учится на каждом сообщении
✅ Понимает фото
✅ Помнит диалоги
✅ Знает тысячи фраз

Просто напиши мне что-нибудь!
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    
    # Обучаемся на приветствии
    brain.train_on_message(f"Пользователь {message.from_user.first_name} начал диалог")

@bot.message_handler(commands=['help'])
def help_command(message):
    """Помощь"""
    help_text = f"""
📚 **Доступные команды:**

/start - Начать общение
/help - Показать помощь
/stats - Статистика нейросети
/clear - Очистить память

📸 **Функции:**
• Отправь фото - я проанализирую
• Напиши текст - я отвечу
• Задавай любые вопросы

🧠 **Нейросеть:**
• Словарь: {brain.words_count} слов
• Нейронов: 512
    """
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Статистика"""
    uptime = datetime.now() - bot_start_time
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds // 60) % 60
    
    stats_text = f"""
📊 **СТАТИСТИКА НЕЙРОСЕТИ**

🧠 **Модель:**
• Словарь: {brain.words_count} слов
• Нейронов: 512
• Память: {len(brain.long_term_memory)} диалогов

📚 **Обучение:**
• База знаний: {len(brain.knowledge_base)} фраз
• Markov цепей: {len(brain.markov_chain)}

⏱️ **Работа:**
• Аптайм: {hours}ч {minutes}мин
• Пользователей: {len(users_stats)}

💡 **Статус:** Активен
    """
    
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_command(message):
    """Очистка памяти"""
    user_id = message.from_user.id
    if user_id in brain.user_memories:
        del brain.user_memories[user_id]
    brain.short_term_memory = []
    bot.send_message(message.chat.id, "🧹 Память очищена! Начинаем с чистого листа.")

# ========== ОБРАБОТКА ТЕКСТА ==========
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    """Обработка всех текстовых сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    # Обновляем статистику
    if user_id not in users_stats:
        users_stats[user_id] = {'messages': 0, 'first_seen': datetime.now()}
    users_stats[user_id]['messages'] += 1
    
    # ===== ОБРАБОТКА КНОПОК =====
    if user_text == '💬 Поговорить':
        bot.send_message(message.chat.id, "👋 Отлично! Я слушаю... Напиши мне что-нибудь!")
        return
    
    if user_text == '📊 Статистика':
        stats_command(message)
        return
    
    if user_text == '📸 Прислать фото':
        bot.send_message(message.chat.id, "📸 Отправляй фото, я проанализирую!")
        return
    
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    # ===== ЕСЛИ ЭТО НЕ КНОПКА - ОТВЕЧАЕМ! =====
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Генерируем ответ
    response = brain.generate_response(user_text, user_id)
    
    # Добавляем эмодзи
    emojis = ['😊', '🤔', '🌟', '💫', '✨', '🎯', '🚀', '💡']
    if random.random() > 0.5 and not any(e in response for e in emojis):
        response += ' ' + random.choice(emojis)
    
    # Отправляем ответ
    bot.reply_to(message, response)
    
    # Обучаемся на диалоге
    brain.train_on_message(user_text, response)

# ========== ОБРАБОТКА ФОТО ==========
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обработка фотографий"""
    
    # Получаем фото
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Показываем что бот думает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Анализируем фото
    analysis = brain.analyze_photo(downloaded_file)
    
    # Отправляем результат
    bot.reply_to(message, f"📸 **Анализ фото:**\n\n{analysis}", parse_mode='Markdown')
    
    # Обучаемся
    brain.train_on_message("[ФОТО]", analysis)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🧠 УМНЫЙ TELEGRAM БОТ v3.0")
    print("=" * 50)
    print(f"📊 Статистика:")
    print(f"   • Словарь: {brain.words_count} слов")
    print(f"   • База знаний: {len(brain.knowledge_base)} фраз")
    print(f"   • Нейронов: 512")
    print("=" * 50)
    print("✅ Бот запущен!")
    print("=" * 50)
    
    bot.infinity_polling()
