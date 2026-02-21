"""
TELEGRAM БОТ — Максимальная скорость для простых вопросов
"""

import os
import telebot
from telebot import types
from model import brain
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logging.error("❌ Нет токена!")
    exit(1)

bot = telebot.TeleBot(TOKEN)
brain.set_bot(bot)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📷 Фото', '📝 Примеры')
    markup.row('🎭 Шутка', '📊 Факт', '❓ Помощь')
    
    welcome = """
🔬 **ИНТЕЛЛЕКТУАЛЬНАЯ СИСТЕМА — 31 НЕЙРОСЕТЬ**

⚡ **ПРОСТЫЕ ВОПРОСЫ** (1-2 секунды):
• 150 + 150 / 2
• cos 30°
• расскажи шутку

🧠 **СЛОЖНЫЕ ВОПРОСЫ** (наука, логика):
• Объясни теорию относительности
• Напиши код сортировки
• В чем смысл жизни?

📸 **ФОТО** (любые примеры)

Система сама выберет лучшие модели!
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
❓ **Помощь:**

📝 **Примеры простых запросов:**
• 150 + 150 / 2
• cos 30°
• x² - 5x + 6 = 0
• расскажи шутку
• интересный факт

🧠 **Примеры сложных запросов:**
• Объясни теорию относительности
• Напиши код быстрой сортировки на Python
• В чем разница между ИИ и машинным обучением?

📸 **Фото:** отправьте изображение с примером
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "🧹 История очищена")
    else:
        bot.reply_to(message, "✅ История пуста")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 **Анализ фото...**")
        
        analysis = brain.analyze_photo(
            downloaded_file, 
            message.from_user.id,
            chat_id=message.chat.id,
            status_message_id=status.message_id
        )
        
        bot.reply_to(message, analysis)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_text = message.text
    
    # Обработка кнопок
    if user_text == '📷 Фото':
        bot.reply_to(message, "📸 Отправьте фото с примером")
        return
    if user_text == '📝 Примеры':
        bot.reply_to(message, "📝 **Примеры:**\n• Простой: `150 + 150 / 2`\n• Сложный: `Объясни теорию относительности`")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '📊 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "🔬 **Анализ запроса...**")
    
    try:
        response = brain.get_response(
            message.from_user.id, 
            user_text,
            chat_id=message.chat.id,
            status_message_id=status.message_id
        )
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

if __name__ == "__main__":
    logging.info("=" * 80)
    logging.info("🚀 ЗАПУСК БОТА — 31 НЕЙРОСЕТЬ")
    logging.info("=" * 80)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
