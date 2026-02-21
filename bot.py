"""
TELEGRAM БОТ — Стабильная версия
"""

import os
import telebot
from telebot import types
from model import brain
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logging.error("❌ Нет токена!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📷 Фото', '📝 Пример')
    markup.row('🎭 Шутка', '📊 Факт', '❓ Помощь')
    
    welcome = """
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ

Принцип работы:
• 30+ нейросетей одновременно анализируют вопрос
• Скорость ответа: 2-5 секунд
• Распознавание фото

Введите запрос или отправьте фото.
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 Анализ фото...")
        
        analysis = brain.analyze_photo(downloaded_file, message.from_user.id)
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, analysis)
        
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_text = message.text
    
    # Обработка кнопок
    if user_text == '📷 Фото':
        bot.reply_to(message, "Отправьте фото с примером")
        return
    if user_text == '📝 Пример':
        bot.reply_to(message, "Примеры:\n• 150 + 150 / 2\n• cos 30°\n• x² - 5x + 6 = 0")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '📊 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        bot.reply_to(message, "/start - начало\n/help - помощь\n/clear - сброс")
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "🔄 Анализ запроса...")
    
    try:
        response = brain.get_response(message.from_user.id, user_text)
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, response)
    except Exception as e:
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    logging.info("🚀 Бот запущен")
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
