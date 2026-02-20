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
🌟 **СУПЕР-БОТ С DEEPSEEK V3** 🌟
**БЕСПЛАТНО, ПОНИМАЕТ ФОТО, УМНЫЙ КАК CHATGPT!**

📸 **ОТПРАВЛЯЙ ФОТО — РЕШУ ЛЮБОЙ ПРИМЕР!**
🧮 **ПРАВИЛЬНО СЧИТАЮ:** 150+150/2 = 225

📝 **ПРИМЕРЫ:**
• `150 + 150 / 2`
• `cos30`
• `x² - 5x + 6 = 0`
• `расскажи шутку`

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
        status = bot.reply_to(message, "📸 Анализирую фото через DeepSeek...")
        
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
        help_command(message)
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    response = brain.ask_gpt(user_id, user_text)
    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📚 **КОМАНДЫ:**
/start - Начать
/help - Помощь
/clear - Очистить память

📸 **Фото:** отправь фото с примером
🧮 **Примеры:** 150+150/2, cos30, x²-5x+6=0
🎭 **Шутка:** расскажи шутку
🔍 **Факт:** интересный факт
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "🧹 Память очищена!")
    else:
        bot.reply_to(message, "✅ Память чиста!")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 БОТ С DEEPSEEK V3 ЗАПУЩЕН — БЕСПЛАТНО!")
    print("=" * 60)
    print("📸 Понимает фото")
    print("🧮 Правильно считает примеры")
    print("💬 Общается как ChatGPT")
    print("=" * 60)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        time.sleep(5)
        bot.polling(non_stop=True, interval=0, timeout=20)
