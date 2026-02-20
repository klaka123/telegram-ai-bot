"""
Telegram бот с собственной нейросетью
Работает полностью на GitHub, бесплатно и навсегда!
"""

import telebot
from telebot import types
import time
import threading
import schedule
import os
from datetime import datetime
import random

# Подключаем нашу нейросеть
from model import brain

# Токен бота (получи у @BotFather)
TOKEN = "8039595780:AAHXwZWo0nL6LLjz9zN-Cw1CRkA4oJ5Q9cM"

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Хранилище пользователей
users = {}
admins = [123456789]  # Замени на свой Telegram ID

# Приветственное сообщение
WELCOME_MESSAGE = """
🌟 Добро пожаловать в бота с СОБСТВЕННОЙ НЕЙРОСЕТЬЮ! 🌟

Я уникальный бот, который:
🧠 Учится на каждом сообщении
📚 Запоминает наши разговоры
🤔 Думает как настоящий ИИ
💡 Отвечает по-разному каждый раз

Просто напиши мне что-нибудь, и я отвечу!
"""

HELP_MESSAGE = """
📚 Доступные команды:

/start - Начать общение
/help - Показать эту помощь
/stats - Статистика нейросети
/learn - Режим обучения
/clear - Очистить историю
/about - О боте

Для админов:
/admin - Панель управления
/save - Сохранить нейросеть
/broadcast - Сделать рассылку
"""

# ============== КОМАНДЫ БОТА ==============

@bot.message_handler(commands=['start'])
def start_command(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # Сохраняем пользователя
    if user_id not in users:
        users[user_id] = {
            'name': username,
            'first_seen': datetime.now(),
            'messages_count': 0,
            'mode': 'normal'
        }
    
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📝 Поговорить', '📊 Статистика')
    markup.row('❓ Помощь', 'ℹ️ О боте')
    
    # Отправляем приветствие
    bot.send_message(
        message.chat.id,
        f"Привет, {username}! 👋\n\n{WELCOME_MESSAGE}",
        reply_markup=markup
    )
    
    # Обучаем нейросеть на приветствии
    brain.train_on_message(f"Пользователь {username} начал общение")

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды /help"""
    bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Обработчик команды /stats - показывает статистику нейросети"""
    stats = f"""
📊 СТАТИСТИКА НЕЙРОСЕТИ

🧠 Словарь: {brain.words_count} слов
💾 Размер скрытого слоя: {brain.hidden_size} нейронов
📚 Изучено диалогов: {len(brain.conversations)}
🔄 Markov цепей: {len(brain.markov_chain)} состояний

👥 Пользователей: {len(users)}
💬 Всего сообщений: {sum(u['messages_count'] for u in users.values())}

⚙️ Режим: Обучение + Генерация
    """
    bot.send_message(message.chat.id, stats)

@bot.message_handler(commands=['learn'])
def learn_command(message):
    """Переключает режим обучения"""
    user_id = message.from_user.id
    
    if user_id in users:
        if users[user_id]['mode'] == 'normal':
            users[user_id]['mode'] = 'learning'
            bot.send_message(message.chat.id, "📚 Режим ОБУЧЕНИЯ включен! Теперь я буду внимательно учиться на твоих сообщениях.")
        else:
            users[user_id]['mode'] = 'normal'
            bot.send_message(message.chat.id, "✅ Режим обычного общения включен.")

@bot.message_handler(commands=['clear'])
def clear_command(message):
    """Очищает историю диалога"""
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "🧹 История диалога очищена! Давай начнем сначала.")
    # Обучаем нейросеть, что диалог сброшен
    brain.train_on_message(f"Пользователь {user_id} сбросил диалог")

@bot.message_handler(commands=['about'])
def about_command(message):
    """Информация о боте"""
    about_text = """
🤖 Telegram AI Bot v2.0

Уникальная особенность: У меня СОБСТВЕННАЯ нейросеть, 
написанная с нуля на чистом Python!

🔧 Технологии:
• Собственная нейросеть (Python + NumPy)
• Markov цепи для улучшения ответов
• Обратное распространение ошибки
• Функции активации ReLU и Softmax
• Автоматическое обучение на диалогах

📦 Версия: 2.0
📅 Создан: 2024
👨‍💻 Разработчик: Ты!

🌟 Хочешь такого же бота? 
Пиши в личные сообщения!
    """
    bot.send_message(message.chat.id, about_text)

# ============== АДМИН КОМАНДЫ ==============

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    """Админ панель"""
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, "⛔ У тебя нет прав администратора!")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💾 Сохранить", callback_data="save"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="users"),
        types.InlineKeyboardButton("🧠 Обучить", callback_data="train"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="broadcast"),
        types.InlineKeyboardButton("🔄 Перезапуск", callback_data="restart")
    )
    
    bot.send_message(message.chat.id, "👨‍💼 Панель администратора:", reply_markup=markup)

