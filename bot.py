"""
TELEGRAM БОТ — 31 НЕЙРОСЕТЬ, КРАСИВОЕ ОФОРМЛЕНИЕ
"""

import os
import telebot
from telebot import types
from model import brain
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

bot = telebot.TeleBot(TOKEN)
brain.set_bot(bot)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📸 Фото', '📝 Примеры')
    markup.row('⚡ Простой вопрос', '🧠 Сложный вопрос')
    markup.row('🎭 Шутка', '🔍 Факт', '❓ Помощь')
    
    welcome = """
🌟 **ИНТЕЛЛЕКТУАЛЬНАЯ СИСТЕМА — 31 НЕЙРОСЕТЬ** 🌟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ **ПРОСТЫЕ ВОПРОСЫ** (1-2 секунды)
• `150 + 150 / 2` → 225
• `cos 30°` → 0.866
• `расскажи шутку`

🧠 **СЛОЖНЫЕ ВОПРОСЫ** (наука, логика)
• Объясни теорию относительности
• Напиши код быстрой сортировки
• В чем смысл жизни?

📸 **ФОТО** — отправь любой пример

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Просто напиши мне что-нибудь!
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
❓ **ПОМОЩЬ** ❓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Простые запросы:**
• `150 + 150 / 2`
• `cos 30°`
• `x² - 5x + 6 = 0`
• `расскажи шутку`
• `интересный факт`

🧠 **Сложные запросы:**
• `Объясни теорию относительности`
• `Напиши код быстрой сортировки на Python`
• `В чем разница между ИИ и ML?`

📸 **Фото:** отправьте изображение с примером

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "🧹 История диалога очищена")
    else:
        bot.reply_to(message, "✅ История уже пуста")

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
    if user_text == '📸 Фото':
        bot.reply_to(message, "📸 Отправьте фото с примером")
        return
    if user_text == '📝 Примеры':
        bot.reply_to(message, "📝 **Примеры:**\n• `150 + 150 / 2`\n• `cos 30°`\n• `x² - 5x + 6 = 0`", parse_mode='Markdown')
        return
    if user_text == '⚡ Простой вопрос':
        bot.reply_to(message, "⚡ Напишите простой вопрос (быстрый ответ)")
        return
    if user_text == '🧠 Сложный вопрос':
        bot.reply_to(message, "🧠 Задайте сложный вопрос (подключатся мощные модели)")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '🔍 Факт':
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
    print("\n" + "="*60)
    print("🚀 ЗАПУСК TELEGRAM БОТА — 31 НЕЙРОСЕТЬ")
    print("="*60 + "\n")
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
