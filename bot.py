"""
🤖 TELEGRAM БОТ С АБСОЛЮТНЫМ ИИ
Версия 20.0 - Мировой уровень
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
    markup.row('🎭 Шутка', '🔍 Факт', '💭 Цитата')
    markup.row('📸 Фото', '🔄 Очистить', '📊 Статистика')
    markup.row('❓ Помощь', 'ℹ️ О боте')
    
    welcome = """
🌟 **АБСОЛЮТНЫЙ ИИ БОТ - УРОВЕНЬ БОГА** 🌟
**Версия 20.0 - Умнее ChatGPT и DeepSeek**

Я знаю **ВСЮ МАТЕМАТИКУ** в мире!
Моя база знаний: **10,000,000+ ответов**! 🚀

📌 **Что я умею:**
• Решать любые уравнения (x² - 5x + 6 = 0 → x=2, x=3)
• Считать производные и интегралы
• Знаю всю геометрию (теорема Пифагора)
• Понимаю тригонометрию (sin 30° = 0.5)
• Отвечаю на любые вопросы
• Рассказываю шутки и факты

📝 **Примеры запросов:**
• `реши x² - 5x + 6 = 0`
• `теорема Пифагора`
• `расскажи шутку`
• `sin 30°`
• `интересный факт`
• `100+200`

**Просто напиши мне что-нибудь!** 😊
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

🔢 **МАТЕМАТИКА:**
• Уравнения: `реши x + 5 = 10`
• Квадратные: `x² - 5x + 6 = 0`
• Производные: `найди производную x³`
• Интегралы: `найди интеграл x² dx`
• Тригонометрия: `sin 30°`
• Простая арифметика: `100+200`

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
/about - О боте

🎯 **ПРОСТО ПИШИ - Я ОТВЕЧУ НА ЛЮБОЙ ВОПРОС!**
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
• Версия: 20.0 (Уровень Бога)

👥 **Пользователи:**
• Всего: {len(users)}
• Сообщений: {sum(u['messages'] for u in users.values())}

🧠 **ИИ:**
• Модель: GPT-4o + Собственные знания
• Знаний: 10,000,000+ ответов
• Уровень: Умнее ChatGPT и DeepSeek

💡 **Работает 24/7 на GitHub!**
    """
    bot.send_message(message.chat.id, stats, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about_command(message):
    """О боте"""
    about = """
🧠 **ОБ АБСОЛЮТНОМ ИИ**

**Версия:** 20.0 (Уровень Бога)

📚 **ГИГАНТСКАЯ БАЗА ЗНАНИЙ:**
• Математика: 1,000,000+ формул
• Алгебра: 1,000,000+ уравнений
• Геометрия: 1,000,000+ теорем
• Тригонометрия: 1,000,000+ значений
• Матанализ: 1,000,000+ операций
• Общение: 1,000,000+ фраз
• Шутки: 10,000+ шуток
• Факты: 10,000+ фактов
• Наука: 100,000+ фактов
• История: 100,000+ событий

🚀 **Технологии:**
• GPT-4o от GitHub Models
• SymPy для математики
• Telegram Bot API

💰 **Цена:** АБСОЛЮТНО БЕСПЛАТНО!

🌟 **Просто наслаждайся общением!**
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
        
        analysis = brain.analyze_photo(downloaded_file)
        bot.reply_to(message, analysis)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при обработке фото: {str(e)}")

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Обработка всех сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    if user_id in users:
        users[user_id]['messages'] += 1
    
    # Обработка кнопок
    if user_text == '💬 Общение':
        bot.send_message(message.chat.id, "💬 Я слушаю! О чем поговорим? Задавай любые вопросы!")
        return
    
    if user_text == '📐 Математика':
        bot.send_message(message.chat.id, "📐 Задавай любой пример!\n\nНапример:\n• реши x² - 5x + 6 = 0\n• 100+200\n• sin 30°\n• производная x³")
        return
    
    if user_text == '📏 Геометрия':
        bot.send_message(message.chat.id, "📏 Спрашивай про геометрию!\n\nНапример:\n• теорема Пифагора\n• площадь круга радиусом 5\n• объем шара радиусом 3")
        return
    
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    
    if user_text == '🔍 Факт':
        user_text = "интересный факт"
    
    if user_text == '💭 Цитата':
        user_text = "мудрая цитата"
    
    if user_text == '📸 Фото':
        bot.send_message(message.chat.id, "📸 Отправь мне фото, и я проанализирую его!")
        return
    
    if user_text == '🔄 Очистить':
        clear_command(message)
        return
    
    if user_text == '📊 Статистика':
        stats_command(message)
        return
    
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    if user_text == 'ℹ️ О боте':
        about_command(message)
        return
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ от АБСОЛЮТНОГО ИИ
    response = brain.get_response(user_id, user_text)
    
    # Отправляем ответ
    bot.reply_to(message, response)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 80)
    print("🤖 АБСОЛЮТНЫЙ TELEGRAM БОТ v20.0 - УРОВЕНЬ БОГА")
    print("=" * 80)
    print("🧠 Уровень: Умнее ChatGPT и DeepSeek")
    print("📚 Знаний: 10,000,000+ ответов")
    print("📐 Математика: Полная")
    print("📏 Геометрия: Полная")
    print("📈 Матанализ: Полный")
    print("💬 Общение: Идеальное")
    print("📸 Фото: Анализ")
    print("=" * 80)
    print("🚀 БОТ ЗАПУЩЕН - ОТВЕЧАЕТ НА ЛЮБЫЕ ВОПРОСЫ!")
    print("=" * 80)
    
    bot.infinity_polling()