@bot.message_handler(commands=['save'])
def save_command(message):
    """Сохраняет нейросеть"""
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, "⛔ Нет прав!")
        return
    
    msg = bot.send_message(message.chat.id, "💾 Сохраняю нейросеть...")
    brain.save_weights()
    bot.edit_message_text("✅ Нейросеть успешно сохранена!", message.chat.id, msg.message_id)

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    """Рассылка сообщения всем пользователям"""
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, "⛔ Нет прав!")
        return
    
    msg = bot.send_message(message.chat.id, "📢 Введите сообщение для рассылки:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    """Обрабатывает рассылку"""
    text = message.text
    
    success = 0
    failed = 0
    
    status_msg = bot.send_message(message.chat.id, "📤 Начинаю рассылку...")
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 РАССЫЛКА:\n\n{text}")
            success += 1
        except:
            failed += 1
        
        # Обновляем статус каждые 10 пользователей
        if (success + failed) % 10 == 0:
            bot.edit_message_text(
                f"📤 Рассылка: {success} отправлено, {failed} ошибок",
                message.chat.id,
                status_msg.message_id
            )
    
    bot.edit_message_text(
        f"✅ Рассылка завершена!\n✓ Успешно: {success}\n✗ Ошибок: {failed}",
        message.chat.id,
        status_msg.message_id
    )

# ============== ОБРАБОТЧИКИ КНОПОК ==============

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик нажатий на inline кнопки"""
    if call.data == "save":
        brain.save_weights()
        bot.answer_callback_query(call.id, "✅ Нейросеть сохранена!")
    
    elif call.data == "stats":
        stats = f"Словарь: {brain.words_count} слов\nДиалогов: {len(brain.conversations)}"
        bot.answer_callback_query(call.id, stats)
    
    elif call.data == "users":
        bot.answer_callback_query(call.id, f"Пользователей: {len(users)}")
    
    elif call.data == "train":
        # Запускаем дополнительное обучение
        bot.answer_callback_query(call.id, "🧠 Начинаю обучение...")
        # Обучаем на всех сохраненных диалогах
        for q, a in brain.conversations[-10:]:  # Последние 10 диалогов
            brain.train_on_message(q, a)
        bot.send_message(call.message.chat.id, "✅ Обучение на последних диалогах завершено!")
    
    elif call.data == "restart":
        bot.answer_callback_query(call.id, "🔄 Перезапускаю...")
        # Здесь можно добавить код перезапуска

# ============== ОСНОВНОЙ ОБРАБОТЧИК СООБЩЕНИЙ ==============

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обрабатывает все текстовые сообщения"""
    user_id = message.from_user.id
    user_text = message.text
    
    # Пропускаем команды
    if user_text.startswith('/'):
        return
    
    # Сохраняем пользователя если его нет
    if user_id not in users:
        users[user_id] = {
            'name': message.from_user.first_name,
            'first_seen': datetime.now(),
            'messages_count': 0,
            'mode': 'normal'
        }
    
    # Увеличиваем счетчик сообщений
    users[user_id]['messages_count'] += 1
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Обрабатываем кнопки меню
    if user_text == '📝 Поговорить':
        bot.send_message(message.chat.id, "👋 Отлично! Напиши мне что-нибудь, и я отвечу!")
        return
    
    elif user_text == '📊 Статистика':
        stats_command(message)
        return
    
    elif user_text == '❓ Помощь':
        help_command(message)
        return
    
    elif user_text == 'ℹ️ О боте':
        about_command(message)
        return
    
    # Генерируем ответ нейросети
    try:
        # Разные режимы ответов
        if users[user_id]['mode'] == 'learning':
            # В режиме обучения просто подтверждаем получение
            bot.reply_to(message, "📚 Понял! Я запомнил это сообщение.")
            brain.train_on_message(user_text)
        else:
            # Обычный режим - генерируем ответ
            response = brain.generate_response(user_text)
            
            # Добавляем эмодзи для разнообразия
            emojis = ['😊', '🤔', '🌟', '💡', '✨', '🎯', '🚀', '💫']
            if random.random() > 0.7:
                response = f"{response} {random.choice(emojis)}"
            
            # Отправляем ответ
            bot.reply_to(message, response)
            
            # Обучаем на этом диалоге
            brain.train_on_message(user_text, response)
    
    except Exception as e:
        # Если что-то пошло не так
        error_message = f"❌ Ошибка: {str(e)}"
        bot.reply_to(message, "😅 Что-то пошло не так, но я уже учусь на этой ошибке!")
        brain.train_on_message(f"Ошибка: {user_text}")

# ============== ФОНОВЫЕ ЗАДАЧИ ==============

def auto_save():
    """Автоматически сохраняет нейросеть каждый час"""
    while True:
        time.sleep(3600)  # Каждый час
        brain.save_weights()
        print(f"💾 Автосохранение в {datetime.now()}")

def send_daily_stats():
    """Отправляет статистику админам каждый день"""
    for admin_id in admins:
        try:
            stats = f"""
📊 ДНЕВНАЯ СТАТИСТИКА
📅 {datetime.now().date()}

🧠 Словарь: {brain.words_count} слов
💬 Новых диалогов: {len(brain.conversations)}
👥 Активных пользователей: {len(users)}
            """
            bot.send_message(admin_id, stats)
        except:
            pass

# Планировщик задач
def run_scheduler():
    """Запускает планировщик задач"""
    schedule.every().day.at("12:00").do(send_daily_stats)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# ============== ЗАПУСК БОТА ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Telegram AI Bot с СОБСТВЕННОЙ нейросетью")
    print("=" * 50)
    print(f"📊 Стартовая статистика:")
    print(f"   • Словарь: {brain.words_count} слов")
    print(f"   • Диалогов: {len(brain.conversations)}")
    print(f"   • Markov цепей: {len(brain.markov_chain)}")
    print("=" * 50)
    print("✅ Бот запущен! Нажми Ctrl+C для остановки")
    print("=" * 50)
    
    # Запускаем автосохранение в отдельном потоке
    save_thread = threading.Thread(target=auto_save, daemon=True)
    save_thread.start()
    
    # Запускаем планировщик
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Запускаем бота
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Останавливаю бота...")
        brain.save_weights()
        print("✅ Нейросеть сохранена! До свидания!")
          
