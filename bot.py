"""
🤖 TELEGRAM БОТ — МЕГА-УРОВЕНЬ
"""

import os
import telebot
from telebot import types
from model import brain
import time
from datetime import datetime

# Токен из секретов GitHub
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Статистика
users = {}
bot_start = datetime.now()

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📸 Отправить фото', '🧮 Решить пример')
    markup.row('🎭 Шутка', '🔍 Факт', '❓ Помощь')
    markup.row('📊 Статистика', '🔄 Очистить', 'ℹ️ О боте')
    
    welcome = """
🌟 **МЕГА-БОТ — УРОВЕНЬ CHATGPT + DEEPSEEK** 🌟

📸 **ОТПРАВЬ ФОТО С ПРИМЕРОМ — Я РЕШУ!**
🧮 **ПРАВИЛЬНО СЧИТАЮ:** 150+150/2 = 225 (сначала деление!)

📌 **ЧТО Я УМЕЮ:**
• Математика (алгебра, геометрия, тригонометрия)
• Физика, химия, история
• Общение на русском и английском
• Шутки и интересные факты

📝 **ПРИМЕРЫ ЗАПРОСОВ:**
• `150 + 150/2`
• `cos30`
• `x² - 5x + 6 = 0`
• `расскажи шутку`
• `интересный факт`

**ПРОСТО НАПИШИ МНЕ ЧТО-НИБУДЬ!** 🚀
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    
    users[message.from_user.id] = {
        'name': message.from_user.first_name,
        'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'messages': 0
    }

@bot.message_handler(commands=['help'])
def help_command(message):
    """Помощь"""
    help_text = """
📚 **КОМАНДЫ И ВОЗМОЖНОСТИ:**

📸 **ФОТО:**
• Отправь фото с примером — я решу!

🧮 **МАТЕМАТИКА:**
• `150 + 150/2` = 225 (правильный порядок!)
• `cos30` = 0.866
• `x² - 5x + 6 = 0` → x=2, x=3

💬 **ОБЩЕНИЕ:**
• `привет`, `как дела`
• `расскажи шутку`
• `интересный факт`
• `кто ты`

⚙️ **КОМАНДЫ:**
/start - Начать
/help - Помощь
/clear - Очистить память
/stats - Статистика
/about - О боте

🎯 **ПРОСТО ПИШИ ИЛИ ОТПРАВЛЯЙ ФОТО!**
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_command(message):
    """Очистка памяти"""
    if brain.clear_context(message.from_user.id):
        bot.send_message(message.chat.id, "🧹 Память очищена! Начинаем с чистого листа.")
    else:
        bot.send_message(message.chat.id, "✅ Память и так чиста!")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Статистика"""
    uptime = datetime.now() - bot_start
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds // 60) % 60
    
    stats = f"""
📊 **СТАТИСТИКА**

🤖 **Бот:**
• Статус: Активен
• Аптайм: {hours}ч {minutes}мин

👥 **Пользователи:**
• Всего: {len(users)}
• Сообщений: {sum(u['messages'] for u in users.values())}

🧠 **ИИ:**
• Модель: GPT-4o
• Уровень: ChatGPT + DeepSeek
• Языки: русский, английский

💡 **Работает 24/7!**
    """
    bot.send_message(message.chat.id, stats, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about_command(message):
    """О боте"""
    about = """
🧠 **О МЕГА-БОТЕ**

**Уровень:** ChatGPT + DeepSeek
**Модель:** GPT-4o через OpenRouter

📚 **ЗНАНИЯ:**
• Математика (алгебра, геометрия, тригонометрия)
• Физика (механика, оптика, квантовая)
• Химия (элементы, реакции, формулы)
• История (все эпохи)
• Языки (русский, английский)

📸 **ФУНКЦИИ:**
• Распознавание фото с примерами
• Правильный порядок вычислений
• Поддержка диалога
• Шутки и факты

💰 **Цена:** АБСОЛЮТНО БЕСПЛАТНО!

🌟 **Наслаждайся общением!**
    """
    bot.send_message(message.chat.id, about, parse_mode='Markdown')

# ========== ОБРАБОТКА ФОТО ==========
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обработка фотографий"""
    
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status_msg = bot.reply_to(message, "📸 Анализирую фото... Секунду!")
        
        analysis = brain.analyze_photo(downloaded_file, message.from_user.id)
        
        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, f"📸 **РЕШЕНИЕ ПО ФОТО:**\n\n{analysis}")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}\n\nПопробуй написать пример текстом!")

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Обработка всех сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    if user_id in users:
        users[user_id]['messages'] += 1
    
    # Обработка кнопок
    if user_text == '📸 Отправить фото':
        bot.send_message(message.chat.id, "📸 Отправь мне фото с примером, и я решу его!")
        return
    
    if user_text == '🧮 Решить пример':
        bot.send_message(message.chat.id, "🧮 Напиши любой пример!\n\nНапример:\n• `150 + 150/2`\n• `cos30`\n• `x² - 5x + 6 = 0`")
        return
    
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    
    if user_text == '🔍 Факт':
        user_text = "интересный факт"
    
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    if user_text == '📊 Статистика':
        stats_command(message)
        return
    
    if user_text == '🔄 Очистить':
        clear_command(message)
        return
    
    if user_text == 'ℹ️ О боте':
        about_command(message)
        return
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ
    response = brain.ask_gpt(user_id, user_text)
    
    # Отправляем ответ
    bot.reply_to(message, response)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 МЕГА-БОТ ЗАПУЩЕН — УРОВЕНЬ CHATGPT")
    print("=" * 60)
    print("🧠 Модель: GPT-4o")
    print("📚 Знания: математика, физика, химия, история")
    print("💬 Языки: русский, английский")
    print("📸 Фото: поддерживается")
    print("=" * 60)
    
    bot.infinity_polling()
