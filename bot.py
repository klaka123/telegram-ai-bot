"""
Telegram бот с настоящим ИИ от GitHub
"""

import os
import telebot
from telebot import types
from model import brain

# Токен из секретов GitHub
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Статистика
users = {}

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💬 Поговорить', '🧮 Математика')
    markup.row('🎭 Шутка', '🔍 Факт')
    markup.row('🔄 Очистить', '❓ Помощь')
    
    welcome = """
🌟 **НАСТОЯЩИЙ ИИ БОТ** 🌟

Я использую **GPT-4o** от GitHub!
Задавай любые вопросы:

📐 **Математика:** "реши x² - 5x + 6 = 0"
💬 **Общение:** "Как дела?"
🎭 **Шутки:** "Расскажи анекдот"
🔍 **Факты:** "Интересный факт"

Напиши мне что-нибудь!
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    users[message.from_user.id] = {'name': message.from_user.first_name}

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📚 **Команды:**
/start - Начать
/help - Помощь
/clear - Очистить память
/math - Режим математики

💡 **Примеры:**
• реши 2x + 5 = 15
• найди производную x³
• sin 30°
• 1000 + 2300 = ?

🎯 Просто пиши вопросы!
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_command(message):
    """Очистка контекста"""
    user_id = message.from_user.id
    if brain.clear_context(user_id):
        bot.send_message(message.chat.id, "🧹 Память очищена! Начинаем с чистого листа.")
    else:
        bot.send_message(message.chat.id, "✅ Память и так чиста!")

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Обработка всех сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    # Обработка кнопок
    if user_text == '💬 Поговорить':
        bot.send_message(message.chat.id, "👋 Я слушаю! О чем поговорим?")
        return
    
    if user_text == '🧮 Математика':
        bot.send_message(message.chat.id, "📐 Задавай любой пример! Например: 'реши x² - 5x + 6 = 0'")
        return
    
    if user_text == '🎭 Шутка':
        user_text = "Расскажи смешную шутку"
    
    if user_text == '🔍 Факт':
        user_text = "Расскажи интересный факт"
    
    if user_text == '🔄 Очистить':
        clear_command(message)
        return
    
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ от настоящего ИИ
    response = brain.get_response(user_id, user_text)
    
    # Отправляем ответ
    bot.reply_to(message, response)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TELEGRAM БОТ С НАСТОЯЩИМ ИИ")
    print("=" * 50)
    print("Модель: GPT-4o от GitHub")
    print("Статус: Запуск...")
    print("=" * 50)
    
    bot.infinity_polling()
