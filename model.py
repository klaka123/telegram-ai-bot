"""
TELEGRAM БОТ — 30+ НЕЙРОСЕТЕЙ, БЫСТРЫЙ АНАЛИЗ
"""

import os
import telebot
from telebot import types
from model import brain
from datetime import datetime
import time

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

users = {}
bot_start = datetime.now()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📷 Фото', '📝 Пример')
    markup.row('🎭 Шутка', '📊 Факт', '❓ Помощь')
    
    welcome = """
АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ

Принцип работы:
• 30+ нейросетей одновременно анализируют вопрос
• Система находит консенсус большинства
• Скорость ответа: 3-8 секунд
• Распознавание фото через Vision-модели

Возможности:
• Математика (150 + 150 / 2 = 225)
• Распознавание фото
• Ответы на любые вопросы
• Факты и шутки

Введите запрос или отправьте фото.
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup)
    users[message.from_user.id] = {'messages': 0}

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
Доступные команды:
/start - начало работы
/help - справка
/clear - сброс диалога

Примеры запросов:
• 150 + 150 / 2
• cos 30°
• x² - 5x + 6 = 0
• расскажи шутку
• интересный факт

Для анализа фото отправьте изображение.
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "История диалога очищена")
    else:
        bot.reply_to(message, "История уже пуста")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "Анализ фото через Vision-модели...")
        
        analysis = brain.analyze_photo(downloaded_file, message.from_user.id)
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, analysis)
        
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text
    
    if user_id in users:
        users[user_id]['messages'] += 1
    
    # Обработка кнопок
    if user_text == '📷 Фото':
        bot.reply_to(message, "Отправьте фото с примером для анализа")
        return
    if user_text == '📝 Пример':
        bot.reply_to(message, "Примеры запросов:\n• 150 + 150 / 2\n• cos 30°\n• x² - 5x + 6 = 0")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '📊 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "Анализ запроса...")
    
    response = brain.get_response(user_id, user_text)
    
    bot.delete_message(message.chat.id, status.message_id)
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("=" * 80)
    print("ЗАПУСК TELEGRAM БОТА — 30+ НЕЙРОСЕТЕЙ")
    print("=" * 80)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
        bot.polling(non_stop=True, interval=0, timeout=20)
