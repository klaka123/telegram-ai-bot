import os
import telebot
import sys

# ========== ПРОВЕРКА ТОКЕНА ==========
print("🔍 ДИАГНОСТИКА ТОКЕНА")
print("-" * 50)

# Проверяем переменные окружения
print(f"1. Все переменные окружения: {list(os.environ.keys())}")

# Проверяем BOT_TOKEN
token = os.environ.get('BOT_TOKEN')
print(f"2. BOT_TOKEN получен: {'✅ ДА' if token else '❌ НЕТ'}")

if token:
    print(f"3. Длина токена: {len(token)} символов")
    print(f"4. Первые 10 символов: {token[:10]}...")
    print(f"5. Последние 5 символов: ...{token[-5:]}")
    
    # Проверяем формат токена
    if ':' in token:
        parts = token.split(':')
        print(f"6. Формат токена: ✅ КОРРЕКТНЫЙ (есть двоеточие)")
        print(f"7. ID бота: {parts[0]}")
    else:
        print(f"6. Формат токена: ❌ НЕКОРРЕКТНЫЙ (нет двоеточия!)")
else:
    print("❌ ТОКЕН НЕ НАЙДЕН В ПЕРЕМЕННЫХ ОКРУЖЕНИЯ!")
    sys.exit(1)

print("-" * 50)

# ========== ПОДКЛЮЧЕНИЕ К TELEGRAM ==========
print("🚀 Пробуем подключиться к Telegram...")

try:
    bot = telebot.TeleBot(token)
    me = bot.get_me()
    print(f"✅ УСПЕХ! Бот @{me.username} (ID: {me.id}) подключен!")
    
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "✅ Бот работает! Токен правильный!")
    
    @bot.message_handler(func=lambda m: True)
    def echo(message):
        bot.reply_to(message, f"Ты написал: {message.text}")
    
    print("🔄 Бот запускает polling...")
    bot.infinity_polling()
    
except Exception as e:
    print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
    print(f"Тип ошибки: {type(e).__name__}")
