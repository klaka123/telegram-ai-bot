"""
🤖 ИДЕАЛЬНЫЙ TELEGRAM БОТ
Фронтенд для идеальной нейросети
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
    """Идеальное приветствие"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💬 Общение', '📐 Математика', '📏 Геометрия')
    markup.row('🎭 Шутка', '🔍 Факт', '❓ Помощь')
    markup.row('🔄 Очистить', '📊 Статистика')
    
    welcome = """
🌟 **ИДЕАЛЬНЫЙ ИИ БОТ** 🌟

Я знаю ВСЁ, что знает ChatGPT и DeepSeek!
И даже больше! 😉

📌 **Что я умею:**
• Решать любую математику
• Объяснять геометрию
• Отвечать на вопросы
• Шутить и общаться
• Запоминать диалоги

📝 **Примеры:**
• "реши x² - 5x + 6 = 0"
• "теорема Пифагора"
• "расскажи шутку"
• "sin 30°"

**Просто напиши мне что-нибудь!** 🚀
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    
    # Сохраняем пользователя
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

🔢 **МАТЕМАТИКА:**
• Уравнения: `реши x + 5 = 10`
• Квадратные: `x² - 5x + 6 = 0`
• Производные: `найди производную x³`
• Интегралы: `найди интеграл x² dx`
• Тригонометрия: `sin 30°`

📐 **ГЕОМЕТРИЯ:**
• `теорема Пифагора`
• `площадь круга радиусом 5`
• `объем шара радиусом 3`

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

🎯 **ПРОСТО ПИШИ - Я ОТВЕЧУ!**
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
• Память: Индивидуальная

💡 **Версия:** 7.0 (Абсолют)
    """
    bot.send_message(message.chat.id, stats, parse_mode='Markdown')

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Обработка всех сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    # Обновляем статистику
    if user_id in users:
        users[user_id]['messages'] += 1
    
    # Обработка кнопок
    if user_text == '💬 Общение':
        bot.send_message(message.chat.id, "💬 Я слушаю! О чем поговорим? Задавай любые вопросы!")
        return
    
    if user_text == '📐 Математика':
        bot.send_message(message.chat.id, "📐 Задавай любой пример!\n\nНапример:\n• реши x + 5 = 10\n• x² - 5x + 6 = 0\n• найди производную x³\n• sin 30°")
        return
    
    if user_text == '📏 Геометрия':
        bot.send_message(message.chat.id, "📏 Спрашивай про геометрию!\n\nНапример:\n• теорема Пифагора\n• площадь круга радиусом 5\n• объем шара радиусом 3")
        return
    
    if user_text == '🎭 Шутка':
        # Превращаем кнопку в запрос
        user_text = "расскажи шутку"
    
    if user_text == '🔍 Факт':
        user_text = "расскажи интересный факт"
    
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    if user_text == '🔄 Очистить':
        clear_command(message)
        return
    
    if user_text == '📊 Статистика':
        stats_command(message)
        return
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ от идеального ИИ
    response = brain.get_response(user_id, user_text)
    
    # Отправляем ответ
    bot.reply_to(message, response)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 ИДЕАЛЬНЫЙ TELEGRAM БОТ v7.0")
    print("=" * 60)
    print("🧠 Уровень: ChatGPT + DeepSeek")
    print("📐 Математика: Полная поддержка")
    print("💬 Общение: Идеальное")
    print("=" * 60)
    print("🚀 Бот запущен и готов к работе!")
    print("=" * 60)
    
    bot.infinity_polling()
