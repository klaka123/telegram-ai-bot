"""
🤖 TELEGRAM БОТ — СУПЕР-КОМБО ИЗ ТРЁХ НЕЙРОСЕТЕЙ
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
    markup.row('📸 Отправить фото', '🧮 Пример')
    markup.row('🎭 Шутка', '🔍 Факт', '❓ Помощь')
    
    welcome = """
🌟 **СУПЕР-КОМБО ИЗ ТРЁХ НЕЙРОСЕТЕЙ** 🌟
**Llama 3.3 + Gemini 2.0 + Qwen VL = ИДЕАЛЬНЫЙ ОТВЕТ!**

📸 **ОТПРАВЛЯЙ ФОТО — ТРИ ИИ ОБДУМАЮТ И РЕШАТ!**
🧮 **ПРАВИЛЬНО СЧИТАЮТ:** 150+150/2 = 225 (проверено трижды)

📝 **ПРИМЕРЫ:**
• `150 + 150 / 2`
• `cos30`
• `x² - 5x + 6 = 0`
• `расскажи шутку`
• `интересный факт`

**ТРИ ГОЛОВЫ ЛУЧШЕ, ЧЕМ ОДНА!** 🚀
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    users[message.from_user.id] = {'messages': 0}

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📚 **КОМАНДЫ:**
/start - Начать
/help - Помощь
/clear - Очистить память

📸 **Фото:** отправь фото с примером — три ИИ проанализируют
🧮 **Примеры:** 150+150/2, cos30, x²-5x+6=0
🎭 **Шутка:** расскажи шутку
🔍 **Факт:** интересный факт

**Три нейросети работают вместе для лучшего ответа!** 🤖🤖🤖
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "🧹 Память очищена!")
    else:
        bot.reply_to(message, "✅ Память чиста!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 Три нейросети анализируют фото... Это займёт пару секунд!")
        
        analysis = brain.analyze_photo(downloaded_file, message.from_user.id)
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, analysis)
        
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
        bot.send_message(message.chat.id, "📸 Отправь мне фото с примером — три нейросети проанализируют его!")
        return
    if user_text == '🧮 Пример':
        bot.send_message(message.chat.id, "🧮 Например: `150 + 150 / 2`\nТри ИИ проверят правильность!")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '🔍 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "🤔 Три нейросети думают над ответом...")
    
    response = brain.ask_gpt(user_id, user_text)
    
    bot.delete_message(message.chat.id, status.message_id)
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("=" * 70)
    print("🤖 СУПЕР-КОМБО ИЗ ТРЁХ НЕЙРОСЕТЕЙ ЗАПУЩЕНО")
    print("=" * 70)
    print("📸 Понимает фото (три ИИ анализируют)")
    print("🧮 Правильно считает примеры (проверка тремя моделями)")
    print("💬 Общается как ChatGPT (три головы лучше одной)")
    print("=" * 70)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
        bot.polling(non_stop=True, interval=0, timeout=20)
