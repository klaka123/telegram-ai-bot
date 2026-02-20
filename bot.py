"""
🤖 TELEGRAM БОТ — С GPT-4o И ФОТО
"""

import os
import telebot
from telebot import types
from model import brain
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

users = {}
bot_start = datetime.now()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📸 Отправить фото', '🧮 Пример')
    markup.row('🎭 Шутка', '🔍 Факт', '❓ Помощь')
    
    welcome = """
🌟 **СУПЕР-БОТ С GPT-4o** 🌟

📸 **ОТПРАВЛЯЙ ФОТО — РЕШУ ЛЮБОЙ ПРИМЕР!**
🧮 **ПРАВИЛЬНО СЧИТАЮ:** 150+150/2 = 225

📝 **ПРИМЕРЫ:**
• `150 + 150 / 2`
• `cos30`
• `x² - 5x + 6 = 0`
• `расскажи шутку`
• `интересный факт`

**ПРОСТО НАПИШИ МНЕ!** 🚀
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    users[message.from_user.id] = {'messages': 0}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 Анализирую фото...")
        
        analysis = brain.analyze_photo(downloaded_file, message.from_user.id)
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, f"📸 **РЕШЕНИЕ:**\n\n{analysis}")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text
    
    if user_id in users:
        users[user_id]['messages'] += 1
    
    # Кнопки
    if user_text == '📸 Отправить фото':
        bot.send_message(message.chat.id, "📸 Отправь мне фото с примером!")
        return
    if user_text == '🧮 Пример':
        bot.send_message(message.chat.id, "🧮 Например: `150 + 150 / 2`")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '🔍 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        bot.reply_to(message, "/start - помощь")
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    response = brain.ask_gpt(user_id, user_text)
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 БОТ ЗАПУЩЕН — ЖДЁМ СООБЩЕНИЯ")
    print("=" * 60)
    bot.infinity_polling()
